"""High-entropy scoped local credentials and user-only secret-file storage."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from pathlib import Path

from portatlas.application.authorization import Scope
from portatlas.domain.clock import Clock, SystemClock, require_utc
from portatlas.domain.identity import OpaqueId, ResourceKind

IdFactory = Callable[[ResourceKind], OpaqueId]


@dataclass(frozen=True, slots=True)
class CredentialRecord:
    credential_id: OpaqueId
    salt: str
    digest: str
    scopes: frozenset[Scope]
    created_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.credential_id.kind is not ResourceKind.CREDENTIAL:
            raise ValueError("Credential record requires a credential identifier.")
        require_utc(self.created_at)
        if self.expires_at is not None:
            require_utc(self.expires_at)
            if self.expires_at <= self.created_at:
                raise ValueError("Credential expiration must follow creation.")
        if self.revoked_at is not None:
            require_utc(self.revoked_at)

    def revoke(self, clock: Clock) -> CredentialRecord:
        return replace(self, revoked_at=require_utc(clock.now()))


@dataclass(frozen=True, slots=True)
class IssuedCredential:
    record: CredentialRecord
    secret: str = field(repr=False)


class TokenService:
    """Issue raw material once and persist only a salted scrypt digest."""

    def __init__(
        self,
        *,
        clock: Clock | None = None,
        id_factory: IdFactory = OpaqueId.new,
    ) -> None:
        self._clock = clock or SystemClock()
        self._id_factory = id_factory

    @staticmethod
    def _derive(secret: str, salt: bytes) -> bytes:
        return hashlib.scrypt(
            secret.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
            dklen=32,
        )

    def issue(
        self,
        *,
        scopes: frozenset[Scope],
        expires_in: timedelta | None,
    ) -> IssuedCredential:
        if not scopes:
            raise ValueError("A credential must have at least one explicit scope.")
        if expires_in is not None and expires_in.total_seconds() <= 0:
            raise ValueError("Credential lifetime must be positive.")
        now = require_utc(self._clock.now())
        secret = secrets.token_urlsafe(32)
        salt = secrets.token_bytes(16)
        digest = self._derive(secret, salt)
        record = CredentialRecord(
            credential_id=self._id_factory(ResourceKind.CREDENTIAL),
            salt=base64.urlsafe_b64encode(salt).decode("ascii"),
            digest=base64.urlsafe_b64encode(digest).decode("ascii"),
            scopes=scopes,
            created_at=now,
            expires_at=now + expires_in if expires_in is not None else None,
        )
        return IssuedCredential(record=record, secret=secret)

    def verify(self, candidate: str, record: CredentialRecord) -> bool:
        now = require_utc(self._clock.now())
        if record.revoked_at is not None:
            return False
        if record.expires_at is not None and now >= record.expires_at:
            return False
        try:
            salt = base64.urlsafe_b64decode(record.salt.encode("ascii"))
            expected = base64.urlsafe_b64decode(record.digest.encode("ascii"))
            actual = self._derive(candidate, salt)
        except (ValueError, UnicodeError):
            return False
        return hmac.compare_digest(actual, expected)


def write_user_only_secret(path: Path, secret: str) -> None:
    """Atomically write a secret without following a destination symlink."""

    if not secret or "\x00" in secret:
        raise ValueError("Secret material must be non-empty text.")
    if path.is_symlink():
        raise ValueError("Secret destination may not be a symbolic link.")
    parent = path.parent
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if parent.is_symlink():
        raise ValueError("Secret directory may not be a symbolic link.")
    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=parent,
        prefix=".credential-",
        text=False,
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(file_descriptor, 0o600)
        payload = secret.encode("utf-8")
        offset = 0
        while offset < len(payload):
            offset += os.write(file_descriptor, payload[offset:])
        os.fsync(file_descriptor)
        os.close(file_descriptor)
        file_descriptor = -1
        temporary_path.replace(path)
        path.chmod(0o600, follow_symlinks=False)
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        temporary_path.unlink(missing_ok=True)
