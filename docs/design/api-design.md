# PortAtlas REST and Event API Design

## Contract principles

- Base path is /api/v1.
- API models represent domain and application DTOs, not database rows.
- All inventory data is sensitive local metadata.
- Collection endpoints use cursor pagination with deterministic ordering.
- Errors have stable codes and request IDs.
- Repeatable mutations use idempotency.
- Revisioned settings use optimistic concurrency.
- Mutations that propose file or configuration changes expose dry-run representations before any future apply capability.
- Normal responses contain no secret values.
- Dashboard real-time delivery uses SSE.

## Authentication

The service binds to 127.0.0.1 by default.

### Browser

1. Native setup produces a one-time high-entropy bootstrap secret in a user-only channel.
2. POST /api/v1/auth/bootstrap exchanges it for an HttpOnly SameSite session.
3. The response sets a CSRF token through a separate non-HttpOnly binding or response field.
4. Browser mutations require the session, permitted Origin, and matching CSRF token.
5. The bootstrap secret is invalidated or rotated after exchange.

### CLI and HTTP MCP

Scoped bearer tokens are issued explicitly, shown once, stored as hashes, and revocable. REST bearer authentication uses Authorization: Bearer. MCP transport details are defined separately.

### Public surface

Only static application assets, a non-sensitive liveness response, and the bootstrap exchange are unauthenticated. Readiness, inventory, project paths, configuration, and diagnostics require authentication.

## Common headers

| Header | Direction | Meaning |
| --- | --- | --- |
| X-Request-ID | both | Caller-provided safe identifier or server-generated identifier |
| Idempotency-Key | request | Required for duplicate-sensitive mutations |
| ETag | response | Resource identity and revision |
| If-Match | request | Required for revision-protected mutation |
| Last-Event-ID | request | SSE replay cursor |
| X-CSRF-Token | browser request | Session-bound mutation protection |

Request IDs are validated for length and safe character set. The service never echoes arbitrary oversized header content.

## Response shapes

### Single resource

~~~json
{
  "data": {
    "id": "ins_...",
    "type": "project_instance",
    "revision": 4,
    "attributes": {}
  },
  "meta": {
    "request_id": "req_..."
  }
}
~~~

### Collection

~~~json
{
  "data": [],
  "page": {
    "next_cursor": "opaque-or-null",
    "has_more": false
  },
  "meta": {
    "request_id": "req_...",
    "snapshot_at": "2026-07-11T00:00:00Z"
  }
}
~~~

Cursors encode a version, stable sort tuple, filters hash, and snapshot boundary, then are authenticated or signed. Clients treat them as opaque. Invalid or expired cursors return a stable error rather than silently restarting.

## Resource groups

### System and collectors

| Method and path | Behavior |
| --- | --- |
| GET /system/status | Service, database, scheduler, collector, scanner, Docker, and optional AI status |
| GET /system/capabilities | Enabled platform and integration capabilities |
| GET /collectors | Collector status and safe limitation summaries |
| POST /collectors/refresh | Start a bounded refresh; idempotent by key |

### Project roots and scans

| Method and path | Behavior |
| --- | --- |
| GET /project-roots | List approved roots |
| POST /project-roots/preview | Canonicalize and preview scope without registering |
| POST /project-roots | Register an approved root |
| GET /project-roots/{root_id} | Get root and scan policy |
| PATCH /project-roots/{root_id} | Revision-protected settings update |
| DELETE /project-roots/{root_id} | Stop scanning and apply explicit retention policy |
| POST /scans | Start root or ProjectInstance scan |
| GET /scans/{scan_id} | Get progress and safe diagnostics |
| POST /scans/{scan_id}/cancel | Request cancellation |

Paths supplied to preview are never returned to callers lacking root-management scope.

### Projects and services

| Method and path | Behavior |
| --- | --- |
| GET /projects | Cursor-paginated logical projects |
| GET /projects/{project_id} | Logical project and instance summary |
| GET /project-instances | Cursor-paginated operational instances |
| GET /project-instances/{instance_id} | ProjectInstance details |
| GET /project-instances/{instance_id}/ports | Unified presentation with separate state records |
| GET /project-instances/{instance_id}/services | Services |
| POST /project-instances/{instance_id}/preflight | Freshness-aware deterministic preflight |

### Port inventory

| Method and path | Behavior |
| --- | --- |
| GET /ports/observations | Runtime observation inventory |
| GET /ports/declarations | Static declaration inventory |
| GET /ports/reservations | Persistent assignments |
| GET /ports/leases | Active and historical leases by scope |
| GET /ports/availability | Availability explanation for protocol, port, and bind scope |
| POST /ports/suggestions | Deterministic explained suggestion; no occupancy change |

Filters include protocol, state, source, ProjectInstance, Service, Docker/native, database category, exposure, confidence, conflict, range, and freshness.

### Registry mutations

| Method and path | Behavior |
| --- | --- |
| POST /ports/reservations | Create a persistent reservation |
| DELETE /ports/reservations/{reservation_id} | Release a reservation |
| POST /ports/leases | Acquire an expiring lease atomically |
| POST /ports/leases/{lease_id}/renew | Renew within policy |
| DELETE /ports/leases/{lease_id} | Release a lease |

Create and renew require Idempotency-Key. Responses include policy rationale, resource revision, relevant conflict status, and the unmanaged-process race warning.

### Conflicts and policies

