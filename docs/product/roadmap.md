# PortAtlas Roadmap

## Roadmap policy

This roadmap is sequenced by evidence and approval gates, not calendar promises. Sprint labels represent two-week-equivalent scopes only. A phase may not claim exit until its gate evidence is recorded; later work can be researched but must not bypass shared contract and safety decisions.

## Current dispositions

- Gate 2 was founder-approved on 2026-07-11 at exact revision [`e53f399`](../project/gate-2-approval.md).
- Gate 3 candidate-local evidence is complete on `codex/gate3-engineering-foundation`; the exact candidate revision, hosted CI, clean Git state, and founder binding remain pending.
- The active engineering scope is the 22-item [Gate 3 sprint brief](../project/gate-3-sprint-brief.md).
- Gate 3 packaging activity is research-only. Distributable packaging and lifecycle acceptance remain Phase/Gate 9.

## Phase and gate map

| Phase | Goal | Principal outputs | Exit gate |
| --- | --- | --- | --- |
| 0 — Discovery and research | Verify repository, environment, current standards, prior art, and risks | Work/assumption/decision/risk registers, official-source research, open questions; no production feature code | Gate 0: findings and assumptions reviewed |
| 1 — Product definition | Agree on problem, users, outcomes, scope, journeys, UX direction, measures, and backlog | Charter, BRD, PRD, personas, journeys, scope, metrics, IA, wireframes, backlog, roadmap | Gate 1: founder approves product direction |
| 2 — Requirements and architecture | Convert direction into testable contracts and decisions | SRS, functional/non-functional requirements, acceptance, traceability, architecture/HLD/LLD, domain/data/API/MCP design, threat model, ADRs, test/deployment strategy | Gate 2: founder approves architecture and MVP scope |
| 3 — Engineering foundation | Establish a coherent monorepo and quality controls | Toolchains, formatting, lint, typing, tests, CI, hooks, docs, `AGENTS.md`, contracts, demo fixtures | Gate 3: foundation green in CI |
| 4 — Runtime inventory | Prove host and Docker observation | Domain/persistence vertical slice, macOS and Docker collectors, normalization/reconciliation, API/basic CLI, tests | Gate 4: accurate on a real macOS machine |
| 5 — Project discovery | Prove safe exact declaration detection | Root management, logical `Project` and concrete `ProjectInstance` identity, locked parser framework, evidence/confidence, watchers/cache, corpus tests | Gate 5: approved real corpus meets detection targets |
| 6 — Registry and conflicts | Prove safe coordination under races | Policies, reservations, leases, allocator, conflict/exposure engine, explanations, audit, concurrency/property tests | Gate 6: allocation/conflict suite passes under concurrency |
| 7 — Human experience | Complete primary local workflows | Setup, overview, ports, projects, conflicts, reservations, settings, integrations, demo, accessibility, E2E | Gate 7: founder completes primary UAT |
| 8 — Agents and conditional local AI | Prove permissioned integration and AI isolation | MCP resources/tools/prompts/transports/auth, Codex/Claude setup, agent tests; optional provider, redaction, validation, failure/security evaluation | Gate 8: safe preflight/reservation and, if included, advisory-only AI |
| 9 — Packaging and release | Produce a reviewable public release candidate | macOS package, lifecycle docs/tests, signing identity, automation, SBOM, changelog, security/release review, working-name/package-namespace evidence | Gate 9: UAT and release checklist approved |

## Sprint sequence

### Sprint 0: Product discovery and requirements

- Goal: create the first reviewable product baseline.
- Dependencies: repository/toolchain inspection and the master brief; no production implementation dependency.
- Scope: Phase 0 findings and Phase 1 product documents; initial requirements outline, risks, decisions, research plan.
- Stories: `US-001`–`US-003`.
- Acceptance criteria: Gate 0 evidence is factual; assurance, scope, metrics, assumptions, and decisions are internally consistent.
- Tests: documentation link, ID, placeholder, and repository-state checks.
- Documentation: all Phase 0/1 product documents and the initial requirements baseline.
- Risks: hidden assumptions, premature architecture choice, or unsupported current-technology claims.
- Demo: walk through problem, personas, assurance boundary, journeys, wireframes, metrics, and open decisions.
- Exit gate: Gate 0 complete and Gate 1 package ready for founder review; no production feature code begins.

