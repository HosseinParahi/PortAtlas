# PortAtlas Requirements Traceability Matrix

## Purpose and identifier sources

This first-checkpoint matrix traces each founder acceptance scenario through the business, product, software, architecture, verification, and release-gate layers.

| Identifier | Canonical source |
| --- | --- |
| `BO-*` | [BRD business objectives](../product/brd.md#5-business-objectives) |
| `PF-*` | [PRD feature catalog](../product/prd.md#6-feature-definitions) |
| `US-*` | [Product backlog](../product/backlog.md) |
| `FR-*`, `NFR-*` | [Functional requirements](functional-requirements.md) and [Non-functional requirements](non-functional-requirements.md) |
| `CMP-*` | [SRS architecture component identifiers](srs.md#7-architecture-component-identifiers) |
| `AC-*` | [Acceptance criteria](acceptance-criteria.md#initial-acceptance-scenarios) |
| `UAT-*` | `docs/testing/uat-plan.md` |
| `G3-*` | [Gate 3 sprint brief](../project/gate-3-sprint-brief.md#evidence-bound-work-items) |
| `G4-*` | [Proposed Gate 4 sprint brief](../project/gate-4-sprint-brief.md#evidence-bound-work-items) |
| Gate N | [Product roadmap](../product/roadmap.md#phase-and-gate-map) |

For Gate 3, `G3-*` was the bounded engineering work item beneath the stable `US-*` plan item. Later issue/PR identifiers shall be appended without replacing either stable upstream identifier. A foundation seam does not satisfy the later feature requirement whose interface it anticipates.

## End-to-end scenario matrix

Every row contains the required BRD objective, PRD feature/story, SRS requirement, architecture component, stable UAT, and final acceptance gate.

| Acceptance scenario | BRD ID | PRD feature/story ID | SRS ID | Architecture component ID | Test/UAT ID | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| `AC-001` Find owner | `BO-01` | `PF-001`, `PF-006`, `PF-007`; `US-020`, `US-021`, `US-023`, `US-061` | `SRS-COL-001`, `SRS-COL-002`, `SRS-COL-004`, `SRS-UI-002`, `SRS-API-001`; `SRS-NFR-001`, `SRS-NFR-002`, `SRS-NFR-005` | `CMP-COL`, `CMP-DOM`, `CMP-API`, `CMP-WEB` | `UAT-001` | Gate 7 |
| `AC-002` Future declared conflict | `BO-02` | `PF-003`, `PF-004`, `PF-005`, `PF-006`; `US-032`, `US-041`, `US-043`, `US-063` | `SRS-SCN-003`, `SRS-REG-002`, `SRS-CNF-001`, `SRS-UI-003`; `SRS-SCN-005` | `CMP-SCN`, `CMP-REG`, `CMP-CNF`, `CMP-WEB` | `UAT-002` | Gate 7 |
| `AC-003` Docker/native conflict | `BO-02` | `PF-002`, `PF-003`, `PF-005`, `PF-006`; `US-022`, `US-032`, `US-043`, `US-063` | `SRS-COL-003`, `SRS-SCN-003`, `SRS-CNF-001`, `SRS-UI-003`; `SRS-NFR-007`, `SRS-SCN-005` | `CMP-DKR`, `CMP-SCN`, `CMP-CNF`, `CMP-WEB` | `UAT-003` | Gate 7 |
| `AC-004` Agent safe port | `BO-03`, `BO-06` | `PF-004`, `PF-008`; `US-041`, `US-042`, `US-071`, `US-072` | `SRS-REG-002`, `SRS-ALC-001`, `SRS-MCP-001`, `SRS-MCP-002`; `SRS-SEC-003`, `SRS-NFR-004` | `CMP-REG`, `CMP-DB`, `CMP-MCP`, `CMP-SEC`, `CMP-AUD` | `UAT-004` | Gate 8 |
| `AC-005` Safe environment scan | `BO-05` | `PF-003`, `PF-007`, `PF-010`; `US-033`, `US-053`, `US-092` | `SRS-SCN-004`, `SRS-OPS-002`; `SRS-SEC-002`, `SRS-NFR-008`, `SRS-SCN-005` | `CMP-SCN`, `CMP-SEC`, `CMP-AUD` | `UAT-005` | Gate 7 |
| `AC-006` UI root configuration | `BO-04`, `BO-07` | `PF-003`, `PF-006`, `PF-007`, `PF-011`; `US-030`, `US-060`, `US-052`, `US-100` | `SRS-SCN-001`, `SRS-SCN-002`, `SRS-UI-001`, `SRS-UI-004`, `SRS-OPS-001`, `SRS-OPS-003`; `SRS-SEC-003`, `SRS-OPS-004`, `SRS-NFR-009` | `CMP-SCN`, `CMP-WEB`, `CMP-CFG`, `CMP-SEC`, `CMP-OPS` | `UAT-006` | Gate 7 |
| `AC-007` Public exposure warning | `BO-01`, `BO-05` | `PF-001`, `PF-004`, `PF-005`, `PF-006`; `US-021`, `US-040`, `US-043`, `US-063` | `SRS-COL-002`, `SRS-REG-001`, `SRS-CNF-001`, `SRS-UI-003`; `SRS-SEC-003` | `CMP-COL`, `CMP-REG`, `CMP-CNF`, `CMP-WEB` | `UAT-007` | Gate 7 |
| `AC-008` Race-safe leases | `BO-03`, `BO-06` | `PF-004`, `PF-008`; `US-042`, `US-071` | `SRS-ALC-001`, `SRS-MCP-001`, `SRS-OPS-002`; `SRS-NFR-004`, `SRS-NFR-008` | `CMP-REG`, `CMP-DB`, `CMP-MCP`, `CMP-AUD` | `UAT-008` | Gate 8 |
| `AC-009` Unmanaged limitation | `BO-02`, `BO-03`, `BO-06` | `PF-004`, `PF-005`, `PF-008`; `US-042`, `US-043`, `US-072` | `SRS-ALC-001`, `SRS-CNF-001`, `SRS-MCP-002`; `SRS-NFR-004` | `CMP-REG`, `CMP-CNF`, `CMP-MCP`, `CMP-AUD` | `UAT-009` | Gate 8 |
| `AC-010` AI unavailable | `BO-05`, `BO-08` | `PF-009`, `PF-010`; `US-080`, `US-083` | `SRS-AI-001`, `SRS-AI-003`; `SRS-SEC-001`, `SRS-NFR-003`, `SRS-AI-004` | `CMP-AI`, `CMP-SEC`, `CMP-DOM`, `CMP-AUD` | `UAT-010` | Gate 8 |
| `AC-011` Grounded explanation | `BO-01`, `BO-08` | `PF-005`, `PF-009`; `US-043`, `US-081` | `SRS-AI-002`, `SRS-AI-003`; `SRS-AI-004` | `CMP-AI`, `CMP-CNF`, `CMP-DOM`, `CMP-SEC` | `UAT-011` | Gate 8 |
| `AC-012` Invalid model output | `BO-05`, `BO-08` | `PF-009`, `PF-010`; `US-083`, `US-092` | `SRS-AI-003`; `SRS-SEC-003`, `SRS-AI-004` | `CMP-AI`, `CMP-SEC`, `CMP-AUD` | `UAT-012` | Gate 8 |
| `AC-013` Prompt injection | `BO-05`, `BO-06`, `BO-08` | `PF-008`, `PF-009`, `PF-010`; `US-072`, `US-083`, `US-092` | `SRS-MCP-002`, `SRS-AI-003`; `SRS-SEC-003`, `SRS-AI-004` | `CMP-MCP`, `CMP-AI`, `CMP-SEC`, `CMP-AUD` | `UAT-013` | Gate 8 |
| `AC-014` Secret-safe summary | `BO-05`, `BO-08` | `PF-003`, `PF-009`; `US-033`, `US-081`, `US-082` | `SRS-SCN-004`, `SRS-AI-002`, `SRS-AI-003`; `SRS-SEC-002`, `SRS-AI-004` | `CMP-SCN`, `CMP-AI`, `CMP-SEC`, `CMP-AUD` | `UAT-014` | Gate 8 |
| `AC-015` Unconfirmed AI extraction | `BO-01`, `BO-08` | `PF-003`, `PF-009`; `US-032`, `US-084` | `SRS-AI-003`; `SRS-AI-004`, `SRS-SCN-005` | `CMP-AI`, `CMP-SCN`, `CMP-DOM`, `CMP-SEC` | `UAT-015` | Gate 8 |

## Requirement coverage outside a single founder scenario

The scenario rows cover the initial founder-facing acceptance contract. Cross-cutting or lower-level requirements also have stable verification IDs `VT-SRS-COL-001` through `VT-SRS-OPS-003` and `VT-SRS-SEC-001` through `VT-SRS-SCN-005` in [Acceptance criteria](acceptance-criteria.md#functional-verification-catalog). Those verification records cover CLI breadth, configuration round trips, demo isolation, API drift/error contracts, packaging lifecycle, audit integrity, maintainability, full performance scale, platform isolation, and release quality that cannot be proven by one founder scenario alone.

## Gate 3 foundation traceability

Gate 3 passed on 2026-07-14 at exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](../project/gate-3-evidence.md). Its accepted scope advances `US-010` through `US-013`, `SRS-NFR-006`, and only the foundation controls within `SRS-NFR-009`. The full `SRS-NFR-009` release-quality requirement remains open through Gate 9. `VT-SRS-NFR-006` and `VT-SRS-NFR-009` are the upstream verification records; focused automated test IDs may supplement but not replace them.

| Gate 3 item | Product/backlog | Requirement/decision | Owning component | Gate 3 evidence | Disposition gate |
| --- | --- | --- | --- | --- | --- |
| `G3-00` | `US-003`, `US-010` | Gate 2 contract; `SRS-NFR-009` | All | Exact founder approval and provenance record | Gate 3 |
| `G3-01` | `US-010` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-OPS`, `CMP-AUD` | Stable sprint scope and evidence ledger | Gate 3 |
| `G3-02` | `US-010` | `SRS-NFR-006`, ADR 0001 | `CMP-OPS` | Toolchain pins, clean-run versions, CI matrix | Gate 3 |
| `G3-03` | `US-010` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-OPS` | Private workspaces, frozen locks, lock-drift checks | Gate 3 |
| `G3-04` | `US-011` | `SRS-NFR-006`, ADR 0001 | `CMP-DOM` | Typed package and inward-import architecture checks | Gate 3 |
| `G3-05` | `US-011` | `SRS-NFR-006`, ADR 0008 | `CMP-DOM` | Domain contract unit tests including `ProjectInstance` | Gate 3 |
| `G3-06` | `US-011` | `SRS-NFR-006`, ADR 0002 | `CMP-DOM`, `CMP-DB` | Repository/UoW and minimal persistence contract checks | Gate 3 |
| `G3-07` | `US-011` | `SRS-NFR-006`, ADR 0010 | `CMP-CFG`, `CMP-SEC` | Versioned config, path, loopback, and no-telemetry tests | Gate 3 |
| `G3-08` | `US-011`, `US-013` | `SRS-SEC-003`, ADR 0011 | `CMP-SEC` | Token, scope, permission, and redaction tests | Gate 3 |
| `G3-09` | `US-011` | `SRS-NFR-006`, ADRs 0003, 0004, 0012, 0016 | `CMP-COL`, `CMP-SCN`, `CMP-CLI`, `CMP-MCP`, `CMP-AI` | Interface and optional-import architecture checks | Gate 3 |
| `G3-10` | `US-011` | `SRS-API-001`, `SRS-NFR-006` | `CMP-API`, `CMP-SEC` | Minimal health/OpenAPI/error contract tests | Gate 3 |
| `G3-11` | `US-011`, `US-012` | `SRS-NFR-006`, ADR 0006 | `CMP-WEB` | Strict type, component, accessibility, and client-drift checks | Gate 3 |
| `G3-12` | `US-011` | `SRS-NFR-006`; versioning policy | `CMP-DOM`, `CMP-API`, `CMP-CLI`, `CMP-MCP`, `CMP-WEB` | Version-authority drift check | Gate 3 |
| `G3-13` | `US-010`, `US-013` | `SRS-NFR-006`, `SRS-NFR-009` | All engineering components | Deterministic unit/contract/integration/architecture/security/web harnesses | Gate 3 |
| `G3-14` | `US-012` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-DOM`, `CMP-COL`, `CMP-SCN`, `CMP-CNF`, `CMP-SEC`, `CMP-AI` | Synthetic fixture inventory and secret-safety checks | Gate 3 |
| `G3-15` | `US-010` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-OPS` | Executed contributor commands and documentation agreement | Gate 3 |
| `G3-16` | `US-010`, `US-013` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-OPS`, `CMP-SEC` | Executable hooks and required hosted-CI result | Gate 3 |
| `G3-17` | `US-010`, `US-012` | `SRS-NFR-003`, `SRS-NFR-007` | `CMP-DOM`, `CMP-DB`, `CMP-COL`, `CMP-AI` | Default suite with optional services/tools absent | Gate 3 |
| `G3-18` | `US-010`, `US-013` | `SRS-NFR-006`, `SRS-NFR-009` | `CMP-SEC`, `CMP-OPS` | Secret/dependency/license/vulnerability/supply-chain results | Gate 3 |
| `G3-19` | `US-010`, `US-011` | `SRS-NFR-006` and Accepted ADRs | All affected components | Dated research closure and owning-gate register updates | Gate 3 |
| `G3-20` | `US-100` | `SRS-OPS-001`, ADR 0007 | `CMP-OPS` | Research memo only; no package or lifecycle acceptance | Gate 3 research; Gate 9 acceptance |
| `G3-21` | `US-010`, `US-013` | `SRS-NFR-006`, foundation subset of `SRS-NFR-009` | `CMP-OPS`, `CMP-AUD` | Exact revision, complete check evidence, clean state, founder disposition | Gate 3 |

## Gate 4 runtime inventory traceability

Gate 4 remains **Proposed** and has no implementation authority until the founder accepts the [Gate 4 sprint brief](../project/gate-4-sprint-brief.md) at an exact revision. Its planning base is integrated closure successor `461243541d6b63ddebf54598c6860ba73abcd012`; the immutable approved Gate 3 engineering candidate remains `4adf1fb500b651e425735595db528fd42fffba73`. Every row below is **Evidence pending**.

The proposed gate advances primary product work for `US-011`, `US-012`, and `US-020` through `US-023` through `SRS-COL-001`–`004`, the applicable cross-cutting security/non-functional requirements, and bounded subsets of `SRS-API-001` and `SRS-CLI-001`. It also advances only the internal audit/observability prerequisite of `US-053`; the complete reviewer workflow and diagnostic interfaces remain Gate 7 and release work. It does not complete any founder UAT: `AC-001` is collector-evidence-only, `AC-003` is runtime-observation-only, both complete at Gate 7, and `AC-007` has no Gate 4 acceptance claim.

| Gate 4 item | Product/backlog | Requirement or decision scope | Owning component | Proposed verification | Final disposition |
| --- | --- | --- | --- | --- | --- |
| `G4-00` | `US-011` | Gate 3 closure; planning base and gate exclusions | All affected components | Ancestry, clean-state, scope, publication, and founder-acceptance audit | Gate 4 prerequisite; Evidence pending |
| `G4-01` | `US-011`, `US-012` | Traceability and partial acceptance dispositions | `CMP-AUD`, `CMP-CFG` | Documentation/link/ID validation and evidence-ledger crosswalk | Gate 4; Evidence pending |
| `G4-02` | `US-011`, `US-012` | Typed runtime contracts for `SRS-COL-001`–`004`; `SRS-NFR-006`/`007` boundaries | `CMP-DOM`, `CMP-COL`, `CMP-DKR` | `TEST-ARCH-001`, `UT-DOM-001`, Gate 4 subsets of `VT-SRS-NFR-006`/`007`, contract/property tests | Gate 4; Evidence pending |
| `G4-03` | `US-011`, `US-053` | Runtime persistence/migration/repository/last-good/outbox plus bounded `SRS-OPS-002` and `SRS-NFR-008` audit/log/correlation/local-metrics subset | `CMP-DB`, `CMP-DOM`, `CMP-AUD`, `CMP-SEC` | `IT-SQL-001`; Gate 4 subsets of `VT-SRS-OPS-002` and `VT-SRS-NFR-008`; opt-in `IT-PG-001` | Gate 4 runtime observability; full audit/diagnostics later; Evidence pending |
| `G4-04` | `US-020`, `US-021`, `US-022` | `SRS-COL-001`–`003` normalization and identity semantics | `CMP-DOM`, `CMP-COL`, `CMP-DKR`, `CMP-SEC` | `UT-DOM-001`, `UT-COL-001`, `VT-SRS-COL-001`–`003` | Gate 4; Evidence pending |
| `G4-05` | `US-020`, `US-021` | `SRS-COL-001` and `SRS-COL-002` primary macOS `psutil` collection | `CMP-COL`, `CMP-DOM` | `VT-SRS-COL-001`, `VT-SRS-COL-002`, controlled real listeners | Gate 4; Evidence pending |
| `G4-06` | `US-020`, `US-021` | Bounded `lsof -nP` fallback/validation for `SRS-COL-001` and `SRS-COL-002` | `CMP-COL`, `CMP-SEC` | `UT-COL-001`, fallback/failure fixtures and real comparison | Gate 4; Evidence pending |
| `G4-07` | `US-021`, `US-012` | PID/start, executable, redacted command, user, working directory, parent, interface facts, and nullable association-ready evidence; no project discovery or assignment | `CMP-SEC`, `CMP-COL`, `CMP-DOM` | `SEC-T-SECRET-001`, `VT-SRS-SEC-002`, `VT-SRS-COL-002`, permission/exit/PID-reuse fixtures | Gate 4 evidence; project identity/association Gate 5; Evidence pending |
| `G4-08` | `US-023` | Runtime-only subset of `SRS-COL-004`; applicable `SRS-NFR-001`/`003`; no filesystem watcher/scan/cache or conflicts | `CMP-DOM`, `CMP-COL`, `CMP-DB`, `CMP-AUD` | `UT-COL-001`, `IT-SQL-001`, `TEST-ISO-001`, runtime subsets of `VT-SRS-COL-004`, `VT-SRS-NFR-001`, and `VT-SRS-NFR-003` | Gate 4 runtime subset; Gate 5 scanner subset; Evidence pending |
| `G4-09` | `US-020`, `US-021`, `US-023` | Bounded `SRS-API-001`/`SRS-CLI-001`: system/capabilities, collectors, refresh, observations; CLI `status`, `ports`, and `collectors refresh` | `CMP-API`, `CMP-CLI`, `CMP-DOM`, `CMP-SEC` | `CT-API-001`, `CT-CLI-001`, `SEC-T-AUTH-001`, bounded `VT-SRS-API-001`, `VT-SRS-CLI-001`, `VT-SRS-SEC-003`, `PERF-API-001` | Later gates complete API/CLI; Evidence pending |
| `G4-10` | `US-023` | Transactional outbox and dashboard SSE runtime subset | `CMP-DB`, `CMP-API`, `CMP-AUD`, `CMP-SEC` | `CT-API-001`, `SEC-T-AUTH-001`, `VT-SRS-SEC-003`, `PERF-SSE-001`, replay/restart/gap/security cases | Gate 4 runtime events; Evidence pending |
| `G4-11` | `US-020`, `US-021`, `US-023` | Real Apple-silicon macOS host vertical slice | `CMP-COL`, `CMP-DOM`, `CMP-DB`, `CMP-API`, `CMP-CLI`, `CMP-SEC` | `VT-SRS-COL-001`, `VT-SRS-COL-002`, `PERF-COL-001`, real controlled matrix | Gate 4 host increment; Evidence pending |
| `G4-12` | `US-022`, `US-023` | Optional Docker SDK probe, negotiation, and degradation under `SRS-COL-003` | `CMP-DKR`, `CMP-CFG`, `CMP-SEC` | `TEST-ISO-001`, `IT-DKR-001`, one real negotiation profile | Gate 4; Evidence pending |
| `G4-13` | `US-022` | Complete `SRS-COL-003` runtime field set: container identity/state, safe name/image/tag, health, start time, restart policy, networks, internal/exposed/published bindings/interfaces, and safe labels; no project assignment | `CMP-DKR`, `CMP-DOM`, `CMP-SEC` | `UT-DOM-001`, `UT-COL-001`, `IT-DKR-001`, `VT-SRS-COL-003` | Gate 4 runtime facts/evidence; project identity/association Gate 5; conflict computation Gate 6; `AC-003`/`UAT-003` completion Gate 7; Evidence pending |
| `G4-14` | `US-023` | Docker events plus periodic reconciliation under runtime subset of `SRS-COL-004` | `CMP-DKR`, `CMP-DOM`, `CMP-DB`, `CMP-API`, `CMP-AUD` | `IT-DKR-001`, `TEST-ISO-001`, `CT-API-001`, runtime subset of `VT-SRS-COL-004` | Gate 4 runtime subset; Evidence pending |
| `G4-15` | `US-022`, `US-023` | Docker security, isolation, redaction, no telemetry, and no lifecycle operations under Gate 4 subsets of `SRS-SEC-001`–`003` and `SRS-NFR-008` | `CMP-DKR`, `CMP-SEC`, `CMP-AUD` | `TEST-ARCH-001`, `TEST-ISO-001`, `SEC-T-AUTH-001`, `SEC-T-SECRET-001`, Gate 4 subsets of `VT-SRS-SEC-001`–`003` and `VT-SRS-NFR-008`, lifecycle/outbound audit | Gate 4; Evidence pending |
| `G4-16` | `US-020`–`US-023` | `SM-04`, `SM-08`, runtime-only `SM-10`; Gate 4 subsets of `SRS-NFR-001`–`003` and `006`–`008` | `CMP-COL`, `CMP-DKR`, `CMP-DB`, `CMP-API`, `CMP-AUD`, `CMP-SEC` | `PERF-COL-001`, `PERF-SSE-001`, `PERF-API-001`, storage part of `PERF-DB-001`, applicable subsets of `VT-SRS-NFR-001`–`003` and `006`–`008`, 1,000 observations | Gate 4 runtime profile; full cross-cutting and `SM-10` evidence remains later; Evidence pending |
| `G4-17` | `US-011`, `US-012` | Exact candidate evidence and founder disposition | `CMP-AUD`, `CMP-SEC` | Local/hosted evidence, real profiles, clean/synced Git, exact 40-character candidate approval | Gate 4; Evidence pending |

The Gate 4 cross-cutting set is the implemented-surface subset of `SRS-SEC-001`–`003`, `SRS-NFR-001`, `003`, `006`, `007`, and `008`, plus only the 1,000-runtime-observation storage/query/reconciliation portion of `SRS-NFR-002` and the Gate 4 read/integration/audit subset of `SRS-OPS-002`. Canonical evidence is the applicable subset of `VT-SRS-SEC-001`–`003`, `VT-SRS-NFR-001`–`003`, `VT-SRS-NFR-006`–`008`, and `VT-SRS-OPS-002`; focused suites supplement rather than replace those records. Scanner/UI/MCP/AI/export/complete-diagnostic portions retain their later owners. `SM-04` completes only at the visible-browser boundary in Gate 7; `SM-08` applies fully to every implemented Gate 4 surface; the complete repository/declaration/UI scale and founder-UAT meaning of `SM-10` remains open through Gates 7 and 9.

## Change-control rules

1. A business/product requirement change updates its `BO-*`/`PF-*`/`US-*` source and every affected matrix row.
2. An SRS change preserves stable IDs; superseded behavior is versioned rather than silently reusing an ID for a different meaning.
3. Architecture ADRs may change repository placement but must map retained responsibilities to the stable `CMP-*` identifiers or explicitly migrate the matrix.
4. When implementation begins, each story row receives issue/PR and automated test artifact links without deleting UAT traceability.
5. A Gate cannot pass with an uncovered Must requirement, missing verification artifact, failed applicable scenario, or unresolved authority/security decision.
