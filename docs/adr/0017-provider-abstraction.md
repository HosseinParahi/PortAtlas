# ADR 0017: Provider abstraction

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Local-model provider protocol and Ollama adapter

## Context

The product needs to test and isolate model availability, capability, cancellation, timeouts, and failures without importing provider details into domain logic. Ollama is the first supported provider, but its API is not strictly versioned and now exposes both local and cloud-backed models. Hard-coding one model or assuming every installed model supports tools and schemas would be unsafe.

## Decision

Define a typed AIProvider protocol behind the optional-AI orchestrator:

- Operations cover health, provider version, model listing, model metadata, capability probing, chat completion, structured completion, embedding generation for future use, cancellation, and keep-alive control.
- Provider types return provider-neutral errors and metadata. They do not receive repositories, domain entities, credentials, or tool authority directly.
- The context builder supplies a bounded redacted task packet; the orchestrator validates output before any application consumer sees it.
- The first adapter targets Ollama at http://127.0.0.1:11434 by default.
- Endpoint configuration is explicit and accepts loopback by default. Non-loopback or authenticated remote endpoints require a visible warning and a future remote-provider security decision.
- Detect and reject cloud-backed models in the MVP local-only profile. A local Ollama endpoint does not by itself prove local inference.
- Do not install Ollama, sign in, create credentials, pull models, or activate models automatically.
- Use bounded input and output, strict connect and request timeouts, cancellation propagation, one concurrent generation by default, safe transient retry only, and a circuit breaker after repeated failure.
- Never run provider I/O on the API event loop.
- Record provider version, model name, digest when available, capabilities, schema version, and timing with each validated result.
- qwen3:4b may be offered only as a benchmarked balanced-profile candidate after current capability, resource, availability, and license checks. Any compatible installed model may be selected.

The provider protocol may gain additional local adapters later without changing deterministic application services.

## Alternatives considered

### Call Ollama directly from API handlers

This is fast to prototype but spreads provider failure, timeout, and response assumptions across the product.

### Implement only an OpenAI-compatible interface

Compatibility endpoints can reduce code but may omit model discovery, digest, keep-alive, embeddings, or provider-specific capability information needed for a safe local UX.

### Hard-code one model

Model availability, license, hardware requirements, and structured-output behavior change. A capability profile is more durable.

### Support cloud providers in the first adapter

This expands privacy, credentials, billing, retention, and network scope beyond the approved local-first MVP.

## Consequences

### Positive

- Provider outages and malformed responses stay outside core state.
- Fake providers can exercise every failure path deterministically.
- Model recommendations can evolve without changing domain code.
- Local versus cloud behavior is an explicit policy decision.

### Costs and risks

- A common protocol can hide provider-specific capabilities if made too generic.
- Capability probing adds startup and UX complexity.
- Ollama API compatibility still needs versioned tests.
- Determining whether a model executes locally may require provider metadata that changes.

## Verification

- Run adapter contract tests against a fake server covering success, invalid JSON, timeout, slow stream, cancellation, disconnection, model missing, restart, and unsupported capabilities.
- Test supported Ollama versions and record the version matrix.
- Verify one-concurrent-request behavior, queue bounds, circuit opening, backoff, and recovery.
- Confirm no automatic installation, sign-in, model pull, cloud request, or non-loopback connection occurs.
- Compare recorded model digest and capability probe with the response metadata.
- Run core-state isolation tests while the provider fails mid-stream.

## Revisit triggers

- A second local provider is approved and exposes a missing protocol capability.
- Ollama changes API stability, model locality metadata, or authentication behavior.
- A remote provider is proposed.
- Capability probing cannot reliably distinguish safe local operation.

## Sources

- [Ollama API introduction](https://docs.ollama.com/api/introduction)
- [Ollama model listing API](https://docs.ollama.com/api/tags)
- [Ollama API errors](https://docs.ollama.com/api/errors)
- [Ollama authentication](https://docs.ollama.com/api/authentication)
