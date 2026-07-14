# Test Strategy

Status: **Gate 3 foundation suites accepted on 2026-07-14 for exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](../project/gate-3-evidence.md); Gate 4 runtime-inventory contract proposed with no behavior authorized; later-gate quality contract proposed**

## Objectives

Testing proves deterministic correctness, managed allocation assurance, honest treatment of unmanaged evidence, privacy, accessibility, degradation, and portability of adapter contracts. Core suites must run on a clean development machine with no Docker daemon and no Ollama service.

The Gate 3 disposition accepts only the bounded foundation evidence identified in its sprint brief. It does not claim a runtime inventory, later-gate feature behavior, a completed security review, full `SRS-NFR-009`, packaging acceptance, or release readiness.

## Test pyramid and stable suites

| Test ID | Suite | Scope | Default dependencies | Release role |
|---|---|---|---|---|
| TEST-ARCH-001 | Foundation architecture | Inward dependency direction, adapter isolation, prohibited implementation surfaces | Standard-library source inspection | Every foundation change |
| TEST-ISO-001 | Optional-integration isolation | Docker/provider absence, explicit degradation, and unchanged authoritative state | Synthetic failing adapters; no live services | Every integration-boundary change |
| UT-DOM-001 | Domain unit and property tests | Entities, value objects, revisions, confidence, state transitions | Python standard test process | Every change |
| UT-CFG-001 | Configuration unit tests | Schema version, strict parsing, loopback/origin bounds, secret exclusion, platform-path seams | Temporary files and synthetic paths | Every configuration change |
| UT-COL-001 | Collector unit tests | Normalization, freshness, identity, safe error mapping | Recorded fixtures and fakes | Every change |
| UT-SCN-001 | Scanner unit and fixture tests | Each locked parser, path policy, provenance | Synthetic project trees | Every change |
| UT-ALC-001 | Allocator property tests | Range rules, exclusion, determinism, exhaustion | In-memory repository fake | Every change |
| IT-SQL-001 | SQLite integration | Migrations, transactions, crashes, leases, repository contracts | Temporary SQLite database | Every change |
| IT-PG-001 | PostgreSQL compatibility | Same repository contract and migration semantics | Opt-in PostgreSQL profile | Release candidate |
| IT-DKR-001 | Docker integration | API negotiation, normalization, permissions, degradation | Fake API by default; optional daemon | Release candidate |
| CT-API-001 | REST/SSE contract | Schemas, errors, idempotency, revisions, replay | In-process service | Every change |
| CT-CLI-001 | CLI contract | Version identity, help surface, stable machine output, prohibited commands | In-process CLI runner | Every CLI change |
| CT-MCP-001 | MCP contract | STDIO and HTTP protocol, scopes, copy, cancellation | In-process transports | Every change |
| E2E-CORE-001 | Core browser journey | Onboard, scan fixtures, inspect evidence, reserve, release | Packaged-like local stack; no Docker or AI | Release candidate |
| SEC-T-AUTH-001 | Security suite | Auth, origin, CSRF, permissions, traversal, secrets | Local adversarial fixtures | Every release candidate |
| SEC-T-SECRET-001 | Secret-boundary suite | Redaction canaries across configuration, errors, fixtures, logs, contracts, and diagnostics | Synthetic canaries only | Every security-boundary change |
| PERF-INV-001 | Capacity and latency | 500 repositories, 2,000 declarations, 1,000 observations | Generated deterministic corpus | Performance gate |
| AI-EVAL-SAFE-001 | Optional AI evaluation | Privacy, injection, grounding, schemas, isolation | Fake provider; optional local Ollama profile | AI inclusion gate only |

## Required techniques

- Example-based unit tests for normal and error flows
- Property tests for port ranges, lease transitions, idempotency, pagination, and revision ordering
- Golden and adversarial fixtures for each parser and collector
- Repository contract tests reused by SQLite and PostgreSQL
- Consumer-visible REST, SSE, CLI, and MCP contract tests
- Integration tests for transaction, migration, crash, permission, and degradation behavior
- Browser E2E tests for keyboard, accessibility, stale state, and user-visible copy
- Security and privacy canary testing at every serialization boundary
- Performance tests with fixed data generation, warm/cold distinction, and machine profile
- Manual founder UAT for product truth and real project coverage

## Quality thresholds

- All mandatory tests pass; flaky-test reruns do not convert failure to acceptance.
- Zero authorization bypass, secret canary leakage, symlink escape, forbidden mutation, or corrupting degradation.
- Parser recall is at least 90% on the labeled supported-format corpus; precision and per-parser misses are reported.
- Runtime changes reach the browser within two seconds under normal-load conditions defined in the performance plan.
- At target capacity, the ports table interaction remains within the documented latency budget and exposes no missing rows.
- Every acceptance scenario AC-001 through AC-015 passes its UAT mapping.
- Optional AI can fail or be absent while core state and all core suites remain green.

## Test environments

