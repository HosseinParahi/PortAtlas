# PortAtlas Low-Level Design

## Purpose

This document defines implementation-level module boundaries, interfaces, transaction rules, and runtime behavior for the approved modular monolith. It intentionally contains no production implementation.

## Proposed Python package layout

~~~text
services/core/src/portatlas/
  domain/
    identity.py
    ports.py
    projects.py
    registry.py
    policies.py
    conflicts.py
    events.py
    errors.py
  application/
    commands/
    queries/
    dto/
    authorization/
    idempotency/
    unit_of_work.py
  collectors/
    contracts.py
    coordinator.py
    macos/
    docker/
  scanners/
    contracts.py
    discovery.py
    traversal.py
    parsers/
  allocator/
    candidate_order.py
    service.py
  conflicts/
    bind_overlap.py
    rules.py
    service.py
  persistence/
    repositories.py
    sqlalchemy/
    migrations/
  api/
    dependencies.py
    routes/
    schemas/
    sse.py
  mcp/
    server.py
    policy.py
    tools/
    resources/
    prompts/
  cli/
    app.py
    renderers/
  config/
    schema.py
    loader.py
    migration.py
    secrets.py
  ai/
    contracts.py
    orchestrator.py
    context_builder.py
    validation.py
    ollama.py
  security/
    paths.py
    redaction.py
    tokens.py
    origins.py
  observability/
    logging.py
    metrics.py
    diagnostics.py
~~~

The package layout is a direction for the engineering foundation. Each module has a public package interface. Imports point inward: adapters depend on application and domain contracts; domain code depends on no web, SQL, OS, Docker, or model-provider library.

## Shared primitives

### Identifiers

All externally visible identifiers are opaque strings with a resource prefix and random UUID payload, for example prj_, ins_, svc_, obs_, dec_, res_, lea_, con_, evd_, aud_, and air_. Clients must not parse IDs.

### Time

Domain timestamps are timezone-aware UTC instants. Expiration comparisons use a monotonic clock inside a process and persisted UTC instants across restarts. The clock is injected for tests.

### Revisions

Mutable resources have an integer revision starting at one. A successful mutation increments it. REST uses an ETag derived from resource identity and revision; commands accept expected_revision where lost updates matter.

### Port key

PortKey contains:

- protocol: tcp or udp;
- port: integer 1 through 65535;
- address family: ipv4, ipv6, dual, or unknown;
- bind address;
- host or container namespace;
- optional host identity for future remote agents.

Bind overlap is evaluated by the conflict engine, not by string equality.

## Application ports

~~~python
class UnitOfWork(Protocol):
    projects: ProjectRepository
    registry: RegistryRepository
    policies: PolicyRepository
    conflicts: ConflictRepository
    audit: AuditRepository
    events: EventOutboxRepository
    idempotency: IdempotencyRepository

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

class HostCollector(Protocol):
    async def collect(
        self,
        request: CollectionRequest,
        cancellation: CancellationToken,
    ) -> CollectionResult: ...

class ProjectParser(Protocol):
    descriptor: ParserDescriptor

    async def parse(
        self,
        source: SafeSource,
        context: ParseContext,
    ) -> ParseResult: ...

class AIProvider(Protocol):
    async def health(self) -> ProviderHealth: ...
    async def list_models(self) -> list[ModelDescriptor]: ...
    async def complete_structured(
        self,
        request: StructuredCompletionRequest,
        cancellation: CancellationToken,
    ) -> ProviderResponse: ...
~~~

These snippets describe contracts. Concrete signatures may use equivalent typed constructs while preserving behavior.

## Commands and queries

Commands are named by intent and return typed result DTOs:

- RegisterProjectRoot
- UpdateProjectRoot
- RemoveProjectRoot
- StartScan
- CancelScan
- ReconcileCollection
- ReservePort
- AcquirePortLease
- RenewPortLease
- ReleasePortAssignment
- UpdatePortPolicy
- ConfirmDeclaration
- IgnoreConflict
- ConfigureIntegration
- ConfigureAIProvider
- DeleteAIDerivedData

Queries are side-effect free:

- GetSystemStatus
- ListPortInventory
- ListProjects
- GetProjectInstance
- GetProjectPorts
- CheckPortAvailability
- SuggestPort
- PreflightProject
- ListConflicts
- DiagnoseConflict
- ListPolicies
- GetDiscoveryEvidence
- ListRecentChanges

REST, CLI, and MCP construct the same command or query DTO and invoke the same handler. Transport identity is converted to a shared Principal with scopes and integration-client metadata.

## Command handler template

Every state-changing handler follows this order:

1. validate the typed request;
2. authenticate and authorize the Principal;
3. resolve and canonicalize resource scope;
4. claim or read the idempotency key when required;
5. load aggregates and effective policy in one unit of work;
6. enforce expected revision;
7. execute deterministic domain behavior;
8. append AuditEvent and EventOutbox records;
9. persist the idempotent response representation;
10. commit once;
11. publish only after commit.

An exception before commit rolls back all writes. Event publication failure leaves the outbox row pending and does not roll back authoritative state.

## Query handler template

Queries authorize before repository access, apply stable ordering, fetch one more row than requested, construct an opaque cursor from the last sort tuple, and redact fields according to caller scope. Queries never create audit noise for ordinary UI refreshes; security-sensitive reads and integration activity can be sampled or audited by explicit policy.

## Background work

### Scheduler

The scheduler triggers host collection, Docker refresh, project reconciliation, lease expiry, retention cleanup, outbox delivery, and cache maintenance. Each job has:

