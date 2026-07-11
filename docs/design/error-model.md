# PortAtlas Error Model

## Goals

Errors are stable, actionable, transport-neutral, safe to expose locally, and consistent across REST, CLI, MCP, background jobs, and SSE status events. The model distinguishes user correction, conflict, permission, dependency degradation, and internal failure without leaking secrets or stack traces.

## Canonical error

~~~json
{
  "code": "PORT_ALREADY_ALLOCATED",
  "message": "The requested TCP port is already allocated in this scope.",
  "retryable": false,
  "request_id": "req_...",
  "details": {
    "conflict_id": "con_..."
  }
}
~~~

Fields:

| Field | Contract |
| --- | --- |
| code | Stable uppercase machine code |
| message | Concise safe human message |
| retryable | Whether the same operation may succeed without user correction |
| request_id | Correlation ID safe to share |
| details | Bounded code-specific object with documented safe fields |
| causes | Optional bounded nested safe causes for batch operations |

Transport adapters may add protocol metadata but never alter code semantics.

## Taxonomy

### Request and validation

| Code | Meaning | Retryable |
| --- | --- | --- |
| REQUEST_INVALID | Request shape or semantic validation failed | false after correction |
| REQUEST_TOO_LARGE | Body, file, header, or output limit exceeded | false after reduction |
| CURSOR_INVALID | Pagination or event cursor is malformed | false |
| CURSOR_EXPIRED | Snapshot or replay boundary is unavailable | true after resync |
| IDEMPOTENCY_KEY_REQUIRED | Duplicate-sensitive mutation lacks key | false |
| IDEMPOTENCY_KEY_REUSED | Key was reused with different request content | false |
| RESOURCE_REVISION_CONFLICT | Expected revision differs from current | true after refetch |

### Authentication and authorization

| Code | Meaning |
| --- | --- |
| AUTHENTICATION_REQUIRED | No valid session or token |
| AUTHENTICATION_INVALID | Credential invalid, expired, or revoked |
| AUTHORIZATION_DENIED | Principal lacks required scope |
| ORIGIN_DENIED | HTTP Origin is not allowed |
| HOST_DENIED | Host validation failed |
| CSRF_VALIDATION_FAILED | Browser mutation lacked valid CSRF binding |
| ROOT_SCOPE_DENIED | Path is outside approved ProjectRoots |
| SYMLINK_SCOPE_DENIED | Resolved path violates symlink policy |

Authentication details never reveal whether a concealed resource exists.

### Resource and state

| Code | Meaning |
| --- | --- |
| RESOURCE_NOT_FOUND | Authorized resource does not exist |
| RESOURCE_STATE_INVALID | Operation is invalid for current lifecycle |
| PROJECT_INSTANCE_AMBIGUOUS | Evidence matches multiple instances |
| PROJECT_INSTANCE_INACCESSIBLE | Instance path cannot be safely accessed |
| MANIFEST_INVALID | Manifest failed schema or policy validation |
| POLICY_INVALID | Policy is internally invalid |
| POLICY_VIOLATION | Requested action violates effective policy |

### Registry and conflict

| Code | Meaning | Retryable |
| --- | --- | --- |
| PORT_ALREADY_ALLOCATED | Cooperative reservation or lease blocks request | false without another candidate |
| PORT_OBSERVED_IN_USE | Runtime evidence blocks request | false until state changes |
| PORT_AVAILABILITY_UNCERTAIN | Freshness or permissions prevent safe conclusion | true after refresh |
| ALLOCATION_RANGE_EXHAUSTED | No candidate satisfies policy | false without policy or state change |
| LEASE_EXPIRED | Lease is no longer active | false |
| LEASE_RENEWAL_DENIED | Ownership or duration policy blocks renewal | false |
| CONFLICT_NOT_ACTIONABLE | Requested automatic action is unsafe or unsupported | false |
| UNMANAGED_RACE_DETECTED | External process collided with cooperative state | true after diagnosis |

### Collector and scanner

| Code | Meaning |
| --- | --- |
| COLLECTOR_UNAVAILABLE | Adapter dependency is absent or unreachable |
| COLLECTOR_PERMISSION_LIMITED | Permissions reduce visibility |
| COLLECTOR_TIMEOUT | Deadline exceeded |
| COLLECTOR_OUTPUT_LIMIT | Bounded output exceeded |
| COLLECTOR_PARSE_FAILED | Supported adapter output could not be normalized |
| SCAN_CANCELLED | User or shutdown cancelled scan |
| SCAN_BUDGET_EXCEEDED | Traversal or parse budget reached |
| SCAN_FILE_UNSUPPORTED | File is outside focused parser support |
| SCAN_FILE_INVALID | Supported file is malformed |
| SCAN_SECURITY_REJECTED | Candidate violated path or input policy |

Partial jobs may complete with warnings rather than a top-level failure. Completeness is explicit.

### Persistence and configuration

