# PortAtlas Product Requirements Document

## 1. Product summary

PortAtlas is a local-first control center for port intelligence and coordination. It reconciles live host and Docker listeners with declarations discovered in approved projects, explicit reservations, temporary leases, and user-reviewed desired state. It serves humans through a browser UI and CLI and serves coding agents through a local versioned API and MCP server.

This PRD defines who the product serves, what the MVP must achieve, and how product acceptance is judged. Normative system behavior is specified in the [SRS](../requirements/srs.md).

## 2. Product truth

The MVP does not manage launches. It offers deterministic inventory, preflight, suggestions, persistent reservations, and atomic leases; every actual service or Docker launch remains external and unmanaged. A lease coordinates participating PortAtlas clients but does not inject configuration, start a process, or verify its listener. UI copy, API semantics, and MCP instructions must not imply end-to-end launch prevention. Version 1 may add a managed runner and may make a stronger integrated-launch claim only after it implements assignment injection, launch, listener verification, and cleanup.

## 3. Personas and jobs to be done

| Persona | Primary job | Desired outcome |
| --- | --- | --- |
| Multi-project local developer | Understand and coordinate many local services | Find ownership quickly and start projects without avoidable collisions |
| Agent-assisted developer | Let a coding agent select ports safely | Preflight, reserve, and report evidence without source edits or launch authority |
| Open-source maintainer | Give contributors predictable local setup | Shared evidence and policy without mandatory hosted infrastructure |
| Future small-team developer | Reuse common policy while retaining local runtime state | Portable policy and manifests with machine-local observations |

Detailed needs and failure modes are in [Personas](personas.md).

## 4. Product outcomes

| ID | Outcome | Product evidence |
| --- | --- | --- |
| PO-01 | The user understands current machine port state | Overview and ports view reconcile listener, owner, project, service, container, address, and evidence |
| PO-02 | The user sees future conflicts before launch | Inactive declarations and reservations participate in the conflict engine |
| PO-03 | Port selection becomes safe and explainable | Policy-aware suggestions, reservations, atomic leases, and selection reasons |
| PO-04 | Configuration requires no source edit | Setup, roots, exclusions, policies, integrations, privacy, and retention are configurable |
| PO-05 | Agent workflows honor the same truth and permissions | Typed MCP tools call application services rather than duplicate business logic |
| PO-06 | Failure and limited capability are understandable | Collector, Docker, permission, watcher, and AI degradation remain visible and isolated |
| PO-07 | Local data remains private | Offline core, redaction, approved roots, local binding, and no telemetry by default |
| PO-08 | Installation and contribution are credible | Tested macOS lifecycle, demo mode, CI, fixtures, and open-source documentation |

## 5. MoSCoW prioritization

### Must have for MVP

- macOS TCP/UDP and IPv4/IPv6 listener inventory with process identity, bind address, timestamps, and permission limits.
- Docker container and published-port mapping without making Docker mandatory.
- UI-configured approved project roots with scan preview, exclusions, progress, and errors.
- Logical `Project` discovery with concrete checkout/worktree `ProjectInstance` records; each instance is the scan, runtime-association, policy, reservation, and allocation boundary.
- The locked deterministic MVP parsers: Compose; Dockerfile `EXPOSE`; safe `.env*` port keys; `package.json` scripts/workspaces; Vite, Next, Nuxt, and SvelteKit; Python launcher commands and `pyproject.toml`; Tauri configuration; and Makefile, Taskfile, Procfile, and justfile.
- Distinct observed, declared, reserved, leased, desired, conflicted, stale, unknown, and ignored state.
- Evidence, source location, parser/collector identity, and confidence.
- Policy-aware suggestion, manual reservation/release, transaction-safe atomic leases, and conflict analysis.
- Setup wizard, dashboard, dense port inventory, project detail, conflict center, settings, integrations, activity/audit, accessible search/filter/sort, and demo mode.
- Versioned loopback REST API with Server-Sent Events, CLI, MCP STDIO and authenticated loopback streamable HTTP, and Codex-first setup.
- Non-secret configuration import/export, backup/restore, migration, and reset paths.
- Local-first privacy, read-only defaults, threat controls, tests, macOS packaging, and open-source foundation.
- Core operation without internet, Docker, elevated permissions, or any model.

### Should have for MVP when gates pass

