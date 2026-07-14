# Roadmap

This file is the public summary. Detailed epics, sprint-sized scopes, dependencies, acceptance criteria, demonstrations, and exit gates are maintained in the [product roadmap](docs/product/roadmap.md), accepted [Gate 3 sprint brief](docs/project/gate-3-sprint-brief.md), proposed [Gate 4 sprint brief](docs/project/gate-4-sprint-brief.md), and [first-checkpoint plan](docs/project/first-checkpoint-plan.md).

## Gate 2 — Product and architecture foundation

Status: **approved on 2026-07-11 at exact revision [`e53f399`](docs/project/gate-2-approval.md).**

- Establish governance, research, product, UX, requirements, architecture, security, testing, operations, and release contracts.
- Validate traceability for fifteen founder acceptance scenarios.
- Resolve no public package or namespace claims.
- Preserve the initial four-commit history and its explicit provenance record.

## Gate 3 — Engineering foundation

Status: **passed on 2026-07-14 at exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](docs/project/gate-3-evidence.md).**

- Complete the evidence-bound work items `G3-00` through `G3-21` without importing later-gate product scope.
- Establish pinned, locked, typed Python and React workspace foundations, shared contracts, quality controls, hooks, and CI.
- Implement the domain kernel, persistence seams, configuration and authentication skeletons, adapter boundaries, minimal REST shell, and accessible browser foundation.
- Prove default core checks run without Docker, PostgreSQL, Ollama, Rust, or packaging tools.
- Limit packaging to a research spike; distributable packaging and lifecycle proof remain Gate 9 work.
- Close only after the exact candidate revision, local evidence, required green CI, clean Git state, and founder disposition are recorded.

The [Gate 3 evidence ledger](docs/project/gate-3-evidence.md) records the accepted local, hosted, clean-state, and founder-disposition evidence for the exact engineering candidate. Pull request [#1](https://github.com/HosseinParahi/PortAtlas/pull/1) was integrated into `main` by fast-forward through closure successor `461243541d6b63ddebf54598c6860ba73abcd012`; [main CI run 29348251404](https://github.com/HosseinParahi/PortAtlas/actions/runs/29348251404) succeeded. The successor is the planning base and does not replace the approved engineering candidate.

## Gate 4 — Runtime inventory

Status: **Proposed planning contract; founder acceptance required before implementation.**

- Review the [Gate 4 sprint brief](docs/project/gate-4-sprint-brief.md) on planning-only branch `codex/gate4-runtime-inventory`.
- Keep all Gate 4 work at sprint planning until the founder accepts the proposed brief.
- After acceptance, the planned scope may prove host and optional Docker observation while preserving unmanaged discovery as evidence rather than managed-allocation assurance.
- Do not import Gate 5 project scanning, Gate 6 allocation/conflicts, Gate 7 full UI behavior, Gate 8 MCP/AI, or Gate 9 packaging and release acceptance.

No runtime inventory exists, Gate 4 implementation has not begun, Gate 4 has not passed, and no Gate 4 product behavior is currently authorized.

## Later gates

- Deterministic collectors and scanners
- Registry, reservations, leases, and conflict engine
- REST, SSE, CLI, and browser UI
- MCP adapters and hardened integrations
- Conditional Ollama evaluation and inclusion decision
- Packaging, compatibility, accessibility, security, and founder UAT
- Naming clearance and first public release

Tauri, managed project launch, source patching, process termination, embeddings, and broad plugin execution remain post-MVP work unless a later accepted decision changes their priority.
