# PortAtlas High-Level Design

## Design intent

This high-level design translates the approved architecture into subsystems, public contracts, workflows, and quality boundaries. The first implementation remains a native modular monolith with a browser UI. Future capabilities are represented as interfaces only where they prevent an incompatible MVP design.

## System decomposition

~~~mermaid
flowchart LR
    subgraph Presentation
        UI[React UI]
        REST[REST API]
        SSE[SSE endpoint]
        CLI[CLI]
        MCP[MCP server]
    end

    subgraph UseCases[Application use cases]
        QUERY[Inventory and project queries]
        SCANCMD[Scan commands]
        REGCMD[Reservation and lease commands]
        POLICY[Policy commands]
        DIAG[Preflight and diagnosis]
        AIUC[Conditional AI use cases]
    end

    subgraph Core
        DOMAIN[Domain model]
        REG[Registry]
        ALLOC[Allocator]
        CE[Conflict engine]
    end

    subgraph Adapters
        HOST[macOS collector]
        LSOF[lsof fallback]
        DK[Docker SDK]
        PARSERS[Focused parsers]
        SQL[SQLAlchemy repositories]
        OLLAMA[Ollama provider]
    end

    UI --> REST
    UI --> SSE
    REST --> UseCases
    CLI --> UseCases
    MCP --> UseCases
    UseCases --> Core
    UseCases --> Adapters
    Core --> SQL
~~~

## Subsystem contracts

### Identity and project catalog

Project is the logical application or repository family. ProjectInstance is the concrete checkout, worktree, or standalone directory on this machine. ProjectInstance is the operational unit for:

- scan status and evidence;
- service membership;
- runtime association;
- policy overrides;
- declarations, reservations, leases, and conflicts;
- audit and event resource identity.

Two worktrees can therefore run simultaneously without being collapsed into one path-based project. A stable generated ID survives path changes when repository and filesystem evidence allow reconciliation. Absolute path alone is never the identity.

### Collector subsystem

Collector adapters return normalized snapshots and explicit limitations. The macOS primary adapter uses psutil where it is reliable. A tested lsof -nP parser is the bounded fallback for missing process or socket relationships. The Docker adapter uses the supported Docker SDK and negotiates the Engine API version.

Collectors are read-only. They never terminate processes, change Docker state, or request elevation. A successful snapshot may retire prior observations in the same scope; a failed or partial snapshot may only mark uncertainty.

### Scanner subsystem

The scanner traverses only approved roots and invokes a focused catalog of deterministic parsers. Parser inputs and outputs are typed. Every declaration links to DiscoveryEvidence with parser version, source location, confidence, and safe excerpt metadata.

Broad numeric-literal scanning, arbitrary code execution, and importing project modules are excluded. Parser additions require fixtures for valid, malformed, oversized, secret-bearing, and adversarial inputs.

### Registry subsystem

The registry persists observed, declared, reserved, leased, and desired records separately. It provides normalized queries and reconciliation, but it does not infer that one class of state proves another.

Registry commands use a unit of work that atomically writes domain state, an AuditEvent, and an event-outbox row. Registry queries are side-effect free.

### Allocator subsystem

The allocator produces explainable, deterministic candidates and transaction-safe reservations or leases. It considers protocol, bind scope, ProjectInstance, service category, policies, observations, reservations, active leases, forbidden ranges, and configured ephemeral ranges.

The registry-only MVP does not bind sockets, inject environment variables, patch files, or launch services. A suggestion is advisory; a committed lease only excludes cooperating PortAtlas clients. The response always states the unmanaged-process race.

### Conflict subsystem

The conflict engine is deterministic and incremental. It evaluates affected records against normalized bind-overlap rules and policy. Findings use stable machine codes, evidence references, severity, safe-action classification, suppression with reason and expiry, and revision.

AI may render an additional explanation after the deterministic finding exists. It cannot create or dismiss a conflict.

