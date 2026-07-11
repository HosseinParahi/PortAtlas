# PortAtlas Software Requirements Specification

## 1. Purpose

This SRS defines the testable behavior and quality constraints for the PortAtlas MVP. It translates the [BRD](../product/brd.md) and [PRD](../product/prd.md) into stable requirements and provides the canonical component vocabulary used by [Acceptance criteria](acceptance-criteria.md) and the [Traceability matrix](traceability-matrix.md).

This is a requirements baseline, not a statement that any capability is implemented.

## 2. System purpose

PortAtlas is a local-first service and control center that reconciles:

- live TCP/UDP listener observations;
- project configuration declarations;
- persistent reservations;
- atomic short-lived leases;
- desired assignments in reviewable plans; and
- deterministic conflict and policy findings.

It exposes evidence-backed state to a browser UI, CLI, local API/event stream, and MCP clients. Optional local AI may explain or summarize authoritative records but cannot become their source of truth.

## 3. Assurance model

### 3.1 Future managed-launch assurance boundary

A future Version 1 managed launcher could preflight, acquire an atomic lease, inject an approved assignment, launch, verify the actual listener, and release or convert the lease. When every participant honors that complete workflow, it can provide strong conflict prevention. The registry-only MVP does **not** patch source, launch a service, terminate a process, or expose those tools or endpoints; it coordinates reservations and leases among cooperating clients only.

### 3.2 Unmanaged launches

An external terminal, IDE, script, Docker command, or application may ignore the registry. PortAtlas shall detect, warn, explain, recommend, and reconcile, but shall not claim a prevention guarantee for that race. A point-in-time suggestion is not a reservation.

## 4. MVP operating context

- One local OS user on macOS is the planning baseline.
- A native Python service owns collection, scanning, domain rules, persistence, API/events, CLI/MCP adapters, audit, and configuration.
- A React/TypeScript browser UI is served locally by the native service in the baseline packaging option.
- Docker is optional and the Docker adapter is unavailable without degrading native core behavior.
- Embedded SQLite is the accepted default behind SQLAlchemy repositories; PostgreSQL is an optional supported profile with shared compatibility tests.
- Network interfaces bind to loopback by default.
- Ollama and all model capabilities are optional and disabled by default.

Accepted decisions and the smaller set of remaining release inputs are governed by [Assumptions and constraints](assumptions-and-constraints.md).

## 5. Users and external systems

| Actor/system | Interaction |
| --- | --- |
| Local developer | Configures roots/policies, inspects state, diagnoses conflicts, reserves/releases ports, manages integrations and local data |
| MCP-capable coding agent | Reads inventory/evidence, preflights, suggests and reserves or leases under policy; it receives no MVP source-patch, launch, termination, or Docker-lifecycle capability |
| macOS | Supplies process/socket and filesystem metadata subject to permissions |
| Docker Engine/Desktop | Supplies container, Compose, network, health, and published-binding state when available |
| Git and project files | Supply identity and deterministic declaration evidence inside approved roots |
| Ollama | Optionally supplies advisory generated output through a restricted provider interface |
| Package/service manager | Installs and controls the local PortAtlas service and lifecycle |

## 6. Normative state and domain terms

| Term | Definition |
| --- | --- |
| ProjectRoot | User-approved canonical directory and scan policy |
| Project | Stable logical repository or application-family identity |
| ProjectInstance | Concrete checkout, Git worktree, or standalone directory beneath one logical Project; the boundary for scans, runtime association, policy, reservations, and leases |
| Service | Logical runnable component within a ProjectInstance |
| PortObservation | Timestamped runtime socket record with protocol/address/process/container evidence |
| PortDeclaration | Port-related configuration finding with source location, parser, confidence, and host/container semantics |
| PortReservation | Persistent explicit assignment owned by a ProjectInstance/service |
| PortLease | Atomic expiring allocation that coordinates cooperating PortAtlas clients without reserving an operating-system socket |
| PortPolicy | Range, exclusion, category, interface, protocol, reuse, conflict, and lease rules |
| Conflict | Deterministic normalized incompatibility or exposure/policy finding |
| ProcessIdentity | PID plus start time and executable identity; PID alone is insufficient |
| ContainerIdentity | Docker ID/name/image/Compose/network/internal/published binding identity |
| DiscoveryEvidence | Provenance explaining an observation, declaration, association, or finding |
| AuditEvent | Safe record of a meaningful read, mutation, configuration, integration, or agent action |
| AI assistance result | Non-authoritative generated artifact with provider/model/schema/evidence/validation/expiry metadata |

