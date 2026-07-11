# AI Structured Output and Evidence Validation

## Objective

Machine-readable AI output is accepted only after strict syntax, schema, semantic, scope, and evidence validation. Valid output remains non-authoritative. Invalid output produces a typed error and changes no core state.

## Schema ownership

Pydantic response models define task schemas and generate JSON Schema supplied to the provider. Each schema has:

- stable schema ID;
- integer version;
- task type;
- additional fields rejected unless explicitly allowed;
- bounded strings and arrays;
- enumerations for protocols, confidence, and action types;
- no free-form path, tool, shell, permission, endpoint, or secret fields.

Provider-specific schema adaptation must preserve constraints. The canonical validator always applies the PortAtlas model after provider output returns.

## Validation pipeline

~~~mermaid
flowchart TD
    RAW[Bounded provider bytes]
    JSON[Strict JSON parse]
    SCHEMA[Pydantic and JSON Schema validation]
    SEM[Semantic constraints]
    SCOPE[ProjectInstance and path scope]
    EVID[Evidence and revision validation]
    POLICY[Authority and action policy]
    REDACT[Post-output secret scan]
    RESULT[Non-authoritative assistance result]
    REJECT[Typed AI error; no state change]

    RAW --> JSON
    JSON -->|valid| SCHEMA
    JSON -->|invalid| REJECT
    SCHEMA -->|valid| SEM
    SCHEMA -->|invalid| REJECT
    SEM -->|valid| SCOPE
    SEM -->|invalid| REJECT
    SCOPE -->|valid| EVID
    SCOPE -->|invalid| REJECT
    EVID -->|valid| POLICY
    EVID -->|invalid| REJECT
    POLICY -->|valid| REDACT
    POLICY -->|invalid| REJECT
    REDACT -->|clean| RESULT
    REDACT -->|secret detected| REJECT
~~~

PortAtlas does not permissively repair malformed JSON for extraction, change planning, manifest proposals, or any other machine-readable safety-sensitive workflow. A separate user-visible prose feature may retry once with no untrusted output fed back, but it still cannot create a structured result without a clean validation pass.

## Common response envelope

~~~json
{
  "schema_id": "portatlas.ai.conflict_explanation",
  "schema_version": 1,
  "generated": true,
  "summary": "A native service already occupies the host port declared by another ProjectInstance.",
  "claims": [
    {
      "text": "TCP 8080 is currently observed on a wildcard address.",
      "evidence_ids": ["ctx_ev_1"]
    }
  ],
  "warnings": [
    "Availability can change after this snapshot."
  ]
}
~~~

Provider and model identity, validation status, timestamp, request ID, staleness, and expiration are attached by deterministic application code, not trusted from provider output.

## Task schemas

### Inventory answer

Required:

- concise answer;
- claims array;
- evidence IDs for every factual claim;
- unknowns;
- optional safe follow-up read-only query suggestions from an enumeration.

Forbidden:

- unsupported owner or project;
- port availability without allocator or inventory evidence;
- mutation request;
- arbitrary URL, shell, or path.

### Conflict explanation

Required:

- conflict ID supplied in context;
- summary;
- impact;
- claims with evidence;
- safe alternatives selected from supplied deterministic actions;
- uncertainty and stale-evidence warnings.

Severity, conflict code, action safety, and allocator alternatives must exactly match supplied deterministic values.

### ProjectInstance summary

Required:

- ProjectInstance ID;
- stack and services;
- separated port states;
- conflicts;
- exposure concerns;
- unknowns;
- evidence for every factual list item.

The model cannot merge ProjectInstances or infer an unprovided database listener.

### Extraction candidate

~~~json
{
  "schema_id": "portatlas.ai.extraction_candidates",
  "schema_version": 1,
  "findings": [
    {
      "service_key": "api",
      "port": 8400,
      "protocol": "tcp",
      "namespace": "host",
      "environment_key": "BACKEND_PORT",
      "confidence": 0.72,
      "reason_code": "recognized_server_argument",
      "evidence_ids": ["ctx_ev_3"]
    }
  ]
}
~~~

Constraints:

- port 1 through 65535;
- protocol tcp or udp;
- namespace from allowed enumeration;
- environment key syntax and secret-name checks;
- confidence 0 through 1;
- reason code from enumeration;
- every evidence reference maps to the supplied snippet location;
- status added by application as AI suggested and unconfirmed.

