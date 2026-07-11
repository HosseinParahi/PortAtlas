# PortAtlas Project Charter

## Document control

- Status: first-checkpoint product definition
- Authority: derived from the PortAtlas master brief
- Decision state: suitable for founder review; it does not authorize production implementation
- Related documents: [Vision](vision.md), [BRD](brd.md), [PRD](prd.md), [Scope and non-goals](scope-and-non-goals.md), [SRS](../requirements/srs.md), and [Assumptions and constraints](../requirements/assumptions-and-constraints.md)

## Purpose

PortAtlas will be an open-source, local-first developer control center for discovering, mapping, monitoring, reserving, and coordinating ports across a developer's machine. It will combine runtime observation, static project discovery, explicit reservations, safe allocation, conflict analysis, and agent integration without turning into a general process manager, Docker orchestrator, or cloud service.

## Problem

Developers who run many projects simultaneously encounter port collisions only when a command or container fails. Native processes, Docker bindings, inactive project declarations, worktrees, databases, and agent-selected defaults form one machine-wide coordination problem, but today they are inspected with disconnected commands and undocumented conventions. The result is wasted time, unsafe public bindings, stale services, and inconsistent source changes.

## Product truth and assurance boundary

The MVP provides inventory, preflight, policy-aware suggestions, persistent reservations, and atomic short-lived leases. A lease coordinates participating PortAtlas clients while it is active, but the MVP does not edit project files, launch or stop services, control Docker lifecycle, or verify a launched listener. All actual launches are unmanaged from the MVP's perspective, so PortAtlas detects, warns, explains, recommends, and reconciles without claiming end-to-end prevention.

Version 1 may add a managed runner that acquires a lease, injects an approved assignment, starts a process, verifies the listener, and releases state. Only that future integrated path may claim strong launch-conflict prevention. Every customer-facing, API, MCP, README, and agent statement must preserve this temporal boundary: "available when checked" is not "reserved," and an MVP lease is not a launch supervisor.

## Objectives

1. Establish a trustworthy, evidence-backed inventory of observed, declared, reserved, leased, desired, conflicted, stale, ignored, and unknown port state.
2. Explain port ownership and declaration provenance quickly enough to support daily development.
3. Detect current and future conflicts, including native-versus-Docker and declaration-versus-declaration collisions.
4. Allocate and reserve ports deterministically and safely under concurrency.
5. Give Codex, Claude-compatible clients, and other MCP hosts a permissioned preflight-and-reservation workflow.
6. Remain private, useful offline, read-only by default, and fully functional without Docker or AI.
7. Ship with macOS-first installation, testing, security, contributor, and release foundations suitable for an open-source project.
8. Model one logical `Project` with one or more concrete `ProjectInstance` checkout/worktree records; scanning, runtime association, policy evaluation, reservation, and lease allocation occur at instance scope.

## Initial scope

The MVP includes macOS host and Docker inventory, approved project-root discovery with `Project`/`ProjectInstance` identity, the locked deterministic parser set, evidence and confidence, policies, reservations and leases, conflict diagnosis, safe suggestions, a browser UI, local API with Server-Sent Events, CLI, MCP server and setup, audit, non-secret import/export, demo data, tests, and conditional optional Ollama assistance. The detailed boundary is maintained in [Scope and non-goals](scope-and-non-goals.md).

## Stakeholders

| Stakeholder | Interest | Decision role |
| --- | --- | --- |
| Founder | Daily utility, product direction, risk and scope | Confirms gate evidence and decides the remaining name, signing, package-namespace, sponsorship, AI-release, and release inputs |
| Multi-project local developer | Fast, accurate inventory and conflict resolution | Primary UAT participant |
| Agent-assisted developer | Safe preflight, reservation, and evidence through MCP | Validates integration workflow |
| Open-source maintainer | Predictable contributor setup and sustainable governance | Reviews maintainability and release readiness |
| Contributors and security researchers | Clear contracts, fixtures, disclosure path, and safe defaults | Provide review and extension feedback |