### Sprint 1: Architecture, ADRs, and foundation design

- Goal: settle the boundaries required for safe parallel work.
- Dependencies: Gate 1 product direction and current official-source research.
- Scope: SRS/traceability, domain/data/API/MCP contracts, threat/test/deployment designs, architecture comparison, mandatory ADR proposals, foundation plan.
- Stories: `US-002`, `US-003`, `US-010`–`US-013`.
- Acceptance criteria: every Must requirement has a stable ID, component, verification mapping, and resolved or explicitly gated architecture dependency.
- Tests: requirements/ID/link validation, architecture consistency, threat-control coverage, and contract examples.
- Documentation: SRS/traceability, architecture/design, threat/test/deployment strategy, and ADR proposals.
- Risks: conflicting schemas, authority gaps, persistence/packaging lock-in, or overbuilt local architecture.
- Demo: trace an acceptance scenario from business outcome through requirement, contract, threat control, and test.
- Exit gate: Gate 2 confirms that detailed contracts and ADRs match the locked shared schemas and authority boundaries.

### Sprint 1A: Engineering foundation

- Goal: turn the approved contracts into one reproducible, typed monorepo and quality foundation without implementing later-gate product behavior.
- Dependencies: exact Gate 2 approval at `e53f39916b2348e8626375bb33cac147e27bd217`, Accepted ADRs, and the working-name publication block.
- Scope: `G3-00` through `G3-21` in the [Gate 3 sprint brief](../project/gate-3-sprint-brief.md): pinned toolchains, frozen locks, Python/domain/persistence/config/auth/adapter/REST foundations, strict React and API-client foundations, version authority, test/fixture harnesses, contributor commands, hooks/CI, optional-dependency isolation, supply-chain controls, research closure, bounded packaging spike, and evidence disposition.
- Stories: `US-010`–`US-013`.
- Acceptance criteria: `SRS-NFR-006` and the Gate 3 subset of `SRS-NFR-009` pass through `VT-SRS-NFR-006` and `VT-SRS-NFR-009`; foundation seams must not claim feature requirements assigned to Gates 4–8.
- Technical tasks: implement exactly the responsibilities named by each `G3-*` item and enforce inward dependency direction, private working-title metadata, deterministic state, secret-safe boundaries, and no telemetry.
- Tests: formatting, lint, strict typing, unit, contract, integration, architecture, security, browser accessibility, contract-drift, documentation, lock, secret, dependency, and license checks; default checks run with optional services absent.
- Documentation: verified development commands, toolchain/lock sources, decision/open-question closure, fixture inventory, CI evidence, risks, and exact-revision gate record.
- Risks: accidental package publication, adapter-owned business rules, unpinned transitive inputs, secret-bearing evidence, optional-service coupling, false feature claims, or premature packaging commitment.
- Demo: reproduce the frozen bootstrap, exercise the minimal authenticated service/client seams and accessible fixture shell, then run the aggregate checks with Docker, PostgreSQL, Ollama, Rust, and packaging tools disabled.
- Exit gate: Gate 3 passes only when all `G3-00`–`G3-21` evidence is accepted, required hosted CI is green for the exact candidate revision, Git/locks are clean, and the founder records a disposition. Local checks alone do not close the gate.

### Sprint 2: Domain, persistence, and macOS collector

- Goal: deliver one tested vertical slice from socket evidence to API/CLI projection.
- Dependencies: Gate 3 approval, component contracts, persistence ADR, and the accepted green foundation revision.
- Scope: state/domain contracts, chosen persistence profile, migrations, macOS collection, process identity, safe logs, fixtures.
- Stories: `US-011`, `US-012`, `US-020`, `US-021`.
- Acceptance criteria: `SRS-COL-001`, `SRS-COL-002`, and persistence/recovery contracts pass controlled TCP/UDP IPv4/IPv6 cases.
- Tests: normalization, process/redaction fixtures, collector integration, migration recovery, permission/timeout/output-limit faults.
- Documentation: domain/data/collector design, persistence ADR, capability behavior, and verified development/test commands.
- Risks: OS output drift, permission gaps, PID reuse, secret-bearing commands, or migration coupling.
- Demo: inspect a real TCP/UDP listener with PID plus start time and evidence.
- Exit gate: collector accuracy/capability report is accepted toward Gate 4 and relevant checks are green.

### Sprint 3: Docker mapping and reconciliation