### Future change-plan proposal

The future schema may contain proposed assignment, affected known files, environment keys, Docker mappings, test descriptors, rollback descriptors, risk, and unknowns. Paths must be selected from a deterministic candidate set and content hashes rechecked. The output is not a patch and no apply capability exists in the registry-only MVP.

## Strict JSON parsing

- UTF-8 only.
- One JSON value and no trailing content.
- Maximum byte and nesting limits.
- Duplicate object keys rejected.
- Non-finite numbers rejected.
- No comments or provider-specific wrappers.
- Unknown fields rejected by task schema.
- Strings normalized and bounded.

Markdown code fences around JSON are invalid for machine-readable requests.

## Semantic validation

After schema validation:

- ports and ranges obey domain constraints;
- protocol and namespace combinations are valid;
- resource IDs were present in context;
- conflict code and severity match authoritative projection;
- recommended action IDs are from supplied deterministic options;
- model-proposed scopes do not widen Principal scope;
- no claim asserts absence when context is partial or truncated;
- generated status cannot be false;
- confidence cannot be promoted to exact or user_confirmed;
- source fingerprints match the context snapshot.

## Evidence validation

For every claim:

1. Resolve request-local evidence handle.
2. Verify it belongs to the request and ProjectInstance scope.
3. Verify referenced resource or source exists.
4. Verify revision or fingerprint still matches.
5. Verify evidence allows the claim category.
6. Reject orphaned, duplicate-abusive, stale, or cross-scope references.

If evidence changed after provider invocation, the result is rejected as stale or returned only with an explicit stale status when the task is prose-only and policy allows it. It is never used to create a declaration.

## Authority validation

The validator rejects:

- commands to reserve, renew, release, suppress, patch, launch, or terminate;
- tool or permission definitions;
- arbitrary filesystem paths;
- arbitrary shell commands;
- claims that model output is authoritative;
- requests to ignore system policy;
- unsupported URLs or network operations;
- secret-bearing or credential-shaped output.

Allowed proposed actions are enumeration values that map to application-owned descriptors.

## Persistence result

Only validated redacted output may become AIAssistanceResult. Stored metadata includes:

- result ID;
- task, schema ID, and schema version;
- provider, model, and digest;
- validation status;
- evidence IDs and revisions;
- confidence where meaningful;
- generated and non-authoritative state;
- created and expiration times;
- user-saved flag.

Raw provider bytes and invalid output are discarded after safe diagnostic counters unless an explicit developer test environment captures synthetic data.

## User confirmation

User confirmation:

1. loads the assistance result;
2. rechecks expiration, scope, evidence, source fingerprint, and policy;
3. presents deterministic effect;
4. invokes a separate authorized application command;
5. creates a new authoritative or user-confirmed record with its own provenance;
6. preserves the AI result as historical advisory evidence according to retention.

Confirmation never changes a PortObservation. Runtime facts still require a collector.

## Error outcomes

| Stage | Error |
| --- | --- |
| JSON parse | AI_OUTPUT_INVALID |
| Schema | AI_OUTPUT_INVALID with safe schema issue count |
| Domain semantics | AI_OUTPUT_INVALID |
| Project or path scope | AI_CONTEXT_REJECTED |
| Evidence missing or stale | AI_EVIDENCE_INVALID |
| Unauthorized action | AI_TOOL_REQUEST_DENIED |
| Secret detected | AI_OUTPUT_INVALID and security audit metadata |
| Output limit | AI_OUTPUT_INVALID |

Messages do not echo invalid provider content.

## Evaluation and tests

- valid fixture per schema version;
- malformed JSON and code-fenced JSON;
- duplicate keys and unknown fields;
- deep nesting and oversized strings;
- out-of-range ports and invalid protocols;
- hallucinated evidence IDs;
- cross-ProjectInstance evidence;
- stale resource revision;
- invented severity or action safety;
- permission escalation and tool injection;
- secret and credential output;
- prompt-injection reflection;
- deterministic invalid-output error;
- proof that failure writes no registry, conflict, reservation, lease, policy, or audit mutation beyond safe AI request outcome metadata.
