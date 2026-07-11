# ADR 0021: Structured output

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Machine-readable AI response validation

## Context

Provider-side structured output improves formatting but does not establish truth, authorization, evidence, valid paths, or safe ports. Models can emit malformed JSON, extra fields, stale evidence IDs, invalid protocols, out-of-range values, or plausible but invented records. Permissive repair can turn an invalid safety-sensitive response into data the model never actually supplied.

## Decision

Use a strict fail-closed validation pipeline for every machine-readable AI result:

1. Select a versioned Pydantic response model for the typed task.
2. Generate JSON Schema from that model and provide it to capable providers.
3. Apply strict input and output byte limits before parsing.
4. Parse exactly one JSON value; reject surrounding prose, trailing data, non-finite numbers, duplicate-key ambiguity, and malformed encoding.
5. Validate the Pydantic model with strict types and forbidden unknown fields unless the specific versioned contract explicitly allows an extension map.
6. Validate semantic constraints such as port range, protocol, confidence bounds, identifier format, result count, and allowed enum values.
7. Resolve and verify every evidence ID against the current authorized request scope.
8. Canonicalize and validate every path against approved ProjectInstance roots.
9. Re-run relevant deterministic policy and availability checks rather than trusting model conclusions.
10. Mark the result generated, non-authoritative, provider-identified, model-identified, schema-versioned, validation-timestamped, and stale when evidence has changed.
11. Persist only the redacted validated representation allowed by ADR 0019.

Do not automatically repair malformed or schema-invalid output for extraction, change plans, manifests, tool arguments, or other safety-sensitive workflows. Return a typed validation error and leave core state unchanged. A user-facing explanation may use bounded plain text, but facts still require evidence references and output rendering is untrusted.

## Alternatives considered

### Trust provider-enforced JSON Schema

Provider constraints improve generation but do not check domain semantics, authorization, current evidence, or post-generation tampering.

### Parse JSON and ignore unknown fields

This makes schema drift silent and can hide attempted instruction or capability injection.

### Automatically repair invalid JSON

Repair can create meaning not present in the response and encourages accepting unreliable output in sensitive workflows.

### Extract fields with regular expressions

Regex extraction is brittle, loses schema versioning, and cannot express nested typed contracts reliably.

### Free-form text only

Text is appropriate for explanations but cannot safely drive typed candidate or plan workflows.

## Consequences

### Positive

- Invalid output has no effect on authoritative state.
- Provider and application validation are defense in depth.
- Evidence and scope checks prevent plausible invented identifiers from passing.
- Versioned models make stored generated artifacts auditable.

### Costs and risks

- Small models may fail strict schemas more often.
- Semantic validation duplicates some deterministic query work.
- Schema evolution requires explicit compatibility handling.
- Fail-closed errors can reduce perceived AI reliability but preserve safety.

## Verification

- Fuzz malformed JSON, duplicate keys, trailing prose, huge values, deep nesting, invalid Unicode, non-finite numbers, and unknown fields.
- Test stale, missing, cross-project, unauthorized, and invented evidence IDs.
- Test path traversal, symlink escape, invalid protocols, port boundaries, and excessive result counts.
- Force provider schema noncompliance and prove no database mutation, lease, file write, or authoritative record occurs.
- Verify every persisted result records schema, provider, model, evidence, generated status, and validation outcome.
- Run contract tests against every recommended model digest and provider version.

## Revisit triggers

- Pydantic or the provider changes JSON Schema compatibility materially.
- A new result type needs controlled extensibility.
- A model cannot meet release thresholds despite valid schemas and prompts.
- A future mutation workflow proposes consuming generated structures.

## Sources

- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