- Goal: reconcile native and container state without requiring Docker.
- Dependencies: Sprint 2 state/persistence contracts and approved Docker threat boundary.
- Scope: Docker API adapter, Compose identity, bindings, event/poll reconciliation, last-known-good/degraded state.
- Stories: `US-022`, `US-023`.
- Acceptance criteria: `SRS-COL-003`, `SRS-COL-004`, and the runtime portion of `AC-003` distinguish internal, exposed, published, and interface state; core remains healthy without Docker.
- Tests: fake/optional real Docker integration, event-loss reconciliation, stopped/permission failure, restart/last-good, and update latency.
- Documentation: Docker risk/limitations, adapter/reconciliation design, capability errors, and troubleshooting.
- Risks: Docker socket privilege, Desktop variation, event loss, or misleading host/container semantics.
- Demo: show a published host binding, internal port, and Docker-disabled degradation.
- Exit gate: Gate 4 runtime inventory is accurate on the supported real macOS profile.

### Sprint 4: Project roots, discovery, and scanner framework

- Goal: safely identify approved projects and services.
- Dependencies: Gate 4 state model, identity/scanner contracts, and canonical-path threat controls.
- Scope: root preview/configuration, canonical paths/symlinks, Git/monorepo/worktree identity, scanner contracts, progress/cancellation.
- Stories: `US-030`, `US-031`, `US-034`.
- Acceptance criteria: `SRS-SCN-001`, `SRS-SCN-002`, and root/identity portions of `AC-006` pass with one logical `Project`, concrete checkout/worktree `ProjectInstance` records, and instance-scoped scan/runtime/allocation identity.
- Tests: traversal/symlink, depth/include/exclude, pause/cancel, rename, multi-instance/worktree, monorepo, nested, and manual-project fixtures.
- Documentation: root/scanner/`ProjectInstance` identity design, privacy defaults, and fixture contribution guide.
- Risks: path escape, huge trees, duplicate logical identity, incorrect instance association, or broad-source-scan creep.
- Demo: preview and scan a founder-approved project root without source changes.
- Exit gate: root security and identity checks are accepted toward Gate 5.

### Sprint 5: Priority parsers, evidence, and cache

- Goal: meet exact-declaration detection target on the approved corpus.
- Dependencies: Sprint 4 scanner/identity framework and founder-prioritized project formats.
- Scope: priority formats, environment redaction, service catalog, confidence/evidence, watchers/cache/invalidation, malformed/large fixtures.
- Stories: `US-032`–`US-034`.
- Acceptance criteria: `SRS-SCN-003`–`SRS-SCN-005`, `AC-002`, `AC-003`, `AC-005`, and `SM-03` pass for the supported corpus.
- Tests: parser fixtures, malformed/oversize/secret/nesting/worktree cases, cache invalidation, and precision/recall report.
- Documentation: supported-format matrix, evidence/confidence, catalog versioning, redaction, and scanner guide.
- Risks: false positives, unsafe environment handling, stale cache, format drift, or heuristic defaults labeled exact.
- Demo: compare declarations from Compose, safe environment keys, package scripts, Python launchers, and Tauri/task files with provenance.
- Exit gate: Gate 5 target passes with precision, recall, errors, and parser versions recorded.

### Sprint 6: Reservations, allocator, and conflict engine

- Goal: make current and future coordination deterministic and race-safe.
- Dependencies: Gates 4–5 evidence, persistence transactions, and policy/allocation/conflict ADRs.
- Scope: policies, suggestion, reservation/release, leases/expiry, conflict types, exposure, suppression/audit, property/concurrency tests.
- Stories: `US-040`–`US-044`.
- Acceptance criteria: `SRS-REG-001`, `SRS-REG-002`, `SRS-ALC-001`, `SRS-CNF-001`, `AC-002`–`AC-004`, and `AC-007`–`AC-009` pass at domain/API level.
- Tests: property/range/uniqueness/idempotency/concurrency/expiry/rollback, every conflict rule, symmetry, and audit/suppression.
- Documentation: policy, allocator, lease, conflict/exposure, audit, error, and unmanaged-assurance behavior.
- Risks: races, transaction portability, wildcard semantics, stale evidence, or overclaiming unmanaged prevention.
- Demo: two simultaneous clients receive different leases; inactive declarations produce a future conflict.
- Exit gate: Gate 6 allocation and conflict suites pass under concurrency with recorded evidence.

