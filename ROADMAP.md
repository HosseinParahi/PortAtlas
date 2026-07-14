# Roadmap

This file is the public summary. Detailed epics, sprint-sized scopes, dependencies, acceptance criteria, demonstrations, and exit gates are maintained in the [product roadmap](docs/product/roadmap.md), [Gate 3 sprint brief](docs/project/gate-3-sprint-brief.md), and [first-checkpoint plan](docs/project/first-checkpoint-plan.md).

## Gate 2 — Product and architecture foundation

Status: **approved on 2026-07-11 at exact revision [`e53f399`](docs/project/gate-2-approval.md).**

- Establish governance, research, product, UX, requirements, architecture, security, testing, operations, and release contracts.
- Validate traceability for fifteen founder acceptance scenarios.
- Resolve no public package or namespace claims.
- Preserve the initial four-commit history and its explicit provenance record.

## Gate 3 — Engineering foundation

Status: **local and hosted engineering evidence complete for exact candidate [`4adf1fb500b651e425735595db528fd42fffba73`](docs/project/gate-3-evidence.md); Gate 3 OPEN pending founder approval bound to that exact revision.**

- Complete the evidence-bound work items `G3-00` through `G3-21` without importing later-gate product scope.
- Establish pinned, locked, typed Python and React workspace foundations, shared contracts, quality controls, hooks, and CI.
- Implement the domain kernel, persistence seams, configuration and authentication skeletons, adapter boundaries, minimal REST shell, and accessible browser foundation.
- Prove default core checks run without Docker, PostgreSQL, Ollama, Rust, or packaging tools.
- Limit packaging to a research spike; distributable packaging and lifecycle proof remain Gate 9 work.
- Close only after the exact candidate revision, local evidence, required green CI, clean Git state, and founder disposition are recorded.

The [Gate 3 evidence ledger](docs/project/gate-3-evidence.md) records the local and hosted evidence for the exact engineering candidate. Gate 3 remains **OPEN** pending founder approval bound to that revision, and Gate 4 behavior remains blocked.

## Later gates

- Deterministic collectors and scanners
- Registry, reservations, leases, and conflict engine
- REST, SSE, CLI, and browser UI
- MCP adapters and hardened integrations
- Conditional Ollama evaluation and inclusion decision
- Packaging, compatibility, accessibility, security, and founder UAT
- Naming clearance and first public release

Tauri, managed project launch, source patching, process termination, embeddings, and broad plugin execution remain post-MVP work unless a later accepted decision changes their priority.
