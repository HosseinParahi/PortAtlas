# First Checkpoint Plan and Gate Record

## Purpose

Gate 2 turns the founder's master brief into a consistent, testable contract before application scaffolding begins. It is documentation-only apart from the standard-library validator used to protect the documentation itself.

## Locked outcomes

1. A Python modular monolith serves a React browser UI; Tauri is reconsidered in Version 1.
2. SQLite is the embedded default behind SQLAlchemy repositories; PostgreSQL is an optional compatibility profile.
3. macOS and one local OS user are the MVP support target; other operating systems retain adapter contracts.
4. One logical `Project` can own many worktree-aware `ProjectInstance` records.
5. MVP mutation is limited to reservations and atomic leases.
6. The deterministic parser set is Compose, Dockerfile `EXPOSE`, safe `.env*` port keys, `package.json` scripts and workspaces, Vite, Next, Nuxt, SvelteKit, Python launch commands and `pyproject.toml`, Tauri configuration, Makefile, Taskfile, Procfile, and justfile.
7. Browser commands use `/api/v1` REST; browser updates use SSE.
8. MCP uses STDIO and authenticated loopback Streamable HTTP under revision 2025-11-25.
9. Ollama is optional, implemented last, and included only after all AI release gates pass.
10. Apache-2.0 permits individual and commercial use without payment; sponsorship is voluntary.
11. The product collects no telemetry.
12. `PortAtlas` remains a working title and no public namespace is released before the collision decision closes.

## Delivery sequence

| Order | Deliverable | Exit evidence |
|---:|---|---|
| 1 | Governance and research baseline | Root policies, registers, dated sources, and machine snapshot committed |
| 2 | Product, UX, and requirements | MoSCoW scope, measurable targets, fifteen scenarios, and full traceability committed |
| 3 | Architecture, security, testing, and operational contracts | ADRs 0001–0023 and cross-cutting strategies committed |
| 4 | Delivery and release gates | Sprint scopes, community templates, validator, and founder checklist committed |
| 5 | Final verification | Validator, unit tests, whitespace check, review, clean status, and four-commit history |

## Acceptance conditions

- Every required document exists and contains substantive decisions rather than unresolved placeholder markers.
- All fifteen acceptance scenarios map from business objective through feature, requirement, component, test/UAT case, and release gate.
- Managed assurance and unmanaged evidence are consistently distinguished.
- Architecture, persistence, identity, parser scope, mutation scope, and AI policy do not contradict each other.
- Internal links and stable requirement, ADR, and test references validate.
- Repository content contains no secrets, private environment values, or hard-coded founder paths.
- Core future tests are designed to run without Docker or Ollama.
- The final worktree is clean and contains no production application code.

## Stop condition

After local verification and the four baseline commits, stop. Do not push, publish, install dependencies, or begin Phase 3. The next action requires explicit founder approval of Gate 2.
