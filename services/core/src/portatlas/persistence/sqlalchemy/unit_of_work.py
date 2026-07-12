"""Short SQLAlchemy transaction boundary behind the application UoW port."""

from __future__ import annotations

from types import TracebackType

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.persistence.sqlalchemy.repositories import (
    SqlAlchemyProjectInstanceRepository,
    SqlAlchemyProjectRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None
        self._committed = False

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        if self._session is not None:
            raise RuntimeError("UnitOfWork instances cannot be re-entered.")
        self._session = self._session_factory()
        self._committed = False
        self.projects = SqlAlchemyProjectRepository(self._session)
        self.project_instances = SqlAlchemyProjectInstanceRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        session = self._require_session()
        try:
            if exc_type is not None or not self._committed:
                session.rollback()
        finally:
            session.close()
            self._session = None

    async def commit(self) -> None:
        session = self._require_session()
        try:
            session.commit()
            self._committed = True
        except IntegrityError as error:
            session.rollback()
            raise SafeError(
                ErrorCode.PERSISTENCE_INTEGRITY_ERROR,
                "The write violated an authoritative persistence constraint.",
            ) from error
        except OperationalError as error:
            session.rollback()
            code = (
                ErrorCode.PERSISTENCE_BUSY
                if "locked" in str(error).lower()
                else ErrorCode.PERSISTENCE_UNAVAILABLE
            )
            raise SafeError(code, "The persistence transaction could not complete.") from error
        except SQLAlchemyError as error:
            session.rollback()
            raise SafeError(
                ErrorCode.PERSISTENCE_UNAVAILABLE,
                "The persistence transaction could not complete.",
            ) from error

    async def rollback(self) -> None:
        self._require_session().rollback()
        self._committed = False

    def _require_session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork must be entered before use.")
        return self._session