The default CI-equivalent environment uses temporary directories, synthetic identities, fixture clocks, an ephemeral SQLite database, fake host/Docker/provider adapters, and loopback networking. Separate opt-in profiles cover a live macOS host, Docker, PostgreSQL, and Ollama. Absence of an opt-in profile is reported as not executed, never as a passing integration.

## Proposed Gate 4 runtime-inventory crosswalk

The [Gate 4 sprint brief](../project/gate-4-sprint-brief.md) is **Proposed**. The crosswalk below defines evidence required if the founder accepts that brief; it does not assert implementation or authorize Gate 4 behavior. Core Gate 4 checks must pass without Docker, PostgreSQL, Ollama, Rust, packaging tools, or public-network access. Live profiles must be recorded separately and cannot report an unavailable dependency as passing.

| Evidence area | Existing test or verification ID | Proposed Gate 4 scope | Required profile or boundary | Disposition |
| --- | --- | --- | --- | --- |
| Architecture boundaries | `TEST-ARCH-001` | Enforce inward boundaries for runtime domain, collectors, Docker, persistence, API, CLI, and audit; prohibit scanner, conflict, allocation, Docker-lifecycle, MCP, AI, and packaging behavior. | Standard source/import checks, no optional service | Evidence pending |
| Optional isolation | `TEST-ISO-001` | Prove absent/stopped/denied Docker and collector failure leave host inventory and authoritative state healthy, explicit, and recoverable. | Failing fakes by default; no live Docker required | Evidence pending |
| Domain behavior | `UT-DOM-001` | Prove typed socket/process/container identities, normalization, revisions, timestamp injection, completeness, freshness/staleness, and nullable association seams. | Deterministic fixtures and property cases | Evidence pending |
| Collector behavior | `UT-COL-001` | Prove `psutil`/`lsof -nP` parsing and selection, partial/complete result semantics, safe errors, reconciliation, retry/cancellation bounds, and no absence-based retirement after a partial result. | Recorded synthetic outputs and fakes | Evidence pending |
| SQLite runtime state | `IT-SQL-001` | Prove runtime migrations/repositories, transaction rollback, last-known-good restart recovery, and atomic observation/audit/outbox commits. | Ephemeral SQLite | Evidence pending |
| PostgreSQL compatibility | `IT-PG-001` | Reuse only the applicable runtime repository/migration contract. PostgreSQL remains opt-in and cannot block or replace default SQLite evidence. | Explicit optional PostgreSQL profile | Evidence pending |
| Docker integration | `IT-DKR-001` | Prove API negotiation, running/stopped identity, safe name/image/tag, health, start time, restart policy, networks, internal/exposed/published/interface normalization, safe Compose labels, events, event-loss reconciliation, permissions, restart, and degradation. | Fake engine by default plus at least one documented real local Engine negotiation | Evidence pending |
| API and SSE contract | `CT-API-001` | Prove the bounded authenticated `/api/v1` system/capability, collector/refresh, cursor-paginated observation, and dashboard SSE surface; later resources remain absent. | In-process service, SQLite, no live Docker | Evidence pending |
| CLI contract | `CT-CLI-001` | Prove only `status`, `ports`, and `collectors refresh` in human, JSON, and non-ANSI piped modes with stable safe exits/errors. | In-process CLI/service seam | Evidence pending |
| Local authentication | `SEC-T-AUTH-001` | Prove loopback binding, browser-origin/CSRF/session behavior, bearer scopes/permissions, and unauthorized REST/SSE/refresh rejection for the bounded Gate 4 surface. | In-process local HTTP and CLI credentials; adversarial origins/tokens | Evidence pending |
| Secret boundary | `SEC-T-SECRET-001` | Search seeded canaries across collector/subprocess/Docker input, persistence, REST, SSE, CLI, audit, logs, diagnostics, and Gate 4 evidence artifacts. | Synthetic canaries only; zero matches required | Evidence pending |
| Host verification | `VT-SRS-COL-001` | Verify normalized TCP/UDP IPv4/IPv6 listeners through fixtures and a controlled real Apple-silicon macOS matrix. | Fake and real macOS profiles | Evidence pending |
| Process verification | `VT-SRS-COL-002` | Verify PID plus start time, executable, redacted command, user, working directory, parent, permission limits, bind/interface semantics, and nullable association-ready evidence without project discovery or an `AC-007` claim. | Fixture and real macOS permission/exit/PID-reuse cases | Evidence pending |
| Docker verification | `VT-SRS-COL-003` | Verify optional Docker identity/state, safe name/image/tag, health, start time, restart policy, networks, internal/exposed/published/interface facts, safe Compose labels, and failure behavior without conflict computation. | Fake engine, Docker-absent core, and real negotiation profile | Evidence pending |
| Reconciliation verification | `VT-SRS-COL-004` | Verify only runtime intervals/manual refresh, Docker events, periodic reconciliation, cancellation, last-good/degraded state, restart, and event latency. Filesystem watcher/scan/cache coverage remains Gate 5. | In-process fault profiles plus optional real Docker | Partial Gate 4 evidence pending |
| API verification | `VT-SRS-API-001` | Verify only the bounded Gate 4 API/SSE resources, authentication, safe errors, cursor pagination, revision/event schemas, and drift. | In-process contract profile | Partial Gate 4 evidence pending |
| CLI verification | `VT-SRS-CLI-001` | Verify only the bounded Gate 4 command subset and machine-output/exit contract. | In-process CLI profile | Partial Gate 4 evidence pending |
| Security verification | `VT-SRS-SEC-003` | Exercise applicable Gate 4 origin/token, subprocess, Docker, least-privilege, and resource-boundary attacks without claiming later path/MCP/model coverage. | In-process threat fixtures plus Docker-absent and optional real profiles | Partial Gate 4 evidence pending |
| Offline-core verification | `VT-SRS-SEC-001` | Prove the Gate 4 runtime/API/CLI core with external network disabled and Docker/Ollama absent, including an outbound no-telemetry audit. | Network-disabled core profile | Partial Gate 4 evidence pending |
| Secret verification | `VT-SRS-SEC-002` | Prove zero canary leakage across every implemented Gate 4 persistence/API/SSE/CLI/log/audit/evidence boundary without claiming later UI/MCP/export/AI surfaces. | Synthetic canaries and implemented-surface artifact scan | Partial Gate 4 evidence pending |
| Responsiveness verification | `VT-SRS-NFR-001` | Prove Gate 4 collector/API/SSE latency, event-loop bounds, cancellation, queue limits, runtime debounce, and pagination; scanner and visible-UI portions remain later. | Controlled runtime load and in-process service | Partial Gate 4 evidence pending |
| Runtime-scale verification | `VT-SRS-NFR-002` | Exercise only the 1,000-observation storage/query/reconciliation profile; repository/declaration/browser/founder-UAT portions remain open. | Target-size SQLite runtime dataset | Partial Gate 4 evidence pending |
| Failure-isolation verification | `VT-SRS-NFR-003` | Prove collector/Docker failure, restart reconciliation, runtime migration recovery, and bounded shutdown; watcher/AI/lifecycle portions remain later. | Fault-injection, restart, and migration profiles | Partial Gate 4 evidence pending |
| Engineering-quality verification | `VT-SRS-NFR-006` | Apply format/lint/type/unit/contract/architecture/dependency/documentation checks to every Gate 4 change. | Default aggregate and hosted CI | Evidence pending |
| Platform-isolation verification | `VT-SRS-NFR-007` | Prove macOS implementation behind common collector contracts and explicit unsupported-platform capability behavior; packaging portability remains Gate 9. | Architecture tests, fake platform adapters, real macOS profile | Partial Gate 4 evidence pending |
| Local-observability verification | `VT-SRS-NFR-008` | Prove Gate 4 correlation IDs, structured safe logs, bounded local collector metrics, redaction, and outbound no-telemetry behavior; diagnostic export/UI remains later. | In-process logging/metrics/audit fixtures and outbound audit | Partial Gate 4 evidence pending |
| Audit verification | `VT-SRS-OPS-002` | Prove correlated minimized audit records for Gate 4 reads, refreshes, collector/Docker integration state, results, and failures; later action classes and complete diagnostic interfaces remain open. | Ephemeral SQLite plus correlation/redaction/local-metrics checks | Partial Gate 4 evidence pending |
| Collection latency | `PERF-COL-001` | Require p95 collector-to-committed normalized state at or below 1.5 seconds under the documented runtime normal-load profile. | Controlled macOS listener changes | Evidence pending |
| Event latency | `PERF-SSE-001` | Measure commit-to-test-subscriber invalidation and server-side end-to-end timing; visible-browser completion of `SM-04` remains Gate 7. | In-process authenticated subscriber, 100 controlled changes | Partial Gate 4 evidence pending |
| API paging latency | `PERF-API-001` | Require warm p95 at or below 200 ms for a cursor page of 100 rows at the 1,000-observation runtime profile. | Target-size SQLite runtime dataset | Evidence pending |
| Runtime storage | `PERF-DB-001` | Exercise target-size runtime migration, integrity, and restart only; packaging-budget finalization remains Gate 9. | 1,000-observation runtime storage profile | Partial Gate 4 evidence pending |

The performance IDs and thresholds are defined in the [performance plan](performance-plan.md#stable-benchmarks). Gate 4 advances only the collector-evidence portion of `AC-001`/`UAT-001` and runtime-observation prerequisite of `AC-003`/`UAT-003`; both scenarios complete at Gate 7. Gate 4 makes no acceptance claim for `AC-007`/`UAT-007`. `SM-04` is partial until visible browser timing passes, `SM-08` requires zero canary leakage on every implemented Gate 4 boundary, and `SM-10` is limited to its 1,000-runtime-observation storage/query/reconciliation subprofile.

## Evidence

Each gate records command, revision, environment profile, test counts, failures, duration, and artifact hashes. Screenshots supplement but do not replace assertions. Secret-bearing logs are never attached.
