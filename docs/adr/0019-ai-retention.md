# ADR 0019: AI retention

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Prompt, response, metadata, summary, export, and deletion policy

## Context

Prompts and model context may reveal project names, paths, process facts, code snippets, or secrets missed by redaction. Complete model responses can reproduce that data. Retaining raw conversations by default would create a new sensitive local archive unrelated to the deterministic audit trail.

## Decision

Minimize AI persistence by default:

- Do not persist raw prompts, raw constructed context, model conversation history, hidden reasoning, or complete raw responses.
- Keep request content in memory only for the bounded request lifetime and release references on completion, cancellation, or failure.
- Persist a redacted metadata record containing request ID, task category, provider and model identity, model digest when available, schema version, timestamps, duration, outcome, token or byte counts, evidence IDs, validation status, redaction counts, and error category.
- Metadata follows the initial seven-day local history retention policy and is configurable.
- Do not store generated summaries automatically. A user may explicitly enable summary storage or save a validated generated artifact.
- Persist only the redacted, validated artifact selected by the user, its evidence references, model metadata, creation time, and invalidation state; never persist hidden reasoning.
- Mark a stored result stale when referenced evidence changes. Stale results cannot be reused as current facts without regeneration.
- Provide one local control to delete all AI-derived metadata, summaries, saved artifacts, caches, and future embedding indexes.
- Exclude AI-derived data from backup, export, and diagnostic bundles unless the user selects it. Even when selected, apply redaction and preview.
- Never place raw AI content in logs, traces, test snapshots, crash reports, or audit event details.

Deletion is transactional and auditable by category and count, without retaining the deleted content in the deletion audit record.

## Alternatives considered

### Store complete conversations

This improves conversational continuity but creates a high-value archive and complicates invalidation, export, and deletion.

### Store every complete response but not prompts

Responses can echo prompt and context content, so this does not solve the main privacy risk.

### Store nothing

This minimizes risk but removes useful provider health, validation, latency, evidence, and deletion audit metadata.

### Unlimited retention because storage is local

Local data is still vulnerable to malware, backups, support bundles, shared accounts, and device loss.

## Consequences

### Positive

- Default storage contains no raw conversation corpus.
- Evidence and model metadata remain available for evaluation and troubleshooting.
- Users deliberately choose which generated artifacts persist.
- One purge control makes the privacy promise testable.

### Costs and risks

- Conversations do not automatically continue after a request or restart.
- Support investigations have less raw reproduction material.
- Redaction failures can still affect explicitly saved artifacts.
- Secure deletion guarantees depend on filesystem and backup behavior and must be described honestly.

## Verification

- Inspect the database, logs, traces, caches, crash output, backups, exports, and diagnostics after representative AI requests.
- Inject canary secrets into rejected context and prove they are absent from persistent stores and snapshots.
- Test seven-day metadata expiry, configurable retention, summary opt-in, explicit save, evidence invalidation, and provider failure.
- Run the purge operation and verify all AI-derived tables, files, indexes, and caches are empty while deterministic state remains intact.
- Verify deletion audit records contain counts and request metadata only.
- Document filesystem and backup limits on guaranteed physical erasure.

## Revisit triggers

- A conversation-memory feature is proposed.
- Team/server mode changes retention or deletion ownership.
- Legal or distribution requirements change local data handling.
- An evaluation requirement cannot be met with redacted metadata.
- Embeddings advance under ADR 0020.

## Sources

- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Ollama usage metadata](https://docs.ollama.com/api/usage)
