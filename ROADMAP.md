# Roadmap

This file is the public summary. Detailed epics, sprint-sized scopes, dependencies, acceptance criteria, demonstrations, and exit gates are maintained in the [product roadmap](docs/product/roadmap.md) and [delivery plan](docs/project/first-checkpoint-plan.md).

## Gate 2 — Product and architecture foundation

Status: documentation baseline prepared for founder approval.

- Establish governance, research, product, UX, requirements, architecture, security, testing, operations, and release contracts.
- Validate traceability for fifteen founder acceptance scenarios.
- Resolve no public package or namespace claims.

## Gate 3 — Engineering foundation

Status: blocked on explicit Gate 2 approval.

- Establish tested Python and React workspace foundations.
- Implement the domain kernel, repositories, configuration, authentication skeleton, and adapter seams.
- Prove core tests run without Docker or Ollama.

## Later gates

- Deterministic collectors and scanners
- Registry, reservations, leases, and conflict engine
- REST, SSE, CLI, and browser UI
- MCP adapters and hardened integrations
- Conditional Ollama evaluation and inclusion decision
- Packaging, compatibility, accessibility, security, and founder UAT
- Naming clearance and first public release

Tauri, managed project launch, source patching, process termination, embeddings, and broad plugin execution remain post-MVP work unless a later accepted decision changes their priority.