### Configuration subsystem

Configuration is versioned, validated, migratable, and writable through UI or CLI. Secrets are stored separately from the exportable configuration. Project roots, scan policies, collector schedules, ranges, retention, integrations, and optional AI settings are configurable without source edits.

Optimistic concurrency prevents lost settings updates. Invalid configuration starts a safe recovery path and does not silently apply partial defaults.

### Presentation adapters

REST, CLI, and MCP call the same application commands and queries. They map transport concerns into shared request types and map domain errors into the stable error model. No adapter implements its own allocation, conflict, path, or redaction logic.

### Event delivery

The dashboard event endpoint is SSE. Each event includes an ID, type, timestamp, resource identity, resource revision, schema version, and minimum payload. React Query uses events as invalidation hints and refetches authoritative REST resources.

### Conditional AI subsystem

Local AI is last in implementation order and ships in the MVP only if its security, privacy, evaluation, and failure-isolation gates pass. It is disabled by default. Ollama is the first adapter behind a provider interface. The AI subsystem receives read-only application queries only, never repository-wide access or mutation tools.

## Core workflows

### Find a port owner

1. A collector coordinator requests a bounded host and Docker snapshot.
2. Adapters return observations plus limitations.
3. Reconciliation upserts ProcessIdentity, ContainerIdentity, and PortObservation records.
4. The conflict engine evaluates affected keys.
5. The transaction appends audit and outbox events.
6. The UI or client queries the observation with evidence and last-seen time.

### Discover project declarations

1. A user approves a ProjectRoot and previews scope.
2. Discovery resolves projects and ProjectInstances.
3. Candidate selection applies include, exclude, depth, symlink, size, and count budgets.
4. Focused parsers return declarations and evidence.
5. Secret filtering discards unrelated values before persistence.
6. Reconciliation updates completed parser scopes and affected conflicts.

### Reserve or lease a port

~~~mermaid
sequenceDiagram
    participant C as UI, CLI, or MCP
    participant A as Application service
    participant P as Policy service
    participant L as Allocator
    participant U as Unit of work

    C->>A: reserve(instance, service, constraints, idempotency key)
    A->>A: authenticate and authorize
    A->>P: resolve effective policy
    P-->>A: ranges and exclusions
    A->>U: begin transaction
    A->>L: choose deterministic candidate
    L->>U: query and lock registry occupancy
    L->>U: insert reservation or lease
    A->>U: append audit and outbox
    U-->>A: commit
    A-->>C: assignment, rationale, revision, race warning
~~~

### Diagnose a conflict

The application retrieves the deterministic Conflict, affected records, evidence, current policy, and allocator alternatives. It returns a concise explanation and safe actions. An optional AI explanation can be requested separately and is labeled generated, validated, and non-authoritative.

## Data ownership

| Aggregate or record | Owning module | Write path |
| --- | --- | --- |
| ProjectRoot, Project, ProjectInstance, Service | Project catalog | Registration and discovery commands |
| ProcessIdentity, ContainerIdentity, PortObservation | Collector registry | Reconciliation only |
| PortDeclaration, DiscoveryEvidence | Scanner registry | Scan reconciliation or explicit confirmation |
| PortReservation, PortLease | Registry and allocator | Authorized transactional commands |
| PortPolicy | Configuration and policy | Revision-checked settings command |
| Conflict | Conflict engine | Deterministic recomputation |
| AuditEvent | Audit | Append in command unit of work |
| EventOutbox | Event delivery | Append in command unit of work |
| AIProviderProfile | AI configuration | Explicit user settings |
| AIAssistanceResult, AIContextRecord | AI orchestration | Validated optional assistance workflow |

## Persistence design

SQLAlchemy repository interfaces isolate persistence. Alembic migrations cover both supported adapters. The shared schema uses portable scalar types and explicit constraints. Database-specific optimization is allowed behind adapters only after compatibility tests.

