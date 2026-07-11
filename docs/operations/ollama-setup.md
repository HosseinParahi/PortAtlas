# Ollama Setup Contract

Status: **Conditional proposal; not an MVP installation instruction**

Ollama integration is disabled by default and implemented last. PortAtlas does not install Ollama, start a provider, download a model, accept a remote provider by default, or make AI a prerequisite for core operation.

## Preconditions for a future setup flow

- The founder has approved AI inclusion after the full evaluation gate.
- A compatible Ollama version and loopback API contract have been reverified.
- The user has independently installed and started Ollama and explicitly selected a locally present model.
- PortAtlas can show provider identity, model identifier, context and resource expectations, privacy behavior, and retention before enablement.

## Proposed enablement

1. User opens AI settings and sees the feature as conditional and non-authoritative.
2. PortAtlas probes only the configured loopback endpoint with a short timeout.
3. It lists locally available models without downloading anything.
4. User selects a model and reviews context, redaction, retention, and resource disclosures.
5. A safe synthetic structured-output check validates compatibility.
6. User explicitly enables the feature; core behavior is unchanged.

No provider credential is needed for the loopback Ollama profile. If a future provider requires credentials or remote transmission, it requires a separate ADR, privacy model, consent flow, and release gate.

## Disable and remove

Disabling AI cancels queued requests, prevents new provider calls, and retains only data allowed by the selected local retention policy. PortAtlas never deletes user-owned Ollama models or changes the provider installation.

## Verification

The future guide must include tested version ranges, exact health expectations, model compatibility evidence, timeouts, cancellation, unavailable and restart behavior, and proof that no model pull or network fallback occurs.
