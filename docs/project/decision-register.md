# Decision Register

This register is a compact index. Architecture rationale and consequences live in the linked ADRs.

| ID | Decision | Status | Source of truth |
|---|---|---|---|
| DEC-001 | Use a native Python modular monolith serving a React browser UI; revisit Tauri in Version 1. | Accepted | [ADR-0001](../adr/0001-runtime-architecture.md), [ADR-0007](../adr/0007-packaging.md) |
| DEC-002 | Use SQLite by default through SQLAlchemy repositories and offer PostgreSQL as an optional compatibility profile. | Accepted | [ADR-0002](../adr/0002-persistence.md) |
| DEC-003 | Target macOS and one OS user for MVP while retaining Linux and Windows adapter contracts. | Accepted | [SRS constraints](../requirements/assumptions-and-constraints.md) |
| DEC-004 | Represent each checkout or worktree as a `ProjectInstance` beneath one logical `Project`. | Accepted | [ADR-0008](../adr/0008-project-identity.md) |
| DEC-005 | Limit MVP mutation to reservations and atomic leases. | Accepted | [ADR-0009](../adr/0009-allocator-and-mutation-boundary.md) |
| DEC-006 | Use the locked focused deterministic parser set. | Accepted | [Scanner design](../design/scanners.md) |
| DEC-007 | Use versioned REST commands and SSE browser updates. | Accepted | [ADR-0005](../adr/0005-server-sent-events.md), [REST contract](../design/rest-api.md) |
| DEC-008 | Support MCP over STDIO and authenticated loopback Streamable HTTP against revision 2025-11-25. | Accepted | [ADR-0013](../adr/0013-mcp-transports.md) |
| DEC-009 | Include Ollama in MVP only if all AI privacy, safety, validation, and isolation gates pass. | Conditional | [ADR-0016](../adr/0016-ai-inclusion-policy.md) |
| DEC-010 | License contributions and releases under Apache-2.0, allow commercial use without payment, and make sponsorship voluntary. | Accepted | [ADR-0015](../adr/0015-apache-licensing-and-sponsorship.md) |
| DEC-011 | Collect no telemetry. | Accepted | [ADR-0014](../adr/0014-telemetry.md) |
| DEC-012 | Treat `PortAtlas` as a working title and block public namespace release pending clearance. | Accepted | [ADR-0023](../adr/0023-working-name-collision-and-trademark-clearance.md) |
| DEC-013 | Use `psutil` with a tested `lsof -nP` fallback and validation path. | Proposed for Phase 3 confirmation | [ADR-0003](../adr/0003-host-collector.md) |
| DEC-014 | Use Docker SDK API negotiation and degrade cleanly when Docker is absent. | Proposed for Phase 3 confirmation | [ADR-0004](../adr/0004-docker-integration.md) |
| DEC-015 | Use Radix accessibility primitives, TanStack Table, and React Query-driven server state. | Proposed for Phase 3 confirmation | [ADR-0006](../adr/0006-ui-primitives.md) |
| DEC-016 | Research PyInstaller and a native background-service model before choosing packaging details. | Proposed | [ADR-0007](../adr/0007-packaging.md) |
| DEC-017 | Use a generated high-entropy local token, one-time browser bootstrap, HttpOnly SameSite session, and scoped bearer credentials for CLI and HTTP MCP. | Accepted contract | [ADR-0011](../adr/0011-local-authentication.md) |
