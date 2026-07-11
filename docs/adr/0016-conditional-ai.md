# ADR 0016: Conditional AI

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Optional local-AI inclusion in the MVP

## Context

Local models can make structured port evidence easier to query and explain, but model output is probabilistic, consumes substantial resources, and creates secret-leakage, prompt-injection, retention, and authority risks. Port discovery, conflict decisions, reservations, leases, allocation, and policy are deterministic responsibilities. Ollama may be missing, stopped, incompatible, or configured with a cloud-backed model.

## Decision

AI is an optional conditional feature, never a core dependency:

- Core scanning, runtime inventory, project discovery, conflicts, allocation, reservations, REST, CLI, and MCP must install, start, and pass tests with no AI provider present.
- AI is disabled by default.
- The user explicitly enables a provider, chooses an already installed compatible model, and separately approves any model download.
- Ollama is the first provider through ADR 0017. No remote provider or cloud-backed model is enabled automatically.
- MVP AI use cases are read-only natural-language inventory, evidence-grounded conflict explanations, and project summaries.
- AI output is visibly generated, advisory, timestamped, model-identified, schema-validated where machine-readable, and linked to authoritative evidence.
- AI does not create observations, declarations, conflicts, policies, reservations, leases, or assignments.
- Provider absence or failure returns a typed degraded state and cannot interrupt core background work or corrupt authoritative state.
- Model selection is capability-driven. qwen3:4b is an evaluation candidate for the balanced local profile, not a hard-coded dependency or release promise.

Ship AI in the MVP only if all of these gates pass:

- Core tests pass with Ollama absent and disabled.
- ADRs 0017 through 0022 are implemented and security-reviewed.
- Secret-redaction and prompt-injection suites pass.
- Machine-readable output is strictly validated.
- The model cannot access mutating, arbitrary-file, shell, process-control, or unrestricted-network tools.
- Provider failure and cancellation leave core state unchanged.
- Users can inspect status and delete all AI-derived data.
- Resource use and supported model behavior are documented.
- UAT confirms disabling AI leaves every core workflow functional.

If any gate fails, release the MVP without AI rather than weakening the gate.

## Alternatives considered

### Make AI mandatory

This would make deterministic local port management depend on model availability, hardware, license, and output quality.

### Exclude AI from all MVP planning

This reduces scope but risks adding it later through unsafe shortcuts that bypass provider, permission, context, and retention boundaries.

### Use a hosted model

A hosted provider may offer stronger models but sends sensitive local project and process context off the machine and violates the default local-only direction.

### Let the model drive the allocator

Allocation needs reproducible transactional rules and current observations; probabilistic output cannot provide those guarantees.

## Consequences

### Positive

- Core value and safety remain deterministic.
- The architecture contains AI risk before feature pressure arrives.
- Users with suitable local hardware can receive explanations without a required cloud service.
- A failed AI evaluation cannot block the non-AI product release.

### Costs and risks

- Conditional scope creates two tested product configurations.
- Small local models may not meet evidence or injection-resistance thresholds.
- Users may assume local execution is automatically private despite unsafe provider configuration.
- Capability and license checks can invalidate a previously suggested model.

## Verification

- Run the complete core suite on a machine with no Ollama installation.
- Enable, disable, stop, restart, overload, cancel, and misconfigure the provider during active core workflows.
- Attempt every forbidden state mutation through natural language and model output.
- Evaluate hallucination, evidence fidelity, secret leakage, schema adherence, prompt injection, latency, memory, and cancellation on each recommended model digest.
- Verify no model is installed, downloaded, activated, or kept loaded without explicit user action.
- Use network capture to reject cloud-backed model traffic in the local-only profile.

## Revisit triggers

- A model and adapter cannot satisfy the release gates on supported hardware.
- A remote provider is proposed.
- AI-assisted extraction or change planning moves from Version 1 into MVP scope.
- Provider behavior or model licensing changes.
- User research shows optional AI materially confuses the deterministic product.

## Sources

- [Ollama API introduction](https://docs.ollama.com/api/introduction)
- [Ollama authentication and local versus cloud behavior](https://docs.ollama.com/api/authentication)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
