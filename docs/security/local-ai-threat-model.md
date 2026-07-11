# Local AI Threat Model

Status: **Conditional MVP proposal; disabled unless every gate passes**

Running a model locally reduces third-party transmission but does not make the workflow private, accurate, or safe. Ollama, model files, prompts, project content, and generated output form a separate untrusted subsystem.

## Assets and adversaries

Assets include project metadata, paths, process and container evidence, allocation state, model prompts, structured responses, and user trust. Adversarial inputs may come from a malicious repository, dependency file, container label, process name, model artifact, compromised local provider, or indirect prompt injection embedded in ordinary text.

## Threats and mandatory controls

| ID | Threat | Mandatory control | Fail-closed behavior |
|---|---|---|---|
| AI-THR-001 | Context contains a credential or proprietary content unrelated to the question. | Field allowlist, minimization, secret redaction, visible preview, explicit invocation. | Do not call provider. |
| AI-THR-002 | Project content tells the model to ignore policy or request broader tools. | Quote as untrusted evidence, fixed instruction hierarchy, injection detector/evaluation, and only a server-defined read-only query allowlist with hard call and scope limits. | Reject or label result unsafe. |
| AI-THR-003 | Model invents a port owner, conflict, or remediation. | Ground output to supplied evidence IDs, strict schema, semantic validation, deterministic source links. | Return deterministic view only. |
| AI-THR-004 | Structured output is syntactically valid but requests forbidden mutation. | Allowlisted recommendation actions; reservations remain explicit application commands with user confirmation. | Reject action field. |
| AI-THR-005 | Ollama is unavailable, slow, or returns excess output. | Short timeouts, cancellation, size limits, separate worker budget and circuit breaker. | Core remains healthy; show conditional feature unavailable. |
| AI-THR-006 | Prompt or response persists in logs, backups, or diagnostics. | Ephemeral default, classified fields, AI-specific redaction and export exclusion. | Block export on canary detection. |
| AI-THR-007 | Model selection silently downloads or reaches a network. | No automatic model pull; explicit local endpoint and model presence check; no provider fallback. | Feature remains disabled. |
| AI-THR-008 | Model output manipulates UI through Markdown or links. | Render as inert structured text with URL policy and escaping. | Strip unsupported content. |
| AI-THR-009 | Repeated AI requests exhaust CPU, memory, or battery. | User-initiated requests, concurrency one by default, resource and queue limits, cancel control. | Reject excess requests safely. |

## Authority boundary

AI never determines authoritative state, allocates a port, edits a file, launches or terminates a process, invokes Docker, selects credentials, or bypasses validation. For approved question types, the orchestrator may execute a fixed set of read-only application queries under the user's existing scope and return bounded structured results to the model. The model cannot register tools, call MCP, access arbitrary application services, or change the allowlist. It may summarize already-authorized evidence or propose a structured plan. A user action still calls the deterministic application service with current revisions and normal authorization.

## Inclusion gate

Ollama is included in MVP only when privacy canaries, redaction, prompt-injection resistance, schema and semantic validation, deterministic grounding, performance, cancellation, and failure-isolation thresholds all pass on the documented evaluation set. Any failed mandatory category excludes AI from the release without blocking the core product.