SQLite local mode:

- user-owned database file on a local filesystem;
- WAL and foreign keys enabled;
- short transactions and bounded busy handling;
- serialized application writes;
- recoverable backups before migration.

PostgreSQL profile:

- explicit connection configuration and secret separation;
- transactional row locking or constraints for lease races;
- identical domain semantics;
- no automatic fallback to SQLite after connection loss.

## API and event contracts

REST lives under /api/v1. Collection endpoints use cursor pagination. Mutation endpoints support request IDs, idempotency where repetition can duplicate state, optimistic concurrency through revision preconditions, and dry-run where the action proposes a change. Normal responses never contain secrets.

The SSE event endpoint supports Last-Event-ID and bounded replay. Delivery is at least once. An event is not an authorization bypass: a connection receives only events permitted by its authenticated session.

## MCP contract

MCP supports:

- stdio for a client-spawned local process;
- authenticated Streamable HTTP on loopback;
- the stable 2025-11-25 MCP specification;
- tools, resources, prompts, progress, and cancellation where supported;
- Origin validation and bearer scopes for HTTP.

Legacy HTTP+SSE is not an MVP transport. The MCP adapter exposes no process-kill, arbitrary shell, arbitrary file-read, or silent file-edit capability.

## Frontend high-level design

React Query owns server-state lifecycles and invalidation. TanStack Table consumes cursor-paginated data. Radix primitives provide accessible interaction foundations. PortAtlas tokens provide color, typography, spacing, focus, and reduced-motion behavior. State badges combine text and icons rather than color alone.

The UI is resilient to collector and AI degradation. A disconnected SSE stream does not erase cached data; it marks freshness and retries before requesting a full resynchronization.

## Quality attributes

### Performance

- API event loop remains free of blocking scans and subprocess work.
- Traversal and parsing use bounded concurrency.
- Large collections are cursor paginated.
- Scan caches include source fingerprint and parser version.
- SSE events carry invalidation-sized payloads.

### Reliability

- Last-known-good records preserve timestamps and source status.
- Background tasks are cancellable and shut down cleanly.
- Database mutations are atomic.
- Idempotency guards retryable commands.
- Migration failure enters recovery mode.

### Security and privacy

- Loopback bind, authentication, origin checks, and CSRF defenses are defaults.
- Scan roots and canonical containment are mandatory.
- No secret-bearing environment values are persisted.
- No telemetry is emitted.
- Model context is minimized and redacted.

### Maintainability

- Domain and application code are framework-independent.
- Every adapter is replaceable through a typed port.
- Parser and collector fixtures pin external-format behavior.
- REST, CLI, and MCP share contracts and error codes.

## Failure matrix

| Boundary | Detection | Containment | Client-visible result |
| --- | --- | --- | --- |
| Host permissions | Adapter limitation record | Keep successful partial facts separate | Degraded collector with permission guidance |
| lsof format change | Parser contract failure | Do not replace last-known-good scope | Collector parse error and stale timestamp |
| Docker daemon absent | SDK connection error | Disable only Docker refresh | Docker unavailable; native inventory remains |
| Malformed project file | Focused parser error | Skip file, continue scan | File-scoped safe diagnostic |
| Database contention | Adapter timeout | Roll back complete command | Retryable persistence error |
| Duplicate reservation retry | Idempotency record | Return original result | Same successful representation |
| SSE gap | Expired event cursor | Require REST resync | Resync-required event |
| MCP invalid scope | Application authorization | Execute no use case | Structured permission error |
| Ollama timeout or invalid JSON | Provider or validator | Persist no authoritative state | Optional AI unavailable or invalid-output error |

## Deferred contracts

Version 1 may add Tauri packaging, managed launch, safe patch application, richer health checks, embeddings, Linux, Windows, and plugin loading. Their ports may be defined now, but their adapters and user-visible promises are not part of the registry-only MVP.
