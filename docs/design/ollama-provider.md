# Ollama Provider Adapter Design

## Purpose

Ollama is the first optional local-model provider behind a provider-neutral interface. PortAtlas does not assume Ollama is installed, does not install it, and does not download or activate a model without explicit user action.

The default endpoint is http://127.0.0.1:11434. A non-loopback endpoint is rejected unless a future reviewed security profile explicitly permits it.

## Official API basis

The adapter uses documented Ollama operations for chat, model listing, model inspection, version, running models, and embeddings when the corresponding PortAtlas capability is enabled. The official chat API supports tools, a JSON schema in format, streaming control, and keep_alive; see the [Ollama chat API reference](https://docs.ollama.com/api/chat).

Embeddings are a Version 1 PortAtlas capability and are not invoked in the MVP.

## Provider protocol

~~~python
class AIProvider(Protocol):
    async def health(self) -> ProviderHealth: ...
    async def version(self) -> ProviderVersion: ...
    async def list_models(self) -> list[ModelDescriptor]: ...
    async def inspect_model(self, model: str) -> ModelDescriptor: ...
    async def probe_capabilities(
        self,
        model: str,
        requested: set[Capability],
    ) -> CapabilityReport: ...
    async def complete_structured(
        self,
        request: StructuredCompletionRequest,
        cancellation: CancellationToken,
    ) -> ProviderResponse: ...
    async def embed(
        self,
        request: EmbeddingRequest,
        cancellation: CancellationToken,
    ) -> EmbeddingResponse: ...
~~~

Cancellation and keep-alive are explicit request behavior. The provider does not expose a generic arbitrary-request method to application code.

## Endpoint mapping

| Provider operation | Ollama API |
| --- | --- |
| health | bounded connection plus version request |
| version | GET /api/version |
| list models | GET /api/tags |
| inspect model | POST /api/show |
| list running models | GET /api/ps |
| structured chat | POST /api/chat |
| embeddings, Version 1 | POST /api/embed |

Create, copy, pull, push, and delete model APIs are not exposed through the MVP PortAtlas adapter.

## Configuration

~~~yaml
provider: ollama
endpoint: http://127.0.0.1:11434
assistant_model: null
structured_model: null
fallback_model: null
timeout_seconds: 30
connect_timeout_seconds: 2
max_concurrency: 1
maximum_output_bytes: 262144
keep_alive: 5m
enabled_capabilities: []
~~~

Model names must come from an installed-model discovery result or explicit validated input. PortAtlas never interpolates a model name into a URL or shell command.

## Connection policy

- Parse endpoint as an absolute HTTP URL.
- Default and recommended host is 127.0.0.1.
- Reject user info, fragments, unexpected paths, and ambiguous host syntax.
- Resolve localhost safely and protect against DNS rebinding for future non-literal hosts.
- Disable redirects by default.
- Apply connect, read, total, and idle deadlines.
- Bound response headers and body.
- Do not inherit ambient proxy configuration for loopback unless explicitly approved.
- Use one dedicated asynchronous HTTP client with bounded connections.

Ollama calls are isolated from the API event loop and from authoritative database transactions.

## Health and capability probing

Health distinguishes:

- disabled;
- not installed or connection refused;
- reachable;
- version unsupported;
- model absent;
- model loading;
- capability unverified;
- ready;
- degraded;
- circuit open.

Capability is measured, not inferred solely from model naming. A lightweight explicit test can verify:

- chat response;
- JSON-schema output;
- tool-call shape for read-only orchestration;
- context limit behavior where metadata exposes it;
- embedding support for Version 1.

Capability probes use synthetic non-secret data, bounded output, and user initiation during setup. Results record provider version, model name, model digest when available, probe version, and timestamp.

## Structured completion

The adapter receives:

- fixed system policy;
- delimited redacted context packet;
- expected JSON Schema;
- temperature and safe generation options;
- model;
- keep_alive;
- deadline and cancellation;
- request ID.

It calls /api/chat with stream false for strict machine-readable results, passes the schema through format where supported, and applies bounded generation settings. The adapter returns raw bytes plus provider metadata to the validator. It does not interpret domain meaning.

Thinking or hidden reasoning is not requested for storage or returned to clients. If a model emits a separate thinking field, the adapter discards it before persistence and response mapping.

## Read-only tool mode

When a capability uses tools, the adapter receives a fixed generated list of PortAtlas read-only functions. It:

- rejects unknown tool names;
- validates every argument through application schemas;
- enforces maximum calls and recursion depth;
- executes calls outside the provider adapter through the AI orchestrator;
- returns only bounded structured results;
- never exposes mutating MCP tools;
- ends the request on a permission-change or arbitrary-execution attempt.

The model cannot register tools or modify descriptions.

## Model selection

PortAtlas provides capability-driven profiles:

- lightweight for classification and short summaries;
- balanced for schema-constrained queries and explanations;
- advanced for larger optional reasoning tasks.

An initial qwen3:4b profile may be benchmarked as a candidate, but is not permanently hard-coded. Releases compare currently available small models for schema adherence, evidence fidelity, prompt-injection resistance, latency, memory, platform compatibility, and license suitability.

The user may select any installed compatible model. PortAtlas displays measured capabilities and resource estimates when available.

## Resilience

### Timeouts and cancellation

Cancellation closes or abandons the HTTP request and discards late output. A provider request never holds a registry transaction. Timeout returns AI_TIMEOUT with no authoritative write.

### Retry

Only safe transient connection failures before a response may receive a small bounded retry with jitter. Invalid output, model-not-found, permission, and capability failures are not retried automatically.

### Circuit breaker

Repeated transient failures open a per-profile circuit:

- closed: calls allowed;
- open: fail fast until retry time;
- half-open: one probe call allowed.

Status is visible in UI and local metrics. No infinite background polling occurs.

### Concurrency

Default concurrency is one per provider profile. A bounded queue rejects excess work with retry guidance. Cancellation removes queued work. System status remains responsive during model load.

## Error mapping

| Provider condition | PortAtlas code |
| --- | --- |
| Connection refused or provider stopped | AI_PROVIDER_UNAVAILABLE |
| Endpoint policy rejected | AI_CONTEXT_REJECTED or configuration error |
| Model absent | AI_MODEL_NOT_FOUND |
| Capability probe fails | AI_CAPABILITY_UNSUPPORTED |
| Deadline exceeded | AI_TIMEOUT |
| User cancellation | AI_CANCELLED |
| HTTP resource exhaustion | AI_PROVIDER_UNAVAILABLE with safe subtype |
| Malformed or oversized body | AI_OUTPUT_INVALID |
| Repeated failure backoff | AI_CIRCUIT_OPEN |

Raw provider error bodies are treated as untrusted and are not returned directly.

## Audit and metrics

Safe metadata:

- request ID;
- provider profile and version;
- model name and digest;
- capability;
- duration;
- load and generation timing when supplied;
- context and output size;
- cancellation;
- outcome and error code;
- validation result.

Raw prompts, repository snippets, environment values, hidden reasoning, and complete invalid responses are absent by default.

## Failure isolation

Provider configuration, health checks, model listing, model completion, and validation run outside authoritative write transactions. No provider result is written until strict validation completes. Provider outage does not affect collectors, scanners, REST inventory, CLI, MCP core tools, registry, allocator, or conflict engine.

## Test plan

- fake Ollama-compatible server;
- health, version, tags, show, and ps;
- strict schema request shape;
- tools allowlist;
- slow connect, slow body, and cancellation;
- redirect and non-loopback rejection;
- oversized response;
- invalid JSON and wrong content type;
- model-not-found;
- provider restart;
- circuit transitions;
- bounded concurrency;
- late response after cancellation;
- proof that no pull, delete, shell, registry, or process operation is reachable.
