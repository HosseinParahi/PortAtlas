# PortAtlas System Architecture

## Architectural style

PortAtlas is a native, local-first modular monolith. One Python service, tentatively named portatlasd, owns domain rules, application services, persistence, collectors, scanners, the REST API, dashboard event stream, CLI entrypoints, and MCP adapters. A React application is compiled to static assets and served by the native service.

The modular-monolith boundary is deliberate:

- local installation has one service lifecycle and one data store;
- collectors require native host visibility;
- transactions span registry, conflict, audit, and event-outbox changes;
- CLI, REST, and MCP can share the same application services;
- modules remain independently testable through ports and adapters;
- the architecture can later extract a component only when measured needs justify it.

No module reaches across another module to query its tables or call private implementation functions.

## Logical component view

~~~mermaid
flowchart TB
    subgraph Clients
        WEB[React browser UI]
        CLI[CLI adapter]
        MCP[MCP adapter]
    end

    subgraph NativeService[portatlasd modular monolith]
        API[REST API and browser session]
        EVENTS[SSE delivery]
        APP[Application command and query services]
        REG[Registry]
        CONFLICT[Conflict engine]
        ALLOC[Allocator]
        SCAN[Project discovery and scanners]
        COLLECT[Host and Docker collectors]
        AI[Conditional AI orchestration]
        AUDIT[Audit service]
        OUTBOX[Event outbox]
        REPOS[Repository interfaces]
        CONFIG[Configuration and policy]
    end

    WEB --> API
    WEB --> EVENTS
    CLI --> APP
    MCP --> APP
    API --> APP
    APP --> REG
    APP --> SCAN
    APP --> COLLECT
    APP --> ALLOC
    APP --> CONFLICT
    APP --> CONFIG
    APP -. eligible requests .-> AI
    APP --> AUDIT
    REG --> REPOS
    SCAN --> REPOS
    COLLECT --> REPOS
    ALLOC --> REPOS
    CONFLICT --> REPOS
    AUDIT --> REPOS
    APP --> OUTBOX
    OUTBOX --> EVENTS
    REPOS --> DB[(SQLite or PostgreSQL)]
~~~

## Module responsibilities

| Module | Owns | Does not own |
| --- | --- | --- |
| Domain | Entities, value objects, invariants, state transitions, error vocabulary | I/O, frameworks, database sessions |
| Application | Use-case orchestration, authorization decisions, transaction boundaries, idempotency | SQL details, OS commands, HTTP serialization |
| Registry | Observations, declarations, reservations, leases, desired records, reconciliation | Choosing UI presentation or running processes |
| Collectors | Runtime facts and collection limitations | Project declaration inference or conflict policy |
| Scanners | Approved-root traversal and deterministic evidence extraction | Runtime truth or secret persistence |
| Allocator | Deterministic suggestions and atomic registry leases | OS socket ownership or managed launch in the MVP |
| Conflict engine | Normalized conflict findings from authoritative records and policy | AI prose as a decision source |
| Persistence | Repository implementations, migrations, unit of work, outbox | Domain policy |
| REST API | HTTP validation, authentication, response mapping, OpenAPI | Business rules |
| MCP | Protocol transport, schemas, scope checks, tool/resource/prompt mapping | Duplicated allocation or conflict logic |
| CLI | Argument parsing and human or JSON rendering | Duplicated business logic |
| SSE delivery | Ordered event envelopes, replay cursor, heartbeat | Source-of-truth state |
| AI orchestration | Optional redacted advisory assistance | Mutations, authority, unrestricted tools |
| Audit | Append-only meaningful action records | Raw secret-bearing request capture |

## Runtime and deployment

### MVP native browser mode

~~~mermaid
flowchart LR
    LA[User launch or LaunchAgent] --> DAEMON[portatlasd]
    DAEMON --> STATIC[Compiled React assets]
    DAEMON --> LOOPBACK[127.0.0.1 REST, SSE, and optional MCP HTTP]
    DAEMON --> SQLITE[(User-owned SQLite database)]
    DAEMON --> HOST[Native host inspection]
    DAEMON --> DOCKER[Optional Docker Engine]
    BROWSER[System browser] --> LOOPBACK
~~~

The package contains the native service, CLI entrypoint, static web assets, migrations, built-in scanner definitions, and service catalog. PyInstaller is the leading packaging research path for the first macOS artifact. Signing, LaunchAgent lifecycle, data locations, upgrade, rollback, and uninstall remain packaging contracts. Tauri is reserved for Version 1 and must use the same loopback API rather than embedding domain logic.

### Optional PostgreSQL profile

SQLite is the zero-setup default. PostgreSQL is enabled only by an explicit deployment profile and implements the same repository contracts. It supports compatibility testing and future team/server use. The application never starts a hidden PostgreSQL instance or consumes a port merely to support local mode.