- Optional Ollama connection, installed-model/capability discovery, read-only natural-language inventory, grounded conflict explanations and project summaries, strict redaction/schema/evidence validation, and complete failure isolation.
- Client-neutral Claude-compatible setup following the polished Codex path.
- Minimal deterministic service status where data already exists, without expanding into a health-monitoring product.
- A design-only contract for a future versioned project manifest. The `.portatlas.yaml` filename is unpublished, is not in the locked MVP parser catalog, and cannot become a public convention before the working-name gate closes.

### Could have after core acceptance

- Tauri shell or menu-bar wrapper if packaging research proves it materially improves installation.
- Managed `portatlas run`, source-change plan/patch capabilities, stale-service heuristics, active health checks, notifications, shell completion, launcher/tmux hooks, reverse-proxy aliases, deferred scanner adapters, and local embeddings.
- Linux and Windows collectors after platform contracts are proven by the macOS implementation.
- PostgreSQL team/server mode and pluggable scanners/collectors.

### Will not have in MVP

- Cloud sync, remote machine control, hosted SaaS, Kubernetes, database administration, firewall management, packet inspection, credential management, full APM, source-patch endpoints/tools, managed launch, process termination, Docker lifecycle control, unrestricted plugins, autonomous AI tool loops, remote AI providers, or claims of universal collision prevention.

## 6. Feature definitions

| ID | Feature | Primary story source |
| --- | --- | --- |
| PF-001 | Host runtime inventory and process/interface evidence | `US-020`, `US-021`, `US-023` in [Backlog](backlog.md) |
| PF-002 | Docker and Compose inventory | `US-022`, `US-023` |
| PF-003 | Approved `Project`/`ProjectInstance` discovery, locked parsers, evidence, and confidence | `US-030`–`US-034` |
| PF-004 | Policies, suggestions, reservations, and atomic leases | `US-040`–`US-042` |
| PF-005 | Deterministic conflict and exposure intelligence | `US-043`, `US-044` |
| PF-006 | Setup, dashboard, ports, projects, conflicts, search, and demo UX | `US-060`–`US-064` |
| PF-007 | Versioned API, event stream, CLI, configuration, and audit | `US-050`–`US-053` |
| PF-008 | MCP and client integration workflows | `US-070`–`US-074` |
| PF-009 | Optional local AI provider and advisory assistance | `US-080`–`US-084` |
| PF-010 | Quality, security, performance, and UAT | `US-090`–`US-093` |
| PF-011 | macOS packaging and open-source release lifecycle | `US-100`–`US-103` |

### PF-001 and PF-002 — Runtime inventory

Collect live host sockets and Docker state, normalize protocol/interface semantics, associate processes and containers, report capability gaps, retain a timestamped last-known-good snapshot, and stream reconciled changes. Acceptance is governed by `SRS-COL-001` through `SRS-COL-004`.

### PF-003 — Project intelligence

Let users approve roots, preview scope, model one logical `Project` with concrete `ProjectInstance` checkouts/worktrees, run only the locked MVP parsers, and inspect exact or confidence-rated evidence without leaking environment secrets. Instances are the scan/runtime/allocation boundary. Acceptance is governed by `SRS-SCN-001` through `SRS-SCN-004`.

### PF-004 and PF-005 — Registry and conflict coordination

Maintain configurable policies, persistent reservations, atomic expiring leases, deterministic suggestions, and normalized conflicts across runtime, configuration, registry, interface, and protocol state. Acceptance is governed by `SRS-REG-001` through `SRS-CNF-001`.

### PF-006 — Human experience

Provide onboarding, dashboard, inventories, project/conflict detail, reservations, settings, audit, integrations, search, import/export, and isolated demo data with WCAG 2.2 AA-oriented interaction. Acceptance is governed by `SRS-UI-001` through `SRS-UI-004`.

### PF-007 and PF-008 — API, CLI, and agents

Expose the same application rules through `/api/v1`, Server-Sent Events, CLI contracts, and MCP. MVP agent mutation is limited to authenticated, instance-scoped reservations and leases. There are no client-config-write, source-patch, managed-launch, process-control, or Docker-lifecycle tools/endpoints. Acceptance is governed by `SRS-API-001` through `SRS-MCP-002`.

### PF-009 — Optional local AI

