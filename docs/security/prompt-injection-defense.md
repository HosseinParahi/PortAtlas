# Prompt-Injection Defense

Status: **Conditional MVP proposal**

## Core rule

All project files, process labels, container metadata, manifest text, user-provided names, and prior model output are untrusted data. Their content cannot change system policy, grant tools, broaden context, or authorize mutation.

## Defense layers

1. **Avoid AI when deterministic logic is sufficient.** Collection, parsing, conflicts, allocation, authentication, and validation never depend on a model.
2. **Minimize context.** Send typed evidence fields and identifiers, not entire files, command lines, environments, or databases.
3. **Redact before prompt construction.** The context builder accepts already-classified fields and fails closed on a redaction error.
4. **Separate instructions from evidence.** Fixed developer instructions define the task; untrusted values are serialized in a clearly labeled data envelope.
5. **Remove mutation and ambient authority.** The provider may select only from a server-defined read-only application-query allowlist executed by the AI orchestrator under existing user and `ProjectInstance` scope. It receives no filesystem, shell, arbitrary network, Docker, MCP, credential, mutation, or tool-registration capability; call count, records, depth, time, and bytes have hard limits.
6. **Constrain output.** Require a versioned JSON schema, bounded strings and arrays, evidence-ID references, and an allowlisted recommendation vocabulary.
7. **Validate semantics.** Reject unknown evidence IDs, forbidden actions, stale revisions, unsafe links, hidden markup, and claims not supported by deterministic state.
8. **Require human action.** A recommendation never becomes a reservation or lease without a normal authenticated command and current-state confirmation.
9. **Isolate failure.** Invalid, hostile, or unavailable AI yields a typed optional-feature error; the authoritative core and browser inventory continue.

## Evaluation categories

- Direct override instructions and role impersonation
- Indirect instructions in filenames, comments, environment values, labels, and manifests
- Encoded, multilingual, fragmented, and quoted injection attempts
- Requests for secrets, full paths, unrelated files, tools, or network calls
- Schema-shaped forbidden actions and fabricated evidence IDs
- Markdown, HTML, URL, and bidirectional-text rendering attacks
- Multi-turn attempts to recover data omitted from current context

The evaluation set includes benign controls so defensive filtering does not make ordinary explanations unusable.

## Monitoring without telemetry

Local counters may record categories such as rejected schema, unknown evidence reference, timeout, or suspected injection. They contain no raw prompt or project content and never leave the device automatically. Users may inspect and clear them.