| Method and path | Behavior |
| --- | --- |
| GET /conflicts | Cursor-paginated conflict findings |
| GET /conflicts/{conflict_id} | Finding, members, evidence, actions, and history |
| POST /conflicts/{conflict_id}/ignore | Suppress with reason and expiry |
| DELETE /conflicts/{conflict_id}/ignore | Remove suppression |
| GET /policies | Policies and effective provenance |
| POST /policies | Create scoped policy |
| PATCH /policies/{policy_id} | Revision-protected policy update |
| POST /policies/evaluate | Dry-run effective policy for a scope |

### Evidence, audit, configuration, and integrations

| Method and path | Behavior |
| --- | --- |
| GET /discovery-evidence/{evidence_id} | Safe provenance only |
| GET /audit-events | Authorized cursor-paginated audit |
| GET /configuration | Redacted exportable configuration |
| POST /configuration/validate | Validate without applying |
| POST /configuration/import-plan | Return migration and diff plan |
| GET /integrations | Configured clients without credentials |
| POST /integrations/tokens | Issue a scoped token once |
| DELETE /integrations/tokens/{token_id} | Revoke token |

### Conditional AI

| Method and path | Behavior |
| --- | --- |
| GET /ai/providers | Provider status and redacted profiles |
| POST /ai/providers/test | Explicit health and capability test |
| GET /ai/models | Installed provider models |
| POST /ai/query | Read-only grounded natural-language query |
| POST /ai/explanations | Grounded conflict explanation |
| POST /ai/summaries | Grounded ProjectInstance summary |
| DELETE /ai/derived-data | Purge AI-derived records |

AI operations return generated, provider, model identity, validation status, evidence IDs, staleness, and request ID. They do not return hidden reasoning.

## Dry-run contract

A dry-run result contains:

- plan ID with bounded expiry;
- operation and target scope;
- expected current revisions and source fingerprints;
- proposed structured changes;
- affected resources and safe paths;
- conflicts and policy effects;
- required permission;
- risk and rollback description;
- validation commands expressed as data, not automatically executed.

Registry reservation creation is already a direct explicit mutation and does not need a fictional dry-run. Future source-file patching requires a dry-run plan and a separate approved apply command; no source-file apply endpoint ships in the registry-only MVP.

## Optimistic concurrency

GET returns ETag. PATCH, DELETE where state can drift, and confirmation actions require If-Match. A mismatch returns RESOURCE_REVISION_CONFLICT with current revision and safe refetch guidance. The server does not merge conflicting policy edits automatically.

## Idempotency

Idempotency scope is principal plus operation plus target scope. The same key and same canonical request returns the original status and representation. The same key with different content returns IDEMPOTENCY_KEY_REUSED. Records expire after a documented interval longer than normal client retry windows.

## SSE event endpoint

GET /api/v1/events accepts an authenticated browser session or bearer with events:read.

Event framing:

~~~text
id: 18442
event: reservation.created
data: {"schema_version":1,"timestamp":"2026-07-11T00:00:00Z","resource":{"type":"port_reservation","id":"res_...","revision":1},"request_id":"req_...","payload":{"protocol":"tcp","port":4310}}
~~~

Required data fields:

- schema_version;
- timestamp;
- resource type, ID, and revision;
- request_id when available;
- minimal payload safe for the authenticated scope.

Representative event types:

- system.status_changed;
- collector.status_changed;
- scan.progressed;
- project_instance.changed;
- observation.changed;
- declaration.changed;
- reservation.created;
- reservation.released;
- lease.changed;
- conflict.created;
- conflict.changed;
- conflict.resolved;
- policy.changed;
- ai.status_changed;
- system.resync_required.

Semantics:

- delivery is at least once;
- IDs are ordered cursors and clients deduplicate;
- Last-Event-ID requests replay within retention;
- expired cursor produces system.resync_required;
- heartbeat comments contain no application data;
- slow consumers are disconnected safely;
- events notify; REST remains authoritative.

This endpoint is not the MCP transport endpoint.

## Error response

~~~json
{
  "error": {
    "code": "PORT_ALREADY_ALLOCATED",
    "message": "The requested TCP port is already allocated in this scope.",
    "retryable": false,
    "request_id": "req_...",
    "details": {
      "conflict_id": "con_..."
    }
  }
}
~~~

Details are code-specific, bounded, documented, and secret-free. Validation errors contain safe field paths. Internal stack traces never reach clients.

## Status mapping

| Status | Use |
| --- | --- |
| 200 | Successful query or idempotent replay |
| 201 | Resource created |
| 202 | Background scan or refresh accepted |
| 204 | Release completed with no body |
| 400 | Syntax or unsupported API contract |
| 401 | Missing or invalid authentication |
| 403 | Scope, Origin, CSRF, or approved-root denial |
| 404 | Resource absent or intentionally concealed |
| 409 | Allocation, idempotency, or state conflict |
| 412 | Expected revision mismatch |
| 422 | Semantically invalid request |
| 429 | Bounded concurrency or rate limit |
| 503 | Required local dependency unavailable |

## Versioning

Breaking HTTP shape changes require a new API major path. Additive fields may appear within v1 only when clients are required to ignore unknown response fields. Input schemas reject unknown fields unless an endpoint explicitly supports extension metadata. SSE data has an independent schema_version. OpenAPI output is checked for drift in CI and feeds a generated or validated TypeScript client.

## Security limits

- JSON, multipart, header, query, and response size limits are explicit.
- CORS is not a substitute for Origin and authentication.
- Host and Origin allowlists prevent DNS rebinding.
- File paths are canonicalized by the application service.
- Tokens, cookies, secret handles, environment values, raw process arguments, and AI prompts never appear in normal responses.
- Non-loopback bind requires a separate future threat model.
