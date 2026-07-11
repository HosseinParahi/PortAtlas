# Architecture Decision Records

This directory is the decision log for the PortAtlas working-title project. The records describe choices approved at the architecture gate, the evidence needed to verify them, and the conditions that require another decision.

## Status vocabulary

- **Accepted**: approved and binding until superseded.
- **Proposed**: a preferred direction that still requires the named evidence or approval.
- **Proposed / Blocking**: unresolved and blocks the release activity identified by the record.
- **Superseded**: replaced by a later ADR that links back to the original.

Changing an accepted decision requires a new ADR. Existing ADRs remain immutable except for corrections that do not alter the decision.

## Index

| ADR | Subject | Status | Decision summary |
| --- | --- | --- | --- |
| [0001](0001-runtime-architecture.md) | Runtime architecture | Accepted | Native Python modular monolith with a browser UI and adapter boundaries |
| [0002](0002-persistence.md) | Persistence | Accepted | SQLite by default through SQLAlchemy, with PostgreSQL compatibility |
| [0003](0003-host-collector.md) | Host collector | Accepted | Host-native collector abstraction with macOS first |
| [0004](0004-docker.md) | Docker | Accepted | Optional read-only Docker Engine integration |
| [0005](0005-sse.md) | SSE | Accepted | REST snapshots plus Server-Sent Events invalidation stream |
| [0006](0006-ui-primitives.md) | UI primitives | Accepted | TanStack Query, Radix Primitives, and TanStack Table |
| [0007](0007-packaging.md) | Packaging | Proposed | Research a PyInstaller-packaged native service; defer Tauri |
| [0008](0008-project-worktree-identity.md) | Project/worktree identity | Accepted | Project groups multiple worktree-aware ProjectInstance records |
| [0009](0009-allocator.md) | Allocator | Accepted | Deterministic policy-aware probing with atomic database leases |
| [0010](0010-manifest.md) | Manifest | Accepted | Versioned optional .portatlas.yaml, gated by name clearance |
| [0011](0011-auth.md) | Auth | Accepted | User-only root secret, browser bootstrap session, scoped bearer clients |
| [0012](0012-mcp.md) | MCP | Accepted | Shared MCP adapter with STDIO and authenticated loopback Streamable HTTP |
| [0013](0013-plugin-boundary.md) | Plugin boundary | Accepted | Stable internal extension contracts; no third-party in-process plugins in MVP |
| [0014](0014-telemetry.md) | Telemetry | Accepted | No external telemetry; local diagnostics only |
| [0015](0015-apache-licensing-sponsorship.md) | Apache licensing/sponsorship | Accepted | Apache-2.0 with unconditional commercial use and voluntary sponsorship |
| [0016](0016-conditional-ai.md) | Conditional AI | Accepted | Optional local AI ships only after safety and evaluation gates |
| [0017](0017-provider-abstraction.md) | Provider abstraction | Accepted | Provider protocol with Ollama as the first local adapter |
| [0018](0018-ai-permission-boundary.md) | AI permission boundary | Accepted | AI receives read-only, evidence-grounded capabilities only |
| [0019](0019-ai-retention.md) | AI retention | Accepted | No raw prompt or complete-response persistence by default |
| [0020](0020-embeddings-deferral.md) | Embeddings deferral | Accepted | Embeddings deferred to an opt-in Version 1 evaluation |
| [0021](0021-structured-output.md) | Structured output | Accepted | Strict schema and semantic validation with fail-closed behavior |
| [0022](0022-prompt-injection-defense.md) | Prompt-injection defense | Accepted | Repository content is untrusted data behind fixed policy and tool allowlists |
| [0023](0023-working-name-collision-trademark-clearance.md) | Working-name collision/trademark clearance | Proposed / Blocking | PortAtlas cannot become the release name until formal clearance |

## Record structure

Every record contains context, the decision, alternatives, consequences, verification, revisit triggers, and primary or authoritative sources. Verification criteria are part of the decision: implementation is not conformant merely because it uses the named technology.

The date on these initial records is 2026-07-11. External standards and product documentation were checked against the versions or revisions named in the individual ADRs.