## Principles

- Local-first and private by default.
- Read-only observation is the default; mutation is explicit, scoped, previewed, and audited.
- Observed, declared, reserved, leased, desired, and conflicted state remain separate.
- Every claim carries evidence, provenance, timestamp, and confidence where applicable.
- Host visibility requires a native collector; Docker is an integration, not a prerequisite.
- macOS is the first implementation target behind cross-platform boundaries.
- AI is optional, advisory, read-only in the MVP, and never authoritative for availability, allocation, leases, policy, or conflicts.
- Open-source documentation, testing, security, packaging, and governance are product work.

## Governance and approval gates

| Gate | Evidence required | Founder decision |
| --- | --- | --- |
| 0 — discovery | Repository/toolchain inspection, current primary-source research, risk and assumption registers | Accept findings and reversible assumptions |
| 1 — product | Charter, BRD, PRD, journeys, scope, metrics, backlog, roadmap, and wireframes | Approve product direction |
| 2 — architecture | SRS, traceability, HLD/LLD, ADRs, data/API/MCP design, threat model, and test strategy | Approve architecture and MVP boundary |
| 3 — foundation | Green formatting, lint, type, test, CI, contracts, fixtures, and base docs | Authorize feature implementation |
| 4–8 — capability gates | Accuracy, corpus, concurrency, UAT, integration, and AI-safety evidence | Approve progression by capability |
| 9 — release | Packaging, install lifecycle, UAT, security review, SBOM, release checklist, and name/license evidence | Approve public release |

No full production feature implementation is authorized by this charter alone.

## Accepted product and architecture baseline

The locked baseline is: macOS and one local OS user for MVP; a native Python service serving a React/TypeScript browser UI; embedded SQLite by default with a supported PostgreSQL profile; one logical `Project` containing concrete `ProjectInstance` checkout/worktree records; Server-Sent Events for UI updates; MCP over STDIO and loopback streamable HTTP; Codex as the first polished client; no telemetry; seven-day configurable history; Apache-2.0 licensing, including commercial use without payment; and voluntary sponsorship only.

The MVP parser and mutation boundaries are also locked. Managed launch, source patch generation/application, process termination, Docker lifecycle actions, active health checks beyond existing deterministic status, embeddings, and semantic search are absent from MVP. Remaining release inputs are limited to working-name clearance, package namespaces, signing identity, sponsorship handle, exact dependency patch versions, conditional AI inclusion after its gates, and packaging implementation evidence. [Assumptions and constraints](../requirements/assumptions-and-constraints.md) records the details.

## Principal risks

| Risk | Consequence | First control |
| --- | --- | --- |
| OS permission gaps or unstable command output | Incorrect ownership or missing sockets | Capability reporting, version-tolerant collectors, fixtures, and real-machine validation |
| Race between suggestion and unmanaged launch | Collision despite a prior check | Distinguish suggestion from lease and explain unmanaged limits |
| Secret leakage from environment/process/project data | Privacy and security incident | Minimum-context parsing, redaction tests, safe logs, and no raw environment export |
| Docker socket privilege | Host compromise surface | Least privilege, local-only adapter, no remote unauthenticated control |
| Broad repository scanning | Performance, privacy, and denial-of-service risk | Approved roots, preview, exclusions, limits, targeted parsers, and cancellation |
| Scope expansion into process management or AI autonomy | Delayed, unsafe MVP | Non-goals, MoSCoW priority, approval gates, and authority boundaries |
| Packaging/signing friction | Five-minute install target missed | Early ADR and real clean-machine packaging tests |
| Working-title collision | Legal or discoverability risk | Repository, registry, domain, and trademark/name review before release |

## Success and exit condition

The first product checkpoint exits only when the founder can review a coherent product direction, scope, requirements baseline, measurable acceptance scenarios, risks, trade-offs, and decisions. Quantitative targets are defined in [Success metrics](success-metrics.md), and delivery evidence is defined in [Acceptance criteria](../requirements/acceptance-criteria.md).