SQLite uses WAL mode on a local filesystem, a busy timeout, short write transactions, and an application-level single-writer discipline. SQLite WAL permits readers and a writer to proceed concurrently but remains a same-host mechanism; see the [official SQLite WAL documentation](https://www.sqlite.org/wal.html). PostgreSQL uses equivalent transactional invariants without database-specific rules leaking into the domain.

## Primary data flows

### Runtime reconciliation

~~~mermaid
sequenceDiagram
    participant S as Scheduler or manual refresh
    participant C as Collector coordinator
    participant H as Host or Docker adapter
    participant R as Reconciliation service
    participant D as Repository unit of work
    participant E as Event outbox

    S->>C: collect(deadline, cancellation)
    C->>H: bounded read-only query
    H-->>C: observations and limitations
    C->>R: normalized snapshot
    R->>D: reconcile by source and identity
    R->>D: recompute affected conflicts
    R->>E: append resource events
    D-->>R: commit atomically
~~~

Each PortObservation records collection time and source. Missing records become stale only after the collector successfully completes a comparable scope. A failed collector never proves that a previously observed listener disappeared.

### Project scan

The scanner resolves a ProjectInstance from an approved ProjectRoot, enumerates allowlisted candidate files under resource budgets, invokes focused parsers, and produces declarations plus DiscoveryEvidence. Reconciliation replaces findings only for parser and source scopes that completed successfully. Unsupported or malformed files generate isolated diagnostics.

### Reservation and lease

The application service authenticates and authorizes the caller, validates ProjectInstance and policy scope, optionally requests a fresh preflight, and opens a database transaction. The allocator derives a deterministic candidate order, checks registry occupancy, inserts a reservation or expiring lease under uniqueness constraints, appends an audit event and outbox event, and commits. It does not bind an OS socket or start a service.

### Browser updates

Domain-affecting transactions append event-outbox rows. The SSE publisher emits schema-versioned events in sequence order. The browser invalidates React Query resources by resource identity and revision. TanStack Table renders paginated inventory; SSE payloads are notifications, not full table snapshots.

### AI assistance

Eligible read-only requests reach the AI orchestrator only when the feature and capability are enabled. A context builder obtains minimum authoritative records through application queries, redacts and delimits them, and passes a strict output schema to the Ollama adapter. A validator rejects malformed, out-of-scope, or ungrounded results. Failure changes no authoritative state.

## Event architecture

PortAtlas uses an in-process domain event dispatcher plus a transactional outbox. The outbox is not a distributed message bus. It provides:

- atomic state-and-event persistence;
- ordered event sequence numbers;
- replay after service restart;
- bounded retention;
- SSE resumption through Last-Event-ID;
- audit-friendly correlation through request IDs.

Every dashboard event contains:

- id: an opaque monotonically ordered event cursor;
- type: a stable event name;
- timestamp: UTC timestamp;
- resource type and resource ID;
- resource revision;
- schema version;
- minimal non-secret payload;
- request ID when caused by a request.

Delivery is at least once. Clients deduplicate by event ID and use REST to refresh state. If the requested cursor has expired, the server emits a resync-required event and closes or continues from the current boundary according to the API contract.

Dashboard SSE at /api/v1/events is separate from the optional SSE framing used by MCP Streamable HTTP. They have different payloads, authentication, and lifecycle.

## Concurrency model

- Blocking subprocess, filesystem, Docker, and model-provider calls run outside the API event loop.
- Background work uses bounded queues, explicit cancellation, and per-task deadlines.
- Registry mutation uses short transactions and database constraints.
- SQLite local mode serializes writes through the unit-of-work coordinator.
- PostgreSQL mode may process concurrent writers but preserves the same command-level invariants.
- Idempotency records prevent duplicate reservation effects.
- Optimistic concurrency revisions protect user-edited settings and policies.
- Collector snapshots are identified by source, scope, start time, and completion state.

## Security architecture

### Authentication and session

On first start, PortAtlas creates a high-entropy token in a user-only location. Browser bootstrap is a one-time exchange that establishes an HttpOnly, SameSite session. CLI and HTTP MCP use separately issued, scoped bearer tokens. Tokens are never returned in normal API resources or logs.

### Authorization

Capabilities are evaluated in application services, not only at transport adapters. Representative scopes are:

- inventory:read;
- projects:read;
- scans:run;
- reservations:write;
- policies:write;
- integrations:manage;
- ai:use.

STDIO MCP runs under the invoking user and an explicitly configured policy profile. It does not imply unrestricted mutation.

### Input boundaries

- Canonical path containment protects project roots.
- File parsers have size, depth, time, and syntax budgets.
- Subprocesses use fixed executable paths or validated lookup plus argument arrays.
- REST and MCP schemas reject unknown or invalid fields.
- Origin and Host validation protect loopback HTTP.
- Every mutation validates scope inside the application layer.
- Docker credentials and socket handles stay inside the Docker adapter.

## Failure isolation

Collectors, scanners, SSE delivery, Docker integration, and AI provider calls are failure-isolated adapters. A module reports typed degradation to the application layer instead of crashing the service. Last-known-good state is preserved with staleness metadata. Transactions either commit the complete intended change, audit row, and outbox row or commit none of them.

The service starts in safe recovery mode if configuration validation or migration fails. Recovery mode exposes authenticated diagnostics and backup guidance but does not run mutations or scans against uncertain state.

## Frontend architecture contract

The React and TypeScript UI uses:

- React Query for server state, caching, invalidation, and request lifecycle;
- TanStack Table for virtualizable, cursor-paginated inventories;
- Radix accessibility primitives wrapped in PortAtlas design tokens;
- a generated or schema-validated API client;
- non-color state indicators and WCAG 2.2 AA interaction targets.

The UI contains no authoritative allocation or conflict rules. It presents application-service results and calls explicit dry-run or mutation endpoints.

## Evolution contracts

The modular monolith defines stable internal ports for future:

- Linux and Windows collectors;
- Tauri shell lifecycle;
- managed launch and post-launch verification;
- structured file patch application;
- plugin manifests and capability isolation;
- local embeddings;
- team/server PostgreSQL operation.

These contracts do not activate those features in the MVP.