### Sprint 7: Core dashboard and ports

- Goal: make machine truth fast and accessible.
- Dependencies: Gate 6 API projections/events, approved information architecture, and component-system ADR.
- Scope: setup core, overview, port table/detail, search/filter/sort, events, degraded status, keyboard/screen-reader patterns.
- Stories: `US-060`, `US-061`, and overview/ports work from `US-063`.
- Acceptance criteria: `SRS-UI-001`, `SRS-UI-002`, `AC-001`, `AC-006`, `AC-007`, `SM-01`, `SM-04`, `SM-05`, `SM-10`, and `SM-15` pass for implemented flows.
- Tests: component/E2E, pagination/filter state, event degradation, accessibility automation/manual review, latency and scale.
- Documentation: UI behavior, setup/privacy copy, accessibility checklist, and degraded/performance evidence.
- Risks: table density, color-only state, event drift, unsafe metadata display, or blocking work on the API loop.
- Demo: complete `AC-001`, `AC-006`, and `AC-007`.
- Exit gate: update latency, scale, ownership interaction, and accessibility evidence are accepted toward Gate 7.

### Sprint 8: Projects, conflicts, settings, and demo

- Goal: complete primary human workflows and configuration lifecycle.
- Dependencies: Sprint 7 interaction foundation and Gate 6 project/conflict/config APIs.
- Scope: project/conflict/reservation/activity/settings pages, import/export, demo isolation, integration setup shell, E2E and founder UAT.
- Stories: `US-052`, `US-053`, `US-062`–`US-064`.
- Acceptance criteria: `SRS-UI-003`, `SRS-UI-004`, `SRS-OPS-002`, `SRS-OPS-003`, `AC-002`, `AC-003`, `AC-005`, and complete core founder UAT pass.
- Tests: project/conflict detail, safe import/export/recovery, audit correlation, demo isolation, degraded/error and accessibility E2E.
- Documentation: configuration/import/export, project/conflict UX, demo, diagnostics/audit, and UAT evidence.
- Risks: accidental mutation, secret-bearing export, real/synthetic data mixing, or stale navigation context.
- Demo: complete `AC-002`, `AC-003`, `AC-005`, and a reviewed reservation workflow.
- Exit gate: Gate 7 founder primary UAT passes.

### Sprint 9: MCP, CLI, Codex, Claude, and optional Ollama

- Goal: expose service-owned truth safely to agents and, conditionally, local AI.
- Dependencies: Gate 7 application/API contracts, MCP/auth ADR, current client docs, and Gate 2 AI inclusion decision.
- Scope: typed MCP contracts/transports/auth/instructions, guarded tools, Codex setup/rollback, client-neutral docs, MVP CLI contract, and optional provider/capability/read-only uses. Managed launch, patch application, shell completion, and process control remain deferred.
- Stories: `US-070`–`US-074`; conditionally `US-080`–`US-082`.
- Acceptance criteria: `SRS-CLI-001`, `SRS-MCP-001`, `SRS-MCP-002`, `AC-004`, `AC-008`, `AC-009`, `SM-06`; conditionally `SRS-AI-001`, `SRS-AI-002`, `AC-010`, and `AC-011`.
- Tests: CLI contracts, MCP STDIO/HTTP/auth/schema/cancellation, client preview/backup/rollback, agent safety, and provider grounded-response checks.
- Documentation: CLI/MCP design and commands, client-neutral/Codex/Claude setup, permissions, rollback/uninstall, and optional Ollama privacy/setup.
- Risks: client format drift, unauthorized mutation, token/origin exposure, duplicated rules, or model/license drift.
- Demo: complete `AC-004`, `AC-008`, and `AC-009`; if AI is included, demonstrate `AC-010` and grounded `AC-011`.
- Exit gate: agent workflow is ready for Gate 8 with no unauthorized edit; conditional AI still requires its full safety evidence.

### Sprint 10: AI evaluation, security, performance, packaging, and UAT

