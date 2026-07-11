# PortAtlas System Context

## Document purpose

This document defines the people, external systems, trust boundaries, and operating assumptions around PortAtlas. It is a contract for the first implementation checkpoint, not production code.

## Product boundary

PortAtlas is a local-first developer control center for discovering, explaining, reserving, and coordinating development ports on one workstation. It combines four distinct classes of state:

- observed state from host and Docker runtime collectors;
- declared state from focused, deterministic project parsers;
- reserved and leased state from the PortAtlas registry;
- desired state from reviewable plans.

Those classes remain separate in storage, APIs, user interfaces, and agent tools. A declaration is not proof of a live listener, and a reservation does not prevent an unmanaged process from binding the same port.

## People and clients

| Actor | Goal | Allowed interaction |
| --- | --- | --- |
| Local developer | Understand listeners, projects, conflicts, and exposure; reserve safe ports | Browser UI and CLI; mutation requires explicit action |
| Agent-assisted developer | Let Codex, Claude, or another MCP client preflight and coordinate ports | MCP resources and tools under configured scopes |
| Open-source contributor | Develop, test, package, and extend PortAtlas | Repository toolchains and synthetic fixtures |
| Future team operator | Share policy through an optional server profile | PostgreSQL-backed deployment contract after local MVP |

The MVP is single-user. Multi-user authorization and remote administration are outside the MVP security model.

## External systems

| External system | Data received by PortAtlas | Data sent by PortAtlas | Authority |
| --- | --- | --- | --- |
| Host operating system | Sockets, process identity, executable metadata, ownership, permission gaps | Safe, bounded process and socket queries | Authoritative for the observation time, subject to permissions |
| Docker Engine | Containers, labels, networks, exposed and published ports, health | Read-only API requests in the MVP | Authoritative for Docker state, subject to daemon availability |
| Approved project roots | Repository metadata and supported configuration files | Read-only scans by default | Authoritative only for file contents, not runtime state |
| Browser | User requests, settings, and confirmation actions | Authenticated REST responses and dashboard SSE events | User-controlled client |
| CLI | Commands and scoped bearer credentials | Human or JSON output | User-controlled client |
| MCP clients | Typed requests, client identity, and scoped credentials | Resources, prompts, structured tool results | Client is untrusted at the permission boundary |
| Ollama, when enabled | Provider status, model metadata, generated advisory output | Minimal redacted context and strict schemas | Never authoritative |
| SQLite | Embedded local records and transactions | Local application state | Default persistence mechanism |
| PostgreSQL, optional | Server-profile records and transactions | Same repository contracts as SQLite | Optional compatibility profile |

SQLite projects discovered by PortAtlas are represented as projects with an embedded database dependency. SQLite is never shown as a network listener unless a separate process actually exposes a network service.

## Context diagram

~~~mermaid
flowchart LR
    DEV[Local developer]
    AGENT[Codex, Claude, or MCP client]
    BROWSER[Browser UI]
    CLI[PortAtlas CLI]
    PA[PortAtlas native service]
    HOST[macOS host APIs and processes]
    DOCKER[Docker Engine]
    ROOTS[Approved project roots]
    DB[(SQLite local store)]
    PG[(Optional PostgreSQL profile)]
    OLLAMA[Optional Ollama provider]

    DEV --> BROWSER
    DEV --> CLI
    AGENT -->|stdio or authenticated loopback HTTP| PA
    BROWSER -->|authenticated REST and SSE| PA
    CLI -->|application services| PA
    PA -->|bounded read-only collection| HOST
    PA -->|read-only SDK calls| DOCKER
    PA -->|focused scans inside approved roots| ROOTS
    PA --> DB
    PA -. optional deployment .-> PG
    PA -. redacted advisory requests .-> OLLAMA
~~~

## Trust boundaries

### Local HTTP boundary

The native service binds to loopback by default. All inventory data is treated as sensitive local metadata. Static UI bootstrap and a minimal health response are the only unauthenticated surfaces. A generated high-entropy, user-only token bootstraps the browser into an HttpOnly SameSite session. CLI and HTTP MCP clients use scoped bearer tokens. Origin checks, CSRF protection, and host validation apply to browser and Streamable HTTP traffic.

Non-loopback binding is disabled by default and requires an explicit future security profile. Loopback reduces exposure but does not make authentication optional because malicious local pages can attempt DNS rebinding or cross-origin requests.