When explicitly enabled, an Ollama provider may translate natural language into read-only PortAtlas queries and explain structured evidence. It cannot allocate, reserve, mutate, read arbitrary files, or redefine policy. Invalid or unavailable model behavior leaves core state untouched. Acceptance is governed by `SRS-AI-001` through `SRS-AI-003`.

### PF-010 and PF-011 — Quality, operations, and audit

Record meaningful actions without secrets and provide a tested local installation, start/stop/status/log/upgrade/rollback/backup/uninstall lifecycle. Acceptance is governed by `SRS-OPS-001` through `SRS-OPS-003`.

## 7. Primary user journeys

1. Install and complete privacy-first setup.
2. Add and preview a project root, then scan.
3. Find the owner and evidence for an active port.
4. Detect a future inactive-project or Docker/native collision.
5. Suggest and reserve a policy-compliant port.
6. Configure Codex and run an agent preflight/reservation workflow.
7. Optionally enable Ollama and inspect a grounded explanation.
8. Back up, restore, upgrade, or uninstall safely.

Detailed normal, exception, and recovery paths are in [User journeys](user-journeys.md).

## 8. UX principles

- Lead with system status and conflicts, not raw configuration.
- Keep ownership/source within two interactions.
- Use state labels and icons in addition to color.
- Show evidence and deterministic facts before generated explanation.
- Preview scan scope and copy-ready integration configuration, and require confirmation for every reservation/lease mutation. PortAtlas does not write client configuration in MVP.
- Explain degraded capability in place and preserve unaffected workflows.
- Support keyboard-first navigation, command palette, screen readers, reduced motion, responsive layouts, and light/dark themes.
- Keep real and synthetic data visibly isolated.

See [Information architecture](information-architecture.md) and [Wireframes](wireframes.md).

## 9. Functional acceptance

The MVP must pass all applicable deterministic scenarios `AC-001` through `AC-009`. If optional local AI is included, it must also pass `AC-010` through `AC-015`. No scenario may be waived merely because its happy path works. Full Given/When/Then criteria and test mappings are in [Acceptance criteria](../requirements/acceptance-criteria.md).

## 10. Local measurement plan

PortAtlas may calculate local operational metrics needed to validate product quality—scan coverage, update latency, query interactions, lease collisions, resource counts, and error rates—without external export. The accepted product has no telemetry or telemetry configuration.

The exact target, method, and evidence artifact for each measure are in [Success metrics](success-metrics.md).

## 11. Launch criteria

- Gate 2 architecture and MVP scope approved.
- All Must requirements have stable SRS IDs and traced tests.
- Required deterministic acceptance scenarios pass on a real macOS machine and controlled fixtures.
- Performance, accessibility, security, redaction, concurrency, recovery, and install-lifecycle thresholds pass.
- Core tests pass with Docker absent and Ollama absent.
- Any shipped AI capability passes all conditional AI release criteria.
- README, contributor, security, operations, release, license, and governance materials are complete.
- Name-collision research, dependency licenses, signing strategy, UAT, and release checklist are approved.

## 12. Product risks

- A broad parser list may dilute exact detection quality; corpus priority must precede expansion.
- UI density may compromise accessibility; table alternatives and keyboard testing are release gates.
- Native permissions and Docker Desktop differences may reduce attribution; the product must state uncertainty.
- Packaging implementation may miss the five-minute or lifecycle targets; the accepted native service/browser architecture requires clean-machine evidence.
- Model quality and licensing drift; no model may be permanently hard-coded or downloaded automatically.

## 13. Remaining release inputs

Architecture and scope choices are locked in [Assumptions and constraints](../requirements/assumptions-and-constraints.md). The remaining inputs are working-name and package-namespace clearance, signing identity, sponsorship handle, exact dependency patch versions, clean-machine packaging evidence, and whether optional AI is included after every AI gate passes.

## 14. Roadmap

Delivery order, gates, and two-week-equivalent sprint scopes are maintained in [Roadmap](roadmap.md). The schedule expresses sequence and evidence, not calendar promises.

## Related documents

- [BRD](brd.md)
- [Backlog](backlog.md)
- [Scope and non-goals](scope-and-non-goals.md)
- [Success metrics](success-metrics.md)
- [SRS](../requirements/srs.md)
- [Traceability matrix](../requirements/traceability-matrix.md)
