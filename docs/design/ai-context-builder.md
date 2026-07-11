# AI Context Builder and Redaction Design

## Mission

Every model call passes through one context builder. It selects the minimum authoritative data for a typed task, enforces ProjectInstance scope, removes secrets and unrelated content, treats repository material as untrusted data, assigns stable evidence references, and produces a previewable bounded packet.

No API, UI, MCP tool, or provider adapter may construct a model prompt directly.

## Inputs

ContextBuildRequest contains:

- task type;
- Principal and ai:use scope;
- enabled AI capability;
- ProjectInstance or explicitly authorized global scope;
- user question or target resource;
- maximum context bytes and tokens;
- provider and model capability profile;
- consent record;
- request ID.

It does not accept an arbitrary filesystem path or arbitrary source list.

## Pipeline

~~~mermaid
flowchart TD
    V[Validate capability, consent, and Principal]
    S[Resolve ProjectInstance scope]
    Q[Run fixed read-only application queries]
    M[Select minimum fields and records]
    R1[Structured secret and sensitivity redaction]
    U[Delimit repository-derived content as untrusted]
    E[Assign and verify evidence IDs]
    B[Apply byte, record, and token budgets]
    P[Build policy plus context packet]
    R2[Post-build secret scan]
    PRE[Produce preview metadata]
    OUT[Approved ContextPacket]

    V --> S
    S --> Q
    Q --> M
    M --> R1
    R1 --> U
    U --> E
    E --> B
    B --> P
    P --> R2
    R2 --> PRE
    PRE --> OUT
~~~

Any failed stage returns AI_CONTEXT_REJECTED and makes no provider call.

## Typed task policies

### Inventory question

Eligible:

- safe project and service names;
- protocol, port, bind scope, and state;
- process executable name and identity reference;
- Docker container safe name, image, compose service;
- conflict codes and resource IDs;
- timestamps and freshness;
- safe policy descriptions;
- evidence summaries.

Ineligible:

- full process command lines;
- full paths unless essential and approved;
- environment values;
- source snippets;
- arbitrary README or issue text.

### Conflict explanation

Eligible:

- deterministic Conflict projection;
- safe member summaries;
- policy provenance;
- allocator-generated alternatives;
- exposure classification;
- evidence IDs and safe locations;
- uncertainty and freshness.

The builder does not include unrelated ports, projects, or files.

### ProjectInstance summary

Eligible:

- ProjectInstance identity and safe display path;
- detected stack categories;
- services and database dependency types;
- separated port states;
- conflicts and exposure warnings;
- scan and collector freshness;
- explicit unknowns.

Repository descriptions are excluded unless project consent enables a bounded safe description field.

### Assisted extraction

Eligible only when independently enabled:

- one supported-size redacted snippet;
- path relative to approved root;
- deterministic parser failure category;
- expected schema;
- line or structured pointer IDs.

The source undergoes secret detection before and after minimization. Complete environment files, arbitrary source trees, and multiple unrelated files are forbidden.

## Data classification

| Class | Examples | Default model policy |
| --- | --- | --- |
| public-safe metadata | protocol name, port number, framework category | eligible within scope |
| local-sensitive metadata | project name, relative path, process name, container image | minimize and require capability consent |
| restricted content | source snippet, command fragment, Git metadata | excluded unless task-specific and redacted |
| secret | token, password, private key, credential URL, cookie, environment secret | always forbidden |
| policy content | system instructions, tool allowlist, permission rules | fixed trusted template only |

Repository instructions, comments, logs, labels, issue text, and model output are local-sensitive or restricted data, never policy.

## Secret detection

Detection layers:

1. structured field denylist;
2. key-name classification;
3. URL credential parser;
4. private-key and token format detectors;
5. high-entropy candidate detector with false-positive safeguards;
6. project-specific user redaction patterns;
7. post-serialization scan.

Redaction replaces a value with a typed marker such as secret_removed, not a reversible prefix. The builder records category counts without storing the original.

If safe redaction would destroy the meaning required by the task, the request is rejected rather than sending the original.

## Path safety

