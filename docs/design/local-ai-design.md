# PortAtlas Optional Local AI Design

## Decision

Local AI is conditional, implemented after deterministic MVP capabilities, disabled by default, and included in an MVP release only when every security and evaluation gate passes. Ollama is the first provider behind an internal provider protocol. Core behavior never depends on an LLM.

The deterministic authority boundary includes:

- host and Docker collectors;
- focused project parsers;
- ProjectInstance identity;
- registry state;
- reservations and leases;
- allocator;
- conflict and policy engines;
- permission and audit systems.

AI output is generated advisory material. It may cite authoritative records but cannot create, renew, release, suppress, or promote them.

## Eligible MVP capabilities

- Natural-language read-only inventory questions.
- Grounded conflict explanations.
- Grounded ProjectInstance summaries.
- Structured extraction candidates from a minimal redacted unsupported source, only if the extraction gate passes.
- Compact safe context packets for a human or external agent.

The following remain unavailable:

- mutating tools;
- arbitrary file reads;
- arbitrary shell or network access;
- process or Docker control;
- lease and reservation authority;
- direct source-file edits;
- autonomous launch;
- global client configuration edits;
- unrestricted model-driven tool loops;
- embeddings in the MVP.

## Architecture

~~~mermaid
flowchart LR
    CLIENT[UI, API, or approved internal caller]
    APP[AI application use case]
    PERM[Capability and project consent]
    QUERY[Read-only application queries]
    CTX[Context builder and redactor]
    PROVIDER[AI provider interface]
    OLLAMA[Ollama adapter]
    VALID[Strict output and evidence validator]
    RESULT[Advisory AIAssistanceResult]

    CLIENT --> APP
    APP --> PERM
    PERM --> QUERY
    QUERY --> CTX
    CTX --> PROVIDER
    PROVIDER --> OLLAMA
    OLLAMA --> VALID
    VALID --> RESULT
~~~

The provider has no repository, database, allocator, MCP mutation, shell, Docker, or process handle. It receives only a completed redacted context packet.

## Authority rules

1. Runtime availability is answered by deterministic application queries.
2. Conflict records exist before an AI explanation is requested.
3. Suggested ports come from the allocator, not the model.
4. Evidence IDs in generated output must resolve to the supplied context.
5. AI extraction candidates remain AI suggested and unconfirmed.
6. Explicit user confirmation invokes a separate deterministic command.
7. Provider failure or invalid output commits no authoritative transaction.
8. Repository text and model output cannot alter system policy or tool permissions.

## Request types

### Natural-language inventory

Input is a bounded user question plus explicit ProjectInstance or global read scope. A deterministic intent router first tries supported direct patterns. If AI is used, it can select only from a fixed read-only internal query allowlist:

- get system status;
- search projects;
- get ProjectInstance details;
- query port inventory;
- get project ports;
- check availability;
- get allocator suggestion;
- list and diagnose conflicts;
- get policies;
- get evidence;
- get recent changes.

Maximum tool calls, total records, wall-clock time, and output bytes are fixed by configuration within hard server limits.

### Conflict explanation

Context includes a deterministic Conflict projection, safe member summaries, evidence IDs, effective policy, allocator-produced alternatives, freshness, and uncertainty. Output explains what conflicts, why it matters, exposure implications, safe alternatives, and available reviewed actions. It cannot invent an owner or mark an action safe.

### ProjectInstance summary

Context includes stack metadata, services, separated port states, conflicts, exposure concerns, policy, evidence freshness, and unknowns. Every factual statement must cite one or more supplied evidence IDs or resource IDs.

### Assisted extraction

This capability is independently gated and may be excluded even if explanations ship. It accepts one minimal redacted snippet from an approved root after deterministic parsers report unsupported syntax. Output is a strict list of candidates with source evidence, confidence, and rationale. Candidates never become exact declarations without deterministic verification or user confirmation.

## Request lifecycle

