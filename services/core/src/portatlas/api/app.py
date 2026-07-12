"""FastAPI application factory with minimal liveness and protected readiness."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Literal

from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from portatlas import __version__
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId, ResourceKind


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["ok"]
    service: Literal["portatlas-core"]
    version: str
    schema_version: Literal[1]


class ReadinessReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["ready", "degraded"]
    components: dict[str, Literal["ready", "degraded", "unavailable"]]
    schema_version: Literal[1]

    @classmethod
    def ready(
        cls,
        components: Mapping[str, Literal["ready", "degraded", "unavailable"]],
    ) -> ReadinessReport:
        return cls(status="ready", components=dict(components), schema_version=1)


class CanonicalError(BaseModel):
    """OpenAPI representation of the transport-neutral documented error."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str
    message: str
    retryable: bool
    request_id: str
    details: dict[str, object]


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    error: CanonicalError


ReadinessProbe = Callable[[], ReadinessReport | Awaitable[ReadinessReport]]
BearerTokenVerifier = Callable[[str], bool | Awaitable[bool]]


_ERROR_STATUS: dict[ErrorCode, int] = {
    ErrorCode.REQUEST_INVALID: 422,
    ErrorCode.AUTHENTICATION_REQUIRED: 401,
    ErrorCode.AUTHENTICATION_INVALID: 401,
    ErrorCode.AUTHORIZATION_DENIED: 403,
    ErrorCode.RESOURCE_NOT_FOUND: 404,
    ErrorCode.RESOURCE_REVISION_CONFLICT: 412,
    ErrorCode.PORT_ALREADY_ALLOCATED: 409,
    ErrorCode.PERSISTENCE_BUSY: 503,
    ErrorCode.PERSISTENCE_UNAVAILABLE: 503,
    ErrorCode.INTERNAL_ERROR: 500,
}


async def _default_readiness_probe() -> ReadinessReport:
    return ReadinessReport(
        status="degraded",
        components={"foundation": "unavailable"},
        schema_version=1,
    )


async def _deny_all_tokens(_token: str) -> bool:
    return False


async def _await_if_needed[T](value: T | Awaitable[T]) -> T:
    if inspect.isawaitable(value):
        return await value
    return value


def _request_id(candidate: str | None) -> str:
    if candidate is not None:
        try:
            return str(OpaqueId.parse(candidate, expected_kind=ResourceKind.REQUEST))
        except ValueError:
            pass
    return str(OpaqueId.new(ResourceKind.REQUEST))


def create_app(
    *,
    readiness_probe: ReadinessProbe | None = None,
    bearer_token_verifier: BearerTokenVerifier | None = None,
) -> FastAPI:
    """Create an adapter with dependencies supplied by the composition root."""

    probe = readiness_probe or _default_readiness_probe
    verify_token = bearer_token_verifier or _deny_all_tokens
    app = FastAPI(
        title="PortAtlas (working title) Core API",
        version=__version__,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/v1/openapi.json",
    )

    @app.middleware("http")
    async def attach_request_id(request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.request_id = _request_id(request.headers.get("x-request-id"))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response

    @app.exception_handler(SafeError)
    async def handle_safe_error(request: Request, error: SafeError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", _request_id(None))
        return JSONResponse(
            status_code=_ERROR_STATUS.get(error.code, 400),
            content={"error": error.as_dict(request_id=request_id)},
            headers={"X-Request-ID": request_id},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, _error: RequestValidationError
    ) -> JSONResponse:
        safe_error = SafeError(
            ErrorCode.REQUEST_INVALID,
            "The request does not match the accepted schema.",
        )
        return await handle_safe_error(request, safe_error)

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, _error: Exception) -> JSONResponse:
        safe_error = SafeError(
            ErrorCode.INTERNAL_ERROR,
            "The request could not be completed; use the request ID for support.",
        )
        return await handle_safe_error(request, safe_error)

    @app.get(
        "/api/v1/health",
        response_model=HealthResponse,
        operation_id="getHealth",
        tags=["system"],
        responses={500: {"model": ErrorEnvelope}},
    )
    async def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service="portatlas-core",
            version=__version__,
            schema_version=1,
        )

    @app.get(
        "/api/v1/ready",
        response_model=ReadinessReport,
        operation_id="getReadiness",
        tags=["system"],
        responses={
            401: {"model": ErrorEnvelope},
            422: {"model": ErrorEnvelope},
            503: {"model": ReadinessReport | ErrorEnvelope},
        },
    )
    async def readiness(authorization: str | None = Header(default=None)) -> object:
        if authorization is None:
            raise SafeError(
                ErrorCode.AUTHENTICATION_REQUIRED,
                "Authentication is required for readiness details.",
            )
        scheme, separator, credential = authorization.partition(" ")
        if separator != " " or scheme.lower() != "bearer" or not credential:
            raise SafeError(
                ErrorCode.AUTHENTICATION_INVALID,
                "The supplied authentication credential is invalid.",
            )
        accepted = await _await_if_needed(verify_token(credential))
        if not accepted:
            raise SafeError(
                ErrorCode.AUTHENTICATION_INVALID,
                "The supplied authentication credential is invalid.",
            )
        try:
            report = await _await_if_needed(probe())
        except SafeError:
            raise
        except Exception as error:
            raise SafeError(
                ErrorCode.PERSISTENCE_UNAVAILABLE,
                "Readiness could not be established.",
            ) from error
        if report.status == "degraded":
            return JSONResponse(status_code=503, content=report.model_dump(mode="json"))
        return report

    return app
