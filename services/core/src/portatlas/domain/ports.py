"""Port identity and deliberately distinct state vocabularies."""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from enum import StrEnum

_MAX_PORT = 65_535
_IPV4_VERSION = 4
_IPV6_VERSION = 6


class TransportProtocol(StrEnum):
    TCP = "tcp"
    UDP = "udp"


class AddressFamily(StrEnum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DUAL = "dual"
    UNKNOWN = "unknown"


class NamespaceKind(StrEnum):
    HOST = "host"
    CONTAINER = "container"


class BindScope(StrEnum):
    LOOPBACK = "loopback"
    ANY = "any"
    SPECIFIC = "specific"
    UNKNOWN = "unknown"


class PortState(StrEnum):
    """Evidence and desired-state vocabulary, never registry assurance."""

    OBSERVED = "observed"
    DECLARED = "declared"
    DESIRED = "desired"
    CONFLICTED = "conflicted"
    STALE = "stale"
    IGNORED = "ignored"
    UNKNOWN = "unknown"


class AssignmentState(StrEnum):
    """Cooperative registry state with stronger managed assurance."""

    RESERVED = "reserved"
    LEASED = "leased"
    RENEWED = "renewed"
    RELEASED = "released"
    EXPIRED = "expired"
    VIOLATED = "violated"


_NAMESPACE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


@dataclass(frozen=True, slots=True)
class PortNamespace:
    kind: NamespaceKind
    identity: str | None = None

    def __post_init__(self) -> None:
        if (
            self.kind is NamespaceKind.HOST
            and self.identity not in (None, "local")
            and not _NAMESPACE_ID.fullmatch(self.identity)
        ):
            raise ValueError("Host namespace identity has an unsafe shape.")
        if self.kind is NamespaceKind.CONTAINER and (
            self.identity is None or not _NAMESPACE_ID.fullmatch(self.identity)
        ):
            raise ValueError("Container namespace requires a safe adapter identity.")

    @classmethod
    def host(cls, identity: str | None = None) -> PortNamespace:
        return cls(NamespaceKind.HOST, identity)

    @classmethod
    def container(cls, identity: str) -> PortNamespace:
        return cls(NamespaceKind.CONTAINER, identity)


@dataclass(frozen=True, slots=True)
class PortKey:
    protocol: TransportProtocol
    port: int
    address_family: AddressFamily = AddressFamily.UNKNOWN
    bind_address: str | None = None
    namespace: PortNamespace = PortNamespace(kind=NamespaceKind.HOST)
    host_identity: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.port, bool) or not isinstance(self.port, int):
            raise TypeError("Port must be an integer.")
        if not 1 <= self.port <= _MAX_PORT:
            raise ValueError("Port must be between 1 and 65535.")
        if self.host_identity is not None and not _NAMESPACE_ID.fullmatch(self.host_identity):
            raise ValueError("Host identity has an unsafe shape.")
        parsed = self._parsed_bind_address()
        if parsed is None:
            return
        if self.address_family is AddressFamily.IPV4 and parsed.version != _IPV4_VERSION:
            raise ValueError("Bind address does not match the IPv4 address family.")
        if self.address_family is AddressFamily.IPV6 and parsed.version != _IPV6_VERSION:
            raise ValueError("Bind address does not match the IPv6 address family.")

    def _parsed_bind_address(self) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
        if self.bind_address is None:
            return None
        try:
            return ipaddress.ip_address(self.bind_address)
        except ValueError as error:
            raise ValueError("Bind address must be an IPv4 or IPv6 address.") from error

    @property
    def bind_scope(self) -> BindScope:
        address = self._parsed_bind_address()
        if address is None:
            return BindScope.UNKNOWN
        if address.is_loopback:
            return BindScope.LOOPBACK
        if address.is_unspecified:
            return BindScope.ANY
        return BindScope.SPECIFIC