- Goal: close release-critical risk and validate the full supported matrix.
- Dependencies: Sprints 2–9 integrated release-candidate surface and approved packaging/signing strategy.
- Scope: adversarial/security/evaluation suites, performance/scale, packaging implementation and install lifecycle, diagnostics, accessibility, backup/recovery, signing and SBOM preparation. The Gate 3 packaging spike supplies research inputs only. No autonomous patch, launch, shell, or process-kill capability is introduced.
- Stories: `US-082`–`US-084`, `US-090`–`US-093`, `US-100`, `US-101`.
- Acceptance criteria: applicable `SRS-SEC-001`–`SRS-SEC-003`, `SRS-NFR-001`–`SRS-NFR-009`, `SRS-OPS-001`–`SRS-OPS-004`, `AC-010`–`AC-015`, performance/accessibility/secret/lifecycle metrics, and core-without-AI checks pass.
- Tests: threat and AI adversarial suites, scale/latency, clean lifecycle/recovery, final E2E, and founder UAT.
- Documentation: security/privacy/AI evaluation, performance, diagnostics, operations, packaging/signing, UAT, and release checklist.
- Risks: late security defects, model resource/quality instability, migration failure, signing friction, or AI delaying core.
- Demo: `AC-010` through `AC-015` when AI ships plus clean install/recovery; otherwise demonstrate full core operation with AI absent.
- Exit gate: Gate 8 passes and Gate 9 candidate evidence is complete; AI is deferred if its gate fails.

### Sprint 11: Release candidate and open-source launch

- Goal: produce a clean, documented, reviewable release.
- Dependencies: Gates 7–8, complete candidate evidence, public name/license decisions, and approved artifact/signing process.
- Scope: final name/license decisions, release automation/artifacts, changelog/notes, governance/support, disclosure, compatibility matrix, final UAT and security review.
- Stories: `US-100`–`US-103`.
- Acceptance criteria: all applicable `AC-001`–`AC-015`, Must requirements, scoped `SM-01`–`SM-15`, and name/license/SBOM/security/lifecycle/release checklists pass.
- Tests: release workflow/artifact integrity, smoke profiles, documentation commands/links, dependency/license/secret/security scans, regression and founder UAT.
- Documentation: README/quick start, development/contribution/security/governance/support, lifecycle, release notes/changelog/versioning, and compatibility.
- Risks: name/trademark collision, license incompatibility, unverifiable artifacts, stale instructions, or secret disclosure.
- Demo: install the release artifact without a repository clone, complete primary workflows, then uninstall with deliberate data handling.
- Exit gate: Gate 9 founder approval; public release occurs only after the checklist and UAT pass.

## Required sprint contents

Every sprint brief must state goal, scope, user stories, acceptance criteria, technical tasks, test plan, documentation work, risks, demo, and exit evidence. A scope item that cannot name its acceptance evidence does not enter active implementation.

## Accepted baseline and remaining release inputs

| Item | Status | Release evidence |
| --- | --- | --- |
| Native Python service plus React/TypeScript browser UI | Accepted | Clean-machine packaging implementation evidence |
| Embedded SQLite default plus PostgreSQL profile | Accepted | Migration and compatibility tests |
| Logical `Project` plus concrete checkout/worktree `ProjectInstance` | Accepted | Identity, scan, runtime, policy, reservation, and allocation fixtures |
| Server-Sent Events; MCP STDIO plus loopback streamable HTTP | Accepted | Contract, auth, reconnect, and cancellation tests |
| No telemetry; Apache-2.0; commercial use without payment; voluntary sponsorship | Accepted | License files and no-outbound-telemetry verification |
| Locked MVP parser set and absence of source patch/managed launch/process/Docker lifecycle control | Accepted | Surface inventory and security tests |
| Working-name and package namespaces | Release input | Clearance record |
| Signing identity and sponsorship handle | Release input | Configured release metadata |
| Exact dependency patch versions | Gate 3 engineering input and Gate 9 revalidation input | Frozen foundation locks; candidate-time license/security audit and SBOM |
| Optional AI inclusion | Conditional release input | All Gate 8 AI criteria pass; otherwise AI is deferred |

## Post-MVP horizon

Version 1 prioritization follows evidence from real usage: platform reach, managed launch/change workflows, richer project identity/status, desktop shell, stable local URLs, notifications, extension points, team persistence, and opt-in semantic assistance. Remote/cloud and general system-management capabilities remain future work and require a new product/security review.

## Related documents

- [Backlog](backlog.md)
- [PRD](prd.md)
- [Acceptance criteria](../requirements/acceptance-criteria.md)
- [Traceability matrix](../requirements/traceability-matrix.md)
