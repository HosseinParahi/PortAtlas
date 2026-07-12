"""TEST-ISO-001: optional-adapter failures leave authoritative state unchanged."""

from __future__ import annotations

import asyncio
import unittest
from datetime import UTC, datetime, timedelta

from portatlas.ai.contracts import (
    AIProvider,
    ProviderHealth,
    ProviderState,
    StructuredCompletionRequest,
)
from portatlas.application.cancellation import CancellationToken
from portatlas.collectors.contracts import (
    CollectionCompleteness,
    CollectionRequest,
    CollectionResult,
    DockerCollector,
)
from portatlas.domain.clock import FrozenClock
from portatlas.domain.errors import ErrorCode
from portatlas.domain.projects import Project
from portatlas.persistence.sqlalchemy.database import (
    create_schema,
    create_session_factory,
    create_sqlite_engine,
)
from portatlas.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


class ActiveCancellationToken:
    @property
    def cancelled(self) -> bool:
        return False


class UnavailableDockerCollector:
    async def collect(
        self,
        request: CollectionRequest,
        cancellation: CancellationToken,
    ) -> CollectionResult:
        return CollectionResult(
            source=request.source,
            completeness=CollectionCompleteness.FAILED,
            observations=(),
            limitations=("integration unavailable",),
            safe_error_code=ErrorCode.COLLECTOR_UNAVAILABLE,
        )


class UnavailableAIProvider:
    async def health(self) -> ProviderHealth:
        return ProviderHealth(ProviderState.UNAVAILABLE, "integration unavailable")

    async def list_models(self) -> list[str]:
        return []

    async def complete_structured(
        self,
        request: StructuredCompletionRequest,
        cancellation: CancellationToken,
    ) -> object:
        raise RuntimeError("synthetic provider failure")


class OptionalDegradationTests(unittest.TestCase):
    def test_docker_and_ai_failures_do_not_mutate_authoritative_projects(self) -> None:
        async def scenario() -> None:
            engine = create_sqlite_engine("sqlite+pysqlite:///:memory:")
            self.addCleanup(engine.dispose)
            create_schema(engine)
            sessions = create_session_factory(engine)
            clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
            project = Project.create(display_name="Authoritative project", clock=clock)
            async with SqlAlchemyUnitOfWork(sessions) as uow:
                uow.projects.add(project)
                await uow.commit()

            collector: DockerCollector = UnavailableDockerCollector()
            provider: AIProvider = UnavailableAIProvider()
            cancellation = ActiveCancellationToken()
            result = await collector.collect(
                CollectionRequest(
                    source="docker",
                    deadline=clock.now() + timedelta(seconds=1),
                ),
                cancellation,
            )
            self.assertEqual(result.completeness, CollectionCompleteness.FAILED)
            self.assertEqual(result.safe_error_code, ErrorCode.COLLECTOR_UNAVAILABLE)
            self.assertEqual((await provider.health()).state, ProviderState.UNAVAILABLE)
            with self.assertRaises(RuntimeError):
                await provider.complete_structured(
                    StructuredCompletionRequest(
                        schema_name="synthetic",
                        context={},
                        maximum_output_bytes=256,
                    ),
                    cancellation,
                )

            async with SqlAlchemyUnitOfWork(sessions) as uow:
                self.assertEqual(uow.projects.list(), [project])

        asyncio.run(scenario())


if __name__ == "__main__":
    unittest.main()