~~~mermaid
sequenceDiagram
    participant U as User
    participant A as AI use case
    participant Q as Deterministic queries
    participant C as Context builder
    participant P as Provider
    participant V as Validator

    U->>A: Request advisory assistance
    A->>A: Check feature, capability, consent, and scope
    A->>Q: Fetch minimum authoritative records
    Q-->>A: Typed records and freshness
    A->>C: Build bounded redacted packet
    C-->>A: Packet and preview metadata
    A->>P: Structured completion with deadline
    P-->>A: Provider output and model metadata
    A->>V: Parse, schema, semantics, and evidence checks
    alt valid
        V-->>A: Valid advisory result
        A-->>U: Generated result with evidence and warnings
    else invalid or unavailable
        V-->>A: Typed AI error
        A-->>U: Core-safe failure and deterministic fallback
    end
~~~

## User consent and privacy

Before enabling AI, the UI explains:

- the configured provider is local by default but data minimization still applies;
- repository content can contain prompt injection;
- PortAtlas redacts and bounds context;
- models consume disk, memory, CPU, GPU, and battery;
- model licenses and capabilities vary;
- model download requires explicit action outside an automatic request;
- AI output may be wrong and is non-authoritative;
- disabling AI leaves core functionality unchanged.

Consent is capability-specific and can be revoked per ProjectInstance. A context preview shows categories, counts, evidence IDs, redactions, and size, not secret-bearing raw text.

## Retention

Defaults:

- raw prompts are not stored;
- conversation history is not stored;
- complete provider responses are not stored unless a user saves a validated artifact;
- request metadata, provider and model identity, timing, result status, context categories, and evidence IDs may be stored;
- assistance results expire by policy;
- results are invalidated when referenced evidence revisions change;
- AI-derived data is excluded from normal export;
- one action deletes all AI-derived data.

## Resource controls

- maximum one concurrent request by default;
- bounded queue with rejection rather than unbounded wait;
- explicit request deadline and cancellation;
- context byte and token budgets;
- bounded provider output;
- model keep-alive control;
- no indefinite retry;
- circuit breaker after repeated transient failures;
- background analysis disabled;
- future battery or charging policy remains opt-in.

## Failure behavior

| Condition | Behavior |
| --- | --- |
| AI disabled | Return AI_DISABLED and deterministic alternatives |
| Ollama absent or stopped | Mark provider unavailable; do not affect other modules |
| Endpoint is non-loopback without explicit secure profile | Reject configuration |
| Model missing | Return AI_MODEL_NOT_FOUND; never pull automatically |
| Model loading or out of memory | Bounded timeout or provider error; apply backoff |
| Invalid JSON or schema | Reject without repair in machine-readable workflows |
| Unsupported tool request | Deny, record safe metadata, and end request |
| Cancellation | Propagate to provider where possible and discard late result |
| Evidence changes during request | Mark stale or reject before persistence |
| Secret detected after context construction | Reject context and record redaction failure count |

The UI message is:

> Local AI is unavailable. Core scanning, conflict detection, allocation, reservations, MCP tools, and project management remain fully operational.

## Security gates

The capability ships only when:

- disabled-by-default behavior is tested;
- no-Ollama core suite passes;
- context minimization and secret redaction tests pass;
- prompt-injection fixtures cannot change tool policy;
- strict output and evidence validation pass;
- AI has no mutation, arbitrary file, shell, process, or Docker access;
- provider failure cannot corrupt core state;
- all AI-derived data can be deleted;
- generated output is visibly labeled;
- model choice remains optional;
- local resource impact and licenses are documented;
- UAT proves disabling AI leaves all core workflows functional.

## Evaluation

Release evaluation measures:

- query and tool-selection accuracy;
- schema adherence;
- conflict explanation fidelity;
- evidence-reference precision;
- hallucinated owner, project, and port rate;
- secret leakage rate;
- prompt-injection resistance;
- latency and cancellation;
- memory and storage impact;
- model-license suitability.

A recommended model profile is selected through dated benchmark evidence. No model name is a permanent product default.

## Future capabilities

Version 1 may add opt-in local embeddings, semantic search, change-plan proposals, manifest proposals, confirmed correction memory, and reproducible benchmarks. These continue to use safe metadata, per-project consent, model-version provenance, deletion controls, and deterministic revalidation.
