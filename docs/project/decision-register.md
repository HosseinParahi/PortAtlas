# Decision Register

This register is a compact index. Architecture rationale and consequences live in the linked ADRs.

| ID | Decision | Status | Source of truth |
|---|---|---|---|
| DEC-001 | Use a native Python modular monolith serving a React browser UI; revisit Tauri in Version 1. | Accepted | [ADR-0001](../adr/0001-runtime-architecture.md), [ADR-0007](../adr/0007-packaging.md) |
| DEC-002 | Use SQLite by default through SQLAlchemy repositories and offer PostgreSQL as an optional compatibility profile. | Accepted | [ADR-0002](../adr/0002-persistence.md) |
| DEC-003 | Target macOS and one OS user for MVP while retaining Linux and Windows adapter contracts. | Accepted | [SRS constraints](../requirements/assumptions-and-constraints.md) |
| DEC-004 | Represent each checkout or worktree as a `ProjectInstance` beneath one logical `Project`. | Accepted | [ADR-0008](../adr/0008-project-worktree-identity.md) |
| DEC-005 | Limit MVP mutation to reservations and atomic leases. | Accepted | [ADR-0009](../adr/0009-allocator.md) |
| DEC-006 | Use the locked focused deterministic parser set. | Accepted | [Scanner design](../design/scanner-design.md) |
| DEC-007 | Use versioned REST commands and SSE browser updates. | Accepted | [ADR-0005](../adr/0005-sse.md), [REST contract](../design/api-design.md) |
| DEC-008 | Support MCP over STDIO and authenticated loopback Streamable HTTP against revision 2025-11-25. | Accepted | [ADR-0012](../adr/0012-mcp.md) |
| DEC-009 | Include Ollama in MVP only if all AI privacy, safety, validation, and isolation gates pass. | Conditional | [ADR-0016](../adr/0016-conditional-ai.md) |
| DEC-010 | License contributions and releases under Apache-2.0, allow commercial use without payment, and make sponsorship voluntary. | Accepted | [ADR-0015](../adr/0015-apache-licensing-sponsorship.md) |
| DEC-011 | Collect no telemetry. | Accepted | [ADR-0014](../adr/0014-telemetry.md) |
| DEC-012 | Treat `PortAtlas` as a working title and block public namespace release pending clearance. | Accepted | [ADR-0023](../adr/0023-working-name-collision-trademark-clearance.md) |
| DEC-013 | Use `psutil` with a tested `lsof -nP` fallback and validation path. | Accepted direction; runtime fidelity evidence due Gate 4 | [ADR-0003](../adr/0003-host-collector.md) |
| DEC-014 | Use Docker SDK API negotiation and degrade cleanly when Docker is absent. | Accepted direction; integration evidence due Gate 4 | [ADR-0004](../adr/0004-docker.md) |
| DEC-015 | Use Radix accessibility primitives, TanStack Table, and React Query-driven server state. | Accepted | [ADR-0006](../adr/0006-ui-primitives.md) |
| DEC-016 | Research PyInstaller and a native background-service model before choosing packaging details. | Proposed research direction; acceptance due Gate 9 | [ADR-0007](../adr/0007-packaging.md) |
| DEC-017 | Use a generated high-entropy local token, one-time browser bootstrap, HttpOnly SameSite session, and scoped bearer credentials for CLI and HTTP MCP. | Accepted contract | [ADR-0011](../adr/0011-auth.md) |
| DEC-018 | Accept the exact Gate 2 product and architecture baseline at revision `e53f39916b2348e8626375bb33cac147e27bd217` and authorize the bounded Gate 3 engineering foundation. | Founder-approved 2026-07-11 | [Gate 2 approval](gate-2-approval.md), [Gate 3 sprint brief](gate-3-sprint-brief.md) |
| DEC-019 | Preserve initial commit `8081f409f54f088d61f9a36433b7e56f2410e66f` unchanged and record a forward founder-approved provenance attestation for its missing sign-off trailer. | Accepted initial-history exception | [Provenance attestation](gate-2-approval.md#provenance-attestation-for-the-root-commit) |
| DEC-020 | Limit Gate 3 packaging work to a research spike; defer package selection, distributable builds, signing, notarization, service lifecycle, and packaging acceptance to Gate 9. | Accepted gate boundary | [Gate 3 `G3-20`](gate-3-sprint-brief.md#evidence-bound-work-items), [ADR-0007](../adr/0007-packaging.md) |
| DEC-021 | Use CPython 3.13.14, uv 0.11.28, Node 24.18.0, and Corepack pnpm 11.10.0 as exact foundation contributor pins; retain Python 3.14.6 in the compatibility matrix. | Accepted Gate 3 implementation input; revalidate at Gate 9 | [Gate 3 evidence](gate-3-evidence.md), [development setup](../operations/development-setup.md) |
| DEC-022 | Use `pyproject.toml` `0.0.0.dev0` as private internal version authority and reject drift across implemented CLI, REST/OpenAPI, and generated-client surfaces without assigning a public product version. | Accepted Gate 3 implementation contract | [Versioning policy](../releases/versioning.md), [Gate 3 evidence](gate-3-evidence.md) |
| DEC-023 | Enforce lock checks, complete advisory/license inventory, matching DCO history, SHA/digest-pinned workflows, pull-request dependency review, and supported Dependabot ecosystems as the Gate 3 supply-chain baseline. | Accepted Gate 3 control; release re-review required | [Security policy](../../SECURITY.md), [Gate 3 evidence](gate-3-evidence.md) |
| DEC-024 | Accept the bounded Gate 3 engineering foundation at exact revision `4adf1fb500b651e425735595db528fd42fffba73` and authorize Gate 4 sprint planning only; do not authorize Gate 4 behavior, public release or publication, namespace claims, or later-gate packaging acceptance. | Founder-approved 2026-07-14 | [Gate 3 evidence](gate-3-evidence.md), [Gate 3 sprint brief](gate-3-sprint-brief.md) |