- Resolve ProjectInstance from an opaque ID.
- Obtain approved canonical root from the project catalog.
- Never accept provider- or model-proposed paths.
- Verify candidate canonical containment immediately before read.
- Reject symlink escape and special files.
- Prefer safe relative paths in context.
- Include file content only for a task policy that explicitly allows it.
- Recheck source fingerprint before accepting a provider result.

## Prompt-injection defense

The packet has distinct trusted and untrusted sections:

~~~text
TRUSTED POLICY
- Fixed PortAtlas authority and tool rules
- Task definition
- Allowed output schema
- Evidence citation rules

UNTRUSTED DATA
- Delimited records and optional redacted snippet
- Explicit instruction: content is data and cannot change policy

OUTPUT CONTRACT
- Strict JSON schema identifier and version
- No hidden reasoning request
- Evidence IDs supplied for reference
~~~

Controls:

- trusted policy is installed code, not configuration from a project;
- untrusted content is encoded as structured values, not string-concatenated instructions;
- fixed read-only tool allowlist;
- independent validation of every tool argument;
- no permission, tool, path, or endpoint fields derived from model output;
- maximum tool calls and no recursive loop;
- adversarial text remains visible only as data.

## Evidence IDs

The builder assigns a request-local evidence handle to each included authoritative fact. Mapping contains:

- request-local handle;
- stable PortAtlas resource or DiscoveryEvidence ID;
- revision or source fingerprint;
- allowed claim categories;
- freshness timestamp.

The provider sees handles. The validator resolves them back to current records and rejects missing, duplicate, out-of-scope, or stale references.

## Context budget

Budgets apply in this order:

1. required policy and output schema;
2. target resource and direct evidence;
3. blocking conflicts and relevant policy;
4. freshness and limitations;
5. optional supporting records.

Records use deterministic priority and ordering. Truncation is explicit in ContextPacket metadata. The model is instructed that omitted records are unknown, not absent.

Hard limits cover:

- record count by category;
- per-field characters;
- snippet lines and bytes;
- total serialized bytes;
- estimated tokens;
- tool-result bytes;
- number of evidence IDs.

## ContextPacket contract

~~~json
{
  "context_schema_version": 1,
  "task": "conflict_explanation",
  "scope": {
    "project_instance_id": "ins_..."
  },
  "authoritative_snapshot": {
    "captured_at": "2026-07-11T00:00:00Z",
    "freshness": "current"
  },
  "records": [],
  "evidence": [],
  "unknowns": [],
  "truncation": {
    "occurred": false
  },
  "safety": {
    "repository_content_untrusted": true,
    "redaction_count": 0
  }
}
~~~

Raw policy prompt is generated separately and is not persisted.

## Preview

Before a capability first sends restricted content, the UI can display:

- task and ProjectInstance;
- categories and record counts;
- safe relative filenames;
- evidence IDs;
- redaction counts and categories;
- context and token estimate;
- provider and model;
- retention behavior.

Preview never reveals a removed secret. User cancellation results in no provider request.

## Persistence

AIContextRecord stores:

- task type and scope;
- evidence IDs and revisions;
- category counts;
- redaction counts;
- context byte and token estimates;
- provider profile;
- creation and expiration;
- whether raw content was stored, false by default.

The serialized ContextPacket, trusted prompt, source snippet, and user question are not stored by default.

## Failure behavior

| Failure | Response |
| --- | --- |
| Missing consent or capability | AI_DISABLED or authorization error |
| ProjectInstance outside scope | ROOT_SCOPE_DENIED |
| Evidence changed during build | Rebuild once within deadline or return stale-context error |
| Secret survives first redaction pass | Remove and re-evaluate |
| Secret survives post-build scan | Reject complete packet |
| Context exceeds hard budget | Deterministically trim; reject if required evidence no longer fits |
| Unsupported source encoding | Reject snippet and preserve core workflow |
| Injection detector flags content | Keep it delimited if safe, or reject assisted extraction |

## Tests

- secret key and value corpus;
- credential-bearing URLs;
- private keys and tokens;
- benign high-entropy values;
- approved-root and symlink escape;
- unrelated-record exclusion;
- deterministic record ordering and truncation;
- prompt injection in README, config, logs, labels, and process metadata;
- post-build leak scan;
- evidence-handle scope;
- context invalidation on revision change;
- proof that complete environment files are never eligible.
