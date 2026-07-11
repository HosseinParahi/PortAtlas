# AI Data Handling

Status: **Conditional MVP proposal**

## Provider boundary

The MVP candidate provider is a user-configured loopback Ollama service. There is no cloud fallback, automatic model download, remote endpoint default, or provider discovery beyond the configured local address. Provider abstraction exists to isolate the application, not to silently add third-party transmission.

## Context construction

AI context is built from an explicit task, typed evidence IDs, managed status, safe port numbers and protocols, confidence, freshness, and user-selected project labels. It excludes authentication data, environment values other than validated port numbers, raw process arguments, source contents, full home paths, Docker credentials, logs, and unrelated history.

Before sending, PortAtlas shows:

- Provider and model identifier
- Purpose of the request
- Categories and approximate size of included context
- Redaction result and any omitted categories
- Whether result history is enabled
- A cancel action

## Transit and retention

- Requests are allowed only to the configured loopback provider under the MVP contract.
- Raw prompts and provider responses are ephemeral by default.
- The application may retain a validated structured recommendation only when the user enables bounded local history.
- Logs store request ID, provider health, timing, token counts when locally reported, and outcome category, not raw context.
- Backups and diagnostic bundles exclude raw AI material by default.
- Clearing AI history removes eligible structured results and local evaluation artifacts without altering authoritative port state.

## Output handling

Provider output is untrusted. Parse it against a versioned schema, enforce size and vocabulary limits, resolve every evidence reference, escape display text, and discard unknown fields. Invalid output is not partially accepted. No AI response is used as an idempotency key, authorization fact, or concurrency revision.

## Consent and disablement

AI is disabled by default and can be disabled globally even if Ollama is running. Each request is user-initiated unless a later ADR explicitly approves a bounded workflow. Disabling the feature cancels queued work, prevents new provider calls, and leaves deterministic functionality intact.

## Release condition

The feature ships only after the evaluation plan demonstrates zero seeded-secret leakage, no successful forbidden-action escalation, acceptable schema and grounding rates, bounded resource use, accessible disclosure UX, and clean core operation with the provider missing or failing.
