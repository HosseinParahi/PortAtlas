# ADR 0001: Runtime architecture

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** MVP runtime and process boundaries

## Context

PortAtlas must inspect host listeners, native processes, project files, and Docker while remaining useful without Docker or an internet connection. A browser dashboard, CLI, REST API, and MCP clients all need the same conflict, policy, reservation, and audit behavior. A container-only service cannot reliably inspect native macOS state, while a desktop shell would add signing and sidecar lifecycle work before the core behavior is proven.

The product is local-first, single-user, macOS-first, read-only by default, and cross-platform by contract. It must not turn a local utility into a fleet of microservices.

## Decision

Build a host-native modular monolith, tentatively exposed as the portatlasd service:

- Python 3.13 is the MVP runtime baseline.
- FastAPI provides the versioned loopback HTTP API and static UI delivery.
- Pydantic defines validated boundary contracts.
- SQLAlchemy and Alembic isolate persistence and migrations.
- Typer provides the CLI adapter.
- A React and Vite application is built into static assets served by the native service.
- REST is authoritative for snapshots and commands; ADR 0005 defines the SSE change stream.
- CLI, HTTP, MCP, collectors, scanners, and optional AI are adapters around shared application services. They do not duplicate domain rules.
- Domain, application, persistence, platform, API, MCP, CLI, UI, packaging, and optional-AI modules have explicit dependency directions.
- Operating-system behavior lives behind platform interfaces. macOS is implemented first without macOS logic entering the domain layer.
- The service binds to loopback by default and performs no cloud calls in core operation.

Use uv for Python dependency locking and execution. The repository may be a monorepo, but deploy one local service rather than independent networked backend components.

Tauri is deferred to Version 1. The architecture may add a Tauri shell later, but the shell must remain a client of the same local service.

## Alternatives considered

### Tauri application with a Python sidecar

This offers a polished desktop container but creates sidecar startup, update, code-signing, notarization, and failure-recovery concerns before host discovery is validated.

### Containerized dashboard with a native helper

This provides familiar server packaging but splits installation and lifecycle management. Docker cannot be the only collector and must remain optional.

### Multiple local microservices

Independent services would isolate faults, but they create unnecessary ports, authentication, upgrades, and distributed-state problems for a single-user MVP whose purpose is managing port complexity.

## Consequences

### Positive

- Host visibility and offline operation are first-class.
- Every client uses one deterministic domain implementation.
- The browser UI can ship without a desktop-shell dependency.
- Platform and persistence adapters remain independently testable.
- Later desktop and server modes can reuse the same contracts.

### Costs and risks

- The native service needs careful lifecycle, local authentication, and packaging work.
- Python and Node build toolchains are both required for contributors.
- Module boundaries need automated checks to keep the modular monolith from becoming a large coupled service.
- Browser delivery is less native than a desktop shell in the MVP.

## Verification

- Start the service on a clean supported macOS account with no Docker and no internet.
- Load the built UI from the service and complete read-only inventory workflows.
- Run domain and application tests without FastAPI, Docker, the UI, or Ollama.
- Run collector, persistence, API, CLI, and MCP contract tests independently.
- Confirm the service binds only to configured loopback addresses by default.
- Add architecture tests that reject platform, web, or provider imports from the domain package.

## Revisit triggers

- Packaging research in ADR 0007 shows the native-service distribution cannot meet installation, signing, upgrade, or uninstall requirements.
- A Tauri shell becomes necessary for an approved Version 1 workflow.
- Linux or Windows support exposes a missing platform boundary.
- Team/server mode introduces genuinely independent scaling or fault-isolation requirements.

## Sources

- [Python 3.13 documentation](https://docs.python.org/3.13/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [React documentation](https://react.dev/)
- [uv project documentation](https://docs.astral.sh/uv/concepts/projects/)
