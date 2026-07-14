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

## Change-control rules

1. A business/product requirement change updates its `BO-*`/`PF-*`/`US-*` source and every affected matrix row.
2. An SRS change preserves stable IDs; superseded behavior is versioned rather than silently reusing an ID for a different meaning.
3. Architecture ADRs may change repository placement but must map retained responsibilities to the stable `CMP-*` identifiers or explicitly migrate the matrix.
4. When implementation begins, each story row receives issue/PR and automated test artifact links without deleting UAT traceability.
5. A Gate cannot pass with an uncovered Must requirement, missing verification artifact, failed applicable scenario, or unresolved authority/security decision.
