# ADR 0018: AI permission boundary

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Model authority, tools, and application access

## Context

A model can misunderstand a request, hallucinate an owner, follow injected repository instructions, or generate unsafe tool arguments. Giving it the user's MCP credential or direct application object access would allow model output to cross from explanation into mutation. Human-facing clients may legitimately have mutating scopes, but that authority must not be inherited by AI orchestration.

## Decision

Treat AI as a distinct least-privilege principal with a fixed read-only capability set:

- AI may read system status, search projects, read project details, query port inventory, read project ports, check availability, request a non-binding suggestion, list and diagnose conflicts, read policies, read evidence, and read recent changes.
- AI cannot register roots, trigger unrestricted scans, reserve or renew leases, release ports, change policy, confirm declarations, ignore conflicts, edit configuration, write files, start or stop processes, access Docker control operations, or alter integrations.
- AI receives no arbitrary file reader, shell, subprocess, network fetch, database connection, process-control interface, or raw MCP bearer credential.
- The orchestrator calls typed application query services through a dedicated internal principal. Tool names and argument schemas are fixed in code, not supplied by repositories, users, or models.
- Canonical approved-root checks, object authorization, argument validation, output limits, call-count limits, wall-clock limits, cancellation, and audit apply independently of model output.
- A model may create a clearly labeled proposal or explanation. Deterministic code must revalidate current evidence and a human must authorize any later mutation through a separate non-AI path.
- Generated suggestions never become observations, exact declarations, conflicts, policies, reservations, leases, or assignments.
- Every factual response cites evidence IDs and carries staleness, provider, model, validation, and generated-content metadata.
- Broader human MCP scopes do not expand this AI allowlist.

## Alternatives considered

### Reuse the invoking user's credential

This is convenient but lets a model inherit mutation power and makes authorization depend on prompt behavior.

### Give the model filesystem and shell tools

This could answer more questions but creates arbitrary code execution and secret-exfiltration paths.

### Permit mutating tools with confirmation

Model-selected arguments remain vulnerable to injection and hallucination even when a confirmation screen exists. The MVP instead separates proposal from deterministic execution.

### Use prompt instructions as the permission boundary

Prompts are advisory to a probabilistic model and cannot replace application authorization.

## Consequences

### Positive

- Model compromise cannot directly mutate authoritative state.
- Tool arguments and project scope remain enforceable by ordinary code.
- Human and AI authority are independently auditable.
- Prompt injection has fewer useful actions to target.

### Costs and risks

- AI cannot complete reservation or change workflows end to end.
- Application query services need safe, minimal response projections.
- Evidence grounding and staleness checks add latency and implementation work.
- Read-only data can still be sensitive and needs minimization.

## Verification

- Enumerate the runtime AI tool registry and compare it exactly with the accepted read-only list.
- Attempt direct and indirect requests for every forbidden capability.
- Inject malicious repository text, tool names, paths, URLs, shell strings, and permission-escalation requests.
- Verify AI execution has no credential, filesystem, subprocess, arbitrary-network, Docker-control, or mutation handle.
- Change evidence after a model response and confirm stale results cannot authorize later action.
- Audit every AI tool call by request ID, tool name, validated arguments, evidence IDs, and outcome without raw prompt storage.

## Revisit triggers

- A future release proposes AI-assisted mutations.
- Application query projections expose more sensitive data than required.
- MCP or provider tool semantics change materially.
- Security evaluation shows a read-only tool can cause side effects.

## Sources

- [MCP 2025-11-25 tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
