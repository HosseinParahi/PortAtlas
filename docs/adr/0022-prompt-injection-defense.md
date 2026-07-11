# ADR 0022: Prompt-injection defense

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Direct and indirect instructions in AI-visible data

## Context

Repositories, README files, source comments, logs, process arguments, container labels, issue text, configuration values, tool results, and model output can contain instructions aimed at a model. This content is data to analyze, not policy. Prompt wording or keyword blocking alone cannot reliably prevent direct, indirect, encoded, multi-turn, or tool-targeted injection.

## Decision

Use architectural least privilege and structured context as the primary defense:

- System policy and the ADR 0018 read-only tool allowlist are fixed by trusted code.
- Repository and runtime content never defines, extends, renames, or configures model tools or permissions.
- The context builder selects the minimum authorized evidence, applies byte and token limits, redacts secrets, assigns stable evidence IDs, and marks every external segment as untrusted data.
- Encode or delimit policy, user task, trusted structured facts, and untrusted text as separate fields. Never concatenate repository text into system or tool instructions.
- Ignore instructions found in analyzed content, including claims that they are system, developer, administrator, security, or tool messages.
- Validate every tool argument independently against typed schemas, approved roots, object authorization, and call budgets.
- Expose no arbitrary shell, subprocess, file reader, URL fetcher, network client, process-control, Docker-control, or mutation tool to AI.
- Apply input and output secret detection. A detection warning can block or reduce context, but pattern detection is not the permission boundary.
- Treat model output as untrusted. ADR 0021 validates structured output; rendered text escapes or sanitizes active markup and does not auto-fetch model-supplied links or images.
- Bound tool-call count, request duration, nested retrieval, context growth, and output size. Do not permit recursive autonomous tool loops.
- Audit injection blocks and tool-validation failures with safe metadata, not raw malicious or secret-bearing content.
- Maintain adversarial fixtures for direct, indirect, obfuscated, encoded, multilingual, README, code-comment, container-label, tool-output, and cross-project attacks.

No model, guardrail model, or prompt classifier may relax these deterministic controls.

## Alternatives considered

### Rely on a strong system prompt

Models can still follow instructions embedded in untrusted content; a prompt is not an authorization mechanism.

### Block suspicious keywords

Patterns help detect common attacks but are bypassed by encoding, paraphrase, typoglycemia, multilingual text, and indirect tool manipulation.

### Give the model broad tools and ask for confirmation

Confirmation does not make injected arguments or data access safe and can mislead users with plausible explanations.

### Use a second guardrail model as the boundary

A guardrail model is also probabilistic and injection-prone. It may be an additional signal but cannot replace fixed permissions and validation.

### Avoid showing repository text to AI entirely

This is safest but prevents approved summary and future extraction use cases. Minimal redacted context plus read-only authority provides a narrower usable boundary.

## Consequences

### Positive

- Successful instruction manipulation still has no mutation or arbitrary-execution path.
- Context provenance and evidence remain inspectable.
- Defenses apply across model families rather than relying on model behavior.
- Adversarial cases become release tests.

### Costs and risks

- Context construction and rendering require dedicated security code.
- Some useful content will be omitted or blocked conservatively.
- Prompt injection cannot be claimed solved; only impact can be constrained.
- New tool or content types require explicit threat review.

## Verification

- Run direct, indirect, encoded, obfuscated, multilingual, multi-turn, README, source-comment, process-argument, container-label, and tool-output injection suites.
- Attempt to redefine policy, add tools, expand roots, expose secrets, fetch URLs, run shell commands, mutate state, and reveal hidden instructions.
- Verify system policy and tool registry hashes do not depend on repository content.
- Confirm malicious Markdown, HTML, image references, and links cannot execute or trigger network requests when rendered.
- Canary-test pre-context and post-output secret detection.
- Require the adversarial suite and manual security review for every new AI tool or context source.

## Revisit triggers

- AI gains a new tool, content source, persistent memory, or provider.
- Research identifies an attack class not represented by current fixtures.
- A future release proposes mutation or arbitrary repository reading.
- Output rendering or browser policy changes.

## Sources

- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