State labels are Observed, Declared, Reserved, Leased, Desired, Conflicted, Stale, Unknown, Ignored, and AI suggested. They shall remain independently queryable and shall not rely on color alone in the UI.

## 7. Architecture component identifiers

These logical component IDs are stable traceability anchors. Their repository placement may change through an ADR, but their responsibilities shall remain explicit.

| ID | Component | Responsibility |
| --- | --- | --- |
| CMP-DOM | Domain and application services | State model, commands/queries, normalization contracts, authority boundaries |
| CMP-COL | Host collector adapter | macOS socket/process observation and future platform contracts |
| CMP-DKR | Docker adapter | Docker/Compose/container/binding collection and events |
| CMP-SCN | Project discovery and scanners | Approved roots, identity, targeted parsers, evidence, confidence, cache/watchers |
| CMP-DB | Persistence adapter | Transactions, migrations, snapshots, repository abstraction, recovery |
| CMP-REG | Policy, reservation, and lease registry | Policy evaluation, suggestions, reservations, atomic leases and expiry |
| CMP-CNF | Conflict engine | Deterministic conflict/exposure classification, severity, explanation, actions |
| CMP-API | REST API and event stream | Versioned local HTTP contracts, validation, pagination, auth/origin protections, updates |
| CMP-CLI | Command-line adapter | Human/JSON commands and stable exit/error contracts |
| CMP-MCP | MCP and client integrations | STDIO/HTTP server, typed tools/resources/prompts, consent and setup workflows |
| CMP-WEB | React web application | Setup, inventory, projects, conflicts, settings, integrations, audit, accessibility |
| CMP-CFG | Configuration services | Versioned local config, import/export, validation, and migration; proposed manifest design remains unpublished and outside the locked MVP parser catalog |
| CMP-AUD | Audit and local observability | Safe audit events, structured logs, local metrics, diagnostics/correlation |
| CMP-SEC | Security and redaction services | Canonical path policy, secret detection/redaction, mutation guard, data minimization |
| CMP-AI | Optional AI orchestrator | Provider abstraction, context construction, read-only tools, schema/evidence validation, retention |
| CMP-OPS | Packaging and lifecycle | Installation, service control, upgrade/rollback, backup/restore, uninstall, release artifacts |

## 8. Functional requirements index

Full requirement records—including rationale, priority, inputs, outputs, preconditions, normal/error flow, security constraints, acceptance, tests, and component—are normative in [Functional requirements](functional-requirements.md).

| Range | Capability | MoSCoW baseline |
| --- | --- | --- |
| SRS-COL-001–SRS-COL-004 | Runtime host/Docker inventory and reconciliation | Must |
| SRS-SCN-001–SRS-SCN-004 | Approved roots, project identity, scanners, evidence and secret safety | Must |
| SRS-REG-001–SRS-REG-002 | Policies, suggestions, and persistent reservations | Must |
| SRS-ALC-001 | Atomic short-lived leases | Must |
| SRS-CNF-001 | Deterministic conflicts and exposure findings | Must |
| SRS-UI-001–SRS-UI-004 | Setup, main UI, detail experiences, search/config/demo | Must |
| SRS-API-001 | Versioned REST API and event stream | Must |
| SRS-CLI-001 | Command-line interface | Must |
| SRS-MCP-001–SRS-MCP-002 | MCP transports, capabilities, agent/client workflow | Must |
| SRS-AI-001–SRS-AI-003 | Optional local AI connection, read-only uses, safety/failure behavior | Should; conditional MVP |
| SRS-OPS-001–SRS-OPS-003 | Packaging lifecycle, audit, configuration lifecycle | Must |

## 9. Non-functional requirements index

Full records are normative in [Non-functional requirements](non-functional-requirements.md).