### Filesystem boundary

Only user-approved ProjectRoot directories may be scanned. Paths are canonicalized before use. Symlink behavior is explicit per root, and a resolved path must remain inside an approved boundary. Repository content, configuration text, filenames, and embedded instructions are untrusted data.

### Process and command boundary

Collectors use platform APIs or subprocess argument arrays with fixed executables, bounded output, and deadlines. No untrusted string is interpolated into a shell command. PortAtlas never requests sudo automatically and never kills a process in the MVP.

### Docker boundary

Access to the Docker socket is highly privileged even when PortAtlas makes read-only calls. The socket is never forwarded to the browser, MCP client, or AI provider. Docker failures degrade Docker visibility rather than stopping host collection.

### Agent boundary

MCP clients do not inherit mutation rights from repository instructions. Every tool has an explicit read or mutation classification, scope, validation schema, and audit policy. No MVP tool permits arbitrary shell execution, arbitrary file reads, process termination, or silent configuration rewriting.

### Local AI boundary

Ollama is optional, disabled by default, and integrated last only after its security and evaluation gates pass. Every model request passes through context minimization, approved-root enforcement, redaction, untrusted-content delimiters, and an allowlist of read-only operations. Model output remains advisory and cannot create observations, reservations, leases, conflicts, or policy decisions.

## Assurance boundary

PortAtlas provides strong atomicity only inside its own registry:

- concurrent PortAtlas reservation and lease requests are serialized by a database transaction;
- the allocator checks current registry state and records an explained choice;
- a preflight can request a fresh collector reconciliation before allocation.

PortAtlas does not own the operating-system bind operation in the registry-only MVP. An unmanaged process can bind after a scan or ignore a reservation. The product must report that residual race and must never describe unmanaged workflows as conflict-proof.

## Privacy boundary

PortAtlas sends no telemetry. It performs no cloud synchronization and configures no remote AI provider automatically. Environment scanning extracts only recognized port-related values. Secret values, complete environment files, credential-bearing URLs, private keys, cookies, tokens, and unrelated source are excluded from API responses, logs, MCP payloads, model context, exports, and diagnostic bundles.

## Open-source boundary

The release target is Apache-2.0, including its permitted commercial use. PortAtlas does not require payment, a hosted account, or sponsorship for any core capability. Sponsorship may be offered voluntarily as a community-sustainability mechanism and does not influence local behavior, privacy, feature access, or architecture.

## Out-of-context systems

The following are deliberately outside the MVP context:

- process supervision and automatic termination;
- Kubernetes or remote-host discovery;
- database administration;
- firewall management;
- autonomous file patching or launch;
- reverse-proxy and certificate management;
- multi-user server administration;
- cloud telemetry or synchronization;
- Tauri desktop shell, retained as a Version 1 packaging contract.

## Failure posture

| Failure | Product behavior |
| --- | --- |
| Host collector partially denied | Preserve last-known-good records with timestamps; expose permission-limited evidence and degraded status |
| Docker unavailable | Continue native collection and project scanning; mark Docker collector unavailable |
| Scanner encounters malformed or hostile input | Isolate the parser failure, record a safe diagnostic, and continue other files |
| SQLite busy or unavailable | Apply bounded retry where safe; reject mutations without partial state and surface recovery guidance |
| PostgreSQL unavailable in optional profile | Refuse state-changing operations; do not silently fall back to a different database |
| Browser SSE disconnects | Reconnect with Last-Event-ID; refresh affected REST resources when replay is unavailable |
| MCP client loses transport | Abort or safely expire in-flight work; idempotency prevents duplicate registry mutation |
| Ollama fails for any reason | Return a typed optional-feature error; all deterministic capabilities remain operational |

## Locked decisions

- Native Python service plus browser UI is the MVP deployment model.
- The backend is a modular monolith, not microservices.
- SQLite is the embedded default; PostgreSQL is an optional adapter profile.
- ProjectInstance is the operational unit for scans, runtime association, policies, reservations, and conflicts.
- Dashboard updates use Server-Sent Events.
- Allocation is registry-only in the MVP.
- Scanning uses focused deterministic parsers, not broad source-number discovery.
- Optional local AI is conditional, disabled by default, and non-authoritative.
- No telemetry is collected.
- Apache-2.0 permits commercial use; sponsorship is voluntary.