- a stable job type;
- a non-overlap or coalescing policy;
- deadline and cancellation token;
- bounded input scope;
- attempt metadata;
- structured safe outcome.

The scheduler does not start a second equivalent scan when one can be coalesced.

### Blocking adapter execution

psutil calls, lsof subprocesses, Docker SDK requests, filesystem traversal, parser work, and Ollama HTTP requests execute in bounded worker pools or asynchronous clients appropriate to the adapter. No blocking operation runs on the FastAPI event-loop thread.

### Shutdown

Shutdown stops accepting new mutations, closes SSE and MCP streams with safe signals, cancels eligible background jobs, allows current database transactions a bounded completion window, checkpoints durable state, and expires only leases whose policy requires process-bound cleanup.

## Collector reconciliation algorithm

1. Create CollectionRun with source, scope, started_at, and adapter version.
2. Collect raw records under deadline and output limit.
3. Normalize protocol, addresses, process identity, and container bindings.
4. Record limitations separately from observations.
5. Begin unit of work after a complete result exists.
6. Upsert identities and observations for the completed scope.
7. Mark unseen prior observations stale only if the result scope is complete.
8. Recompute conflicts for affected PortKeys.
9. Append a summarized audit event and resource events.
10. Commit and publish.

A partial result may add verified observations but cannot retire previously verified observations.

## Scan pipeline

1. Resolve ProjectRoot and canonical traversal boundary.
2. Enumerate candidate ProjectInstances.
3. Build a candidate-file list using exact names and patterns.
4. Enforce depth, file count, file size, total byte, and duration budgets.
5. Open files through safe path checks.
6. Invoke the matching parser without executing project code.
7. Redact before logging or persistence.
8. Validate PortDeclaration and DiscoveryEvidence.
9. Reconcile only successfully completed parser-source scopes.
10. Recompute affected conflicts and publish events.

Parser results include parser_id, parser_version, source fingerprint, confidence, safe location, and warnings. Caches are invalidated when the fingerprint, parser version, scan policy, or manifest schema version changes.

## Allocator transaction

For SQLite local mode, the unit of work begins a write transaction before final candidate selection. The adapter may use BEGIN IMMEDIATE to acquire the write reservation predictably. For PostgreSQL, a transaction plus row or advisory locking and unique constraints prevents overlapping active leases. The domain receives an abstract OccupancyView and is unaware of the locking mechanism.

Uniqueness is enforced over the normalized allocation domain. An active lease or reservation that blocks a candidate cannot be inserted twice. Expired leases are excluded only after deterministic expiry evaluation in the same transaction.

## Conflict recomputation

The ConflictEngine receives affected records and an EffectivePortPolicy. It produces a set of ConflictProjection values with stable fingerprints. Persistence:

- inserts new fingerprints;
- updates revision and evidence for continuing findings;
- resolves absent findings only when all required source scopes are fresh;
- preserves suppression history;
- emits events for created, changed, resolved, and reopened transitions.

## REST dependency flow

FastAPI dependencies perform:

- request ID acceptance or generation;
- host and origin validation;
- browser session or bearer authentication;
- CSRF validation for browser mutations;
- Principal construction;
- JSON content and body limits;
- unit-of-work factory injection;
- error mapping.

Route functions remain thin. OpenAPI schemas originate from Pydantic request and response types that mirror application DTOs without exposing persistence models.

## SSE implementation contract

The endpoint reads committed outbox events after the authenticated cursor. It serializes:

~~~text
id: 18442
event: conflict.changed
data: {"schema_version":1,"timestamp":"...","resource":{"type":"conflict","id":"con_...","revision":4},"request_id":"req_...","payload":{"severity":"high"}}
~~~

Heartbeats are SSE comments and contain no data. Connections enforce per-user limits, bounded buffers, and slow-consumer disconnect. Last-Event-ID is parsed as an opaque cursor. An expired cursor yields system.resync_required.

## Authentication implementation contract

- Generate at least 256 bits of entropy for the bootstrap token.
- Store token material in a user-only file or platform credential storage.
- Compare credentials in constant time.
- Exchange the bootstrap token once for an HttpOnly SameSite session.
- Rotate and revoke CLI or MCP bearer tokens by token ID.
- Store only a salted hash of long-lived bearer secrets.
- Attach scopes and optional expiration to each issued token.
- Never log Authorization, Cookie, bootstrap query data, or raw tokens.

Browser bootstrap must not leave the token in history, referrer data, or persistent frontend storage.

## Idempotency

Reservation, lease acquisition, and other repeatable side-effecting requests require an Idempotency-Key for HTTP and an equivalent field for MCP or CLI automation. The record contains principal, operation, scope, canonical request hash, response status, response representation, and expiry. Reusing a key with a different request returns IDEMPOTENCY_KEY_REUSED.

## Observability

Structured logs contain timestamp, level, component, event name, request ID, job ID, and safe resource IDs. They exclude raw environment values, tokens, full command lines, arbitrary file contents, and model prompts. Metrics remain local and have bounded label cardinality. No exporter is enabled by default.

## Test seams

- Fake clock for lease expiry and retention.
- In-memory repository fakes for domain and application unit tests.
- SQLite and PostgreSQL repository contract suites.
- Fixture-backed collector and parser adapters.
- Fake Docker Engine and fake Ollama-compatible server.
- Deterministic event outbox and SSE replay tests.
- Principal and scope matrices for API, CLI, and MCP parity.

## Extension limits

Collector, parser, provider, and packaging interfaces are internal extension seams. Loading third-party code is not part of the MVP. A future plugin host must add signed or trusted manifests, explicit capabilities, isolation, compatibility negotiation, and security review before these interfaces become public.