| Range | Quality | Baseline |
| --- | --- | --- |
| SRS-SEC-001–SRS-SEC-003 | Local privacy, secret safety, least privilege and attack controls | Must |
| SRS-NFR-001–SRS-NFR-002 | Responsiveness and scale | Must |
| SRS-NFR-003–SRS-NFR-004 | Failure recovery and transactional integrity | Must |
| SRS-NFR-005 | Accessibility | Must |
| SRS-NFR-006–SRS-NFR-007 | Maintainability and portability | Must |
| SRS-NFR-008 | Local observability and no telemetry by default | Must |
| SRS-AI-004 | AI independence and bounded resources | Must if AI ships; core independence always Must |
| SRS-OPS-004 | Installability and lifecycle quality | Must |
| SRS-NFR-009 | Open-source release quality | Must |
| SRS-SCN-005 | Supported parser detection accuracy | Must |

## 10. External interface requirements

### 10.1 Browser UI

The UI shall implement the information model in [Information architecture](../product/information-architecture.md), the primary flows in [Wireframes](../product/wireframes.md), and accessibility requirements in `SRS-NFR-005`. It shall distinguish authoritative, heuristic, generated, stale, and degraded state.

### 10.2 REST API and event stream

The local API shall be explicitly versioned under `/api/v1`, generate OpenAPI from backend definitions, validate a generated or schema-checked TypeScript client, use cursor pagination for large collections, stable machine-readable errors, request IDs, idempotency where applicable, optimistic concurrency, dry-run semantics for supported previews, loopback binding, local mutation authentication, and deployment-appropriate CSRF/origin defenses. Browser updates use schema-versioned Server-Sent Events. No MVP endpoint patches source, launches a service, terminates a process, or mutates Docker lifecycle.

### 10.3 CLI

The CLI shall offer human and JSON modes, stable exit codes, non-ANSI piped output, clear permission/degradation errors, and behavior consistent with application/API/MCP services.

### 10.4 MCP

MCP shall support STDIO and streamable HTTP on loopback with bearer authentication for HTTP, structured errors, typed schemas, explicit consent, concise instructions, resources/tools/prompts, and cancellation/progress where useful. Client-specific instructions shall remain thin adapters.

### 10.5 Optional AI provider

The provider interface shall support health/version/model/capability discovery, chat/structured output, optional future embeddings, timeout/cancellation/keep-alive, bounded context/output, and isolated calls. It shall not assume Ollama or a model is installed and shall never install/download/activate one without approval.

## 11. Data requirements

- Persist authoritative and advisory records separately with timestamps and provenance.
- Use transaction or equivalent locking for lease uniqueness.
- Version configuration, API, event, and migration schemas; keep the proposed manifest schema design-only until its name and scope gates close.
- Do not persist secret values or complete environment content.
- Do not identify a process by PID alone, a logical Project only by a path, or collapse separate ProjectInstance checkout/worktree records.
- Retain last-known-good evidence with explicit staleness.
- Store raw AI prompts/conversations off by default; store safe metadata and saved artifacts only under policy.
- Exclude AI-derived data from export unless selected and permit complete purge.

## 12. Error model

All interfaces shall map domain errors to stable codes and safe messages. At minimum distinguish validation, not found, permission/capability limited, conflict, unavailable, stale precondition, lease expired, concurrency collision, path outside scope, authentication/authorization, provider/model, timeout/cancellation, schema/evidence failure, and recoverable persistence/configuration errors. Errors shall not include secrets, full environment lines, unsafe process arguments, or hidden model reasoning.

## 13. Verification model

- Each requirement maps to a stable verification ID in [Acceptance criteria](acceptance-criteria.md).
- The fifteen founder scenarios are `AC-001` through `AC-015`, with `UAT-001` through `UAT-015`.
- [Traceability](traceability-matrix.md) connects every scenario to a business objective, product story, SRS requirement, architecture component, test/UAT identifier, and delivery gate.
- A feature is not complete until requirement links, review, type/lint, relevant unit/integration/E2E tests, security/accessibility review, documentation, safe errors/logs, migration impact, and recorded verification evidence are present.

## 14. Approval boundary

This SRS supports Gate 2 review. Accepted ADRs settle runtime architecture, persistence, `Project`/`ProjectInstance` identity, SSE, local authentication, MCP transports, the registry-only MVP mutation boundary, no telemetry, and Apache-2.0 licensing. Packaging implementation evidence, public-name and namespace clearance, exact dependency patches, and conditional AI inclusion remain gated. No production implementation begins until the founder approves Gate 2.