| Code | Meaning |
| --- | --- |
| PERSISTENCE_BUSY | Database could not acquire bounded write access |
| PERSISTENCE_UNAVAILABLE | Configured store is unavailable |
| PERSISTENCE_INTEGRITY_ERROR | Constraint or data integrity failed |
| MIGRATION_REQUIRED | Application cannot operate until migration |
| MIGRATION_FAILED | Migration did not complete safely |
| CONFIGURATION_INVALID | Active configuration cannot be applied |
| SECRET_STORE_UNAVAILABLE | Required secret handle cannot be resolved |

PostgreSQL failure never triggers silent SQLite fallback.

### MCP and integration

| Code | Meaning |
| --- | --- |
| MCP_PROTOCOL_UNSUPPORTED | Requested protocol revision is unsupported |
| MCP_CAPABILITY_UNSUPPORTED | Optional client or server capability unavailable |
| INTEGRATION_DISABLED | Configured client is disabled |
| INTEGRATION_SCOPE_DENIED | Tool exceeds integration policy |
| TOOL_ARGUMENT_INVALID | MCP tool input failed validation |
| OPERATION_CANCELLED | Explicit cancellation accepted |

### Conditional AI

| Code | Meaning |
| --- | --- |
| AI_DISABLED | Optional AI is not enabled |
| AI_PROVIDER_UNAVAILABLE | Ollama or configured provider cannot be reached |
| AI_MODEL_NOT_FOUND | Selected installed model is absent |
| AI_CAPABILITY_UNSUPPORTED | Model or provider lacks required capability |
| AI_TIMEOUT | Request exceeded deadline |
| AI_CANCELLED | Request was cancelled |
| AI_CONTEXT_REJECTED | Context failed root, redaction, or size policy |
| AI_OUTPUT_INVALID | Strict syntax or schema validation failed |
| AI_EVIDENCE_INVALID | Output references absent or mismatched evidence |
| AI_TOOL_REQUEST_DENIED | Model requested a non-allowlisted operation |
| AI_CIRCUIT_OPEN | Provider backoff is active after repeated failures |

AI errors never degrade core registry, collection, scanning, allocation, API, CLI, or MCP behavior.

### Internal

INTERNAL_ERROR is the only generic unexpected-failure code exposed. It includes request ID and safe support guidance, not exception type or stack trace. Component-level detail remains in redacted local logs.

## REST mapping

| Error family | HTTP status |
| --- | --- |
| Authentication | 401 |
| Authorization, Origin, CSRF, root scope | 403 |
| Resource absent | 404 |
| Request syntax | 400 |
| Semantic validation | 422 |
| Allocation, state, idempotency conflict | 409 |
| Revision precondition | 412 |
| Size or rate limits | 413 or 429 |
| Required local dependency or persistence unavailable | 503 |
| Deadline | 504 where HTTP gateway semantics fit |
| Unexpected internal | 500 |

REST wraps the canonical error under error and returns X-Request-ID.

## CLI mapping

| Exit | Meaning |
| --- | --- |
| 0 | Success |
| 2 | Usage or validation |
| 3 | Conflict or unavailable requested port |
| 4 | Authentication or permission |
| 5 | Local dependency or degraded collector |
| 6 | Persistence or configuration |
| 7 | Cancelled or timed out |
| 8 | Unexpected internal |

JSON mode prints the canonical error object to standard output as the command result. Human mode prints a concise message and request ID to standard error. No ANSI is required when output is not a terminal.

## MCP mapping

Protocol and framing failures use JSON-RPC errors. Expected tool-domain failures return isError true and structuredContent containing the canonical error. This lets agents branch on code without parsing prose. The adapter does not translate permission denial into resource absence unless concealment policy requires it.

## SSE failure signaling

Connection-level authentication or validation uses HTTP status before stream establishment. After establishment:

- system.resync_required signals an expired cursor;
- system.status_changed carries degraded component state;
- heartbeat comments do not carry errors;
- a terminal stream error contains a stable safe code then closes.

Clients fetch REST state after reconnect. SSE never carries stack traces.

## Retry guidance

retryable true means a bounded retry can be reasonable. It does not instruct clients to retry immediately. Details may include retry_after_ms with a server maximum.

Safe retry examples:

- PERSISTENCE_BUSY with jitter and cap;
- AI_CIRCUIT_OPEN after retry_after_ms;
- CURSOR_EXPIRED after full resource resync;
- COLLECTOR_TIMEOUT only when user or scheduler policy permits.

Validation, authorization, policy, and idempotency mismatch errors require changed input or state.

## Batch and partial outcomes

Scans and collections distinguish:

- succeeded;
- succeeded_with_warnings;
- partial;
- cancelled;
- failed.

Per-item causes are capped and aggregated by code. A response includes counts and a cursor to authorized safe diagnostics rather than thousands of embedded errors.

## Redaction rules

Messages and details exclude:

- tokens, cookies, session IDs, and secret references;
- environment values;
- complete database URLs;
- raw process command lines;
- arbitrary file lines;
- paths outside caller scope;
- Docker socket details;
- model prompts, hidden reasoning, and raw invalid output.

Paths inside approved scope are relative where possible. Secret detection runs before serialization and logging.

## Stability

Error codes are part of the v1 contract. A code keeps its meaning for the API major version. New codes may be added. Message wording may improve and is not a machine contract. Every code has tests across REST, CLI, and MCP mapping where applicable.
