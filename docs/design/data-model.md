# PortAtlas Data Model

## Goals

The persistence model supports embedded SQLite by default and an optional PostgreSQL profile through the same SQLAlchemy repository contracts. It preserves source provenance, transaction-safe registry operations, ProjectInstance identity, deterministic conflicts, audit history, and dashboard event replay.

The schema avoids database-specific domain behavior. Adapter-specific locking and indexing are permitted when repository contract tests prove equivalent semantics.

## Conventions

- Table names are plural snake_case.
- IDs are opaque text UUID identifiers with resource prefixes.
- Timestamps are UTC and stored with portable precision.
- Mutable resources have revision integer not null.
- Enumerations are validated in the application and by check constraints where portable.
- JSON columns contain versioned non-secret metadata, never unbounded arbitrary source data.
- Foreign keys are enabled and explicit.
- Deletion favors archive or status transitions when audit provenance matters.

## Relationship overview

~~~mermaid
erDiagram
    PROJECT_ROOTS ||--o{ PROJECT_INSTANCES : contains
    PROJECTS ||--o{ PROJECT_INSTANCES : realizes
    PROJECT_INSTANCES ||--o{ SERVICES : contains
    PROJECT_INSTANCES ||--o{ PORT_DECLARATIONS : owns
    PROJECT_INSTANCES ||--o{ PORT_RESERVATIONS : owns
    PROJECT_INSTANCES ||--o{ PORT_LEASES : owns
    SERVICES ||--o{ PORT_DECLARATIONS : scopes
    SERVICES ||--o{ PORT_RESERVATIONS : scopes
    SERVICES ||--o{ PORT_LEASES : scopes
    PROCESS_IDENTITIES ||--o{ PORT_OBSERVATIONS : owns
    CONTAINER_IDENTITIES ||--o{ PORT_OBSERVATIONS : owns
    DISCOVERY_EVIDENCE ||--o{ PORT_DECLARATIONS : supports
    CONFLICTS ||--o{ CONFLICT_MEMBERS : contains
    AUDIT_EVENTS }o--|| INTEGRATION_CLIENTS : attributes
    AI_PROVIDER_PROFILES ||--o{ AI_ASSISTANCE_RESULTS : produces
    AI_CONTEXT_RECORDS ||--o{ AI_ASSISTANCE_RESULTS : grounds
~~~

## Core catalog tables

### project_roots

| Column | Type | Rules |
| --- | --- | --- |
| root_id | text | primary key |
| canonical_path | text | unique among active roots |
| display_path | text | user-facing, may be redacted in exports |
| category | text | personal, work, experiment, archive, custom |
| scan_policy_json | JSON | versioned, validated policy |
| state | text | active, paused, inaccessible, removed |
| revision | integer | optimistic concurrency |
| created_at, updated_at | timestamp | UTC |

### projects

| Column | Type | Rules |
| --- | --- | --- |
| project_id | text | primary key |
| display_name | text | non-empty |
| manifest_identity | text nullable | user-controlled stable key |
| repository_fingerprint | text nullable | local evidence, indexed |
| metadata_json | JSON | safe Git and stack metadata |
| created_at, updated_at | timestamp | UTC |

### project_instances

| Column | Type | Rules |
| --- | --- | --- |
| instance_id | text | primary key |
| project_id | text | foreign key projects |
| root_id | text | foreign key project_roots |
| canonical_path | text | unique among active instances |
| relative_path | text | relative to root |
| worktree_identity | text nullable | indexed |
| filesystem_identity | text nullable | platform evidence |
| state | text | discovered, active, paused, inaccessible, archived, removed |
| manifest_status | text | absent, valid, invalid, version_unsupported |
| revision | integer | optimistic concurrency |
| first_seen_at, last_seen_at | timestamp | UTC |

### services

Unique constraint: instance_id plus service_key.

Columns: service_id, instance_id, service_key, display_name, category, framework, metadata_json, revision, created_at, updated_at.

## Runtime tables

### collection_runs

Records collector_id, adapter_version, scope_hash, started_at, completed_at, status, completeness, observation_count, limitation_count, safe_error_code, and request_id. Raw command output is not stored.

### process_identities

Unique natural key within host: pid, start_time, executable_fingerprint. Columns also include safe executable name, user identity, parent reference, redacted command metadata, and last_seen_at.

### container_identities

Docker container ID is unique. Store safe name, image reference, compose project and service, selected labels, networks, health, restart policy, start time, state, and last_seen_at.

### port_observations

| Column group | Fields |
| --- | --- |
| Identity | observation_id, collector_id, source_record_key |
| Port | protocol, port, address_family, bind_address, namespace, host_identity |
| Socket | socket_state, observed_at, last_seen_at, freshness |
| Owner | process_identity_id nullable, container_identity_id nullable |
| Association | instance_id nullable, service_id nullable, confidence, evidence_json |
| Provenance | collection_run_id, adapter_version, permission_limited |

Indexes:

- protocol, port, freshness;
- instance_id, last_seen_at;
- process_identity_id;
- container_identity_id;
- collector_id, source_record_key unique for current identity.

Historical snapshots are retained according to policy; the current inventory query uses freshness and latest source identity.

## Scanner tables

### scan_runs

Records root or instance scope, scanner version, started and completed time, status, candidate count, parsed count, failure count, byte count, completeness, and request ID.

### discovery_evidence

Columns: evidence_id, instance_id, kind, safe_relative_path, line, column, structured_pointer, source_fingerprint, producer_id, producer_version, confidence, rationale_code, redaction_json, discovered_at.

No full file lines or environment contents are stored.

### port_declarations

Columns: declaration_id, instance_id, service_id nullable, protocol, port, address_family, bind_address nullable, namespace, declaration_role, environment_key nullable, evidence_id, confidence, confirmation_state, source_fingerprint, parser_id, parser_version, first_seen_at, last_seen_at, freshness.

Unique current-source key: instance_id, parser_id, evidence_id, declaration_role, protocol, port, namespace.

## Registry tables

### port_reservations

Columns: reservation_id, instance_id, service_id, protocol, port, bind_scope, status, owner_principal_id, rationale, policy_snapshot_json, expires_at nullable, revision, created_at, updated_at, released_at.

### port_leases

Columns: lease_id, instance_id, service_id, protocol, port, bind_scope, status, owner_principal_id, idempotency_key_hash, policy_snapshot_json, expires_at, revision, created_at, updated_at, released_at.

The persistence adapter enforces no overlapping active blocking allocation. SQLite uses a write transaction and supporting active-key table or equivalent portable uniqueness strategy. PostgreSQL may use partial unique indexes or transactional locks behind the repository.

### port_policies

Columns: policy_id, scope_type, scope_id nullable for global, policy_json, schema_version, revision, created_at, updated_at. Unique current policy per scope.

### scan_rules

Columns: scan_rule_id, rule_key, rule_type, schema_version, parser_id, parser_version, scope_type, scope_id, rule_json, enabled, revision, created_at, updated_at. Built-in rules record the installed release identity; user rules are limited to the supported declarative rule schema.

### health_checks

Future-compatible columns: health_check_id, service_id, check_type, safe_config_json, enabled, execution_policy, revision, created_at, updated_at. The MVP does not persist arbitrary shell strings or execute custom command checks. A health result, when implemented, remains separate from socket observations.

### desired_port_assignments

Columns: desired_id, change_plan_id, instance_id, service_id, protocol, port, bind_scope, rationale, status, created_at, expires_at. Desired rows never participate as registry occupancy.

## Conflict tables

### conflicts

Columns: conflict_id, fingerprint unique, code, severity, status, explanation_params_json, automated_safety, first_seen_at, last_seen_at, resolved_at, suppression_reason, suppression_expires_at, revision.

### conflict_members

Columns: conflict_id, member_type, member_id, role, evidence_id nullable. Primary key: conflict_id, member_type, member_id, role.

### conflict_actions

Stores deterministic recommended action descriptors, ordering, risk, dry-run capability, and required permission. It stores no executable shell strings.

## Integration and security tables

### integration_clients

Client ID, type, display name, transport, enabled state, policy profile, revision, created and last-used timestamps.

### access_tokens

Token ID, client ID, salted secret hash, scopes, created_at, expires_at, revoked_at, last_used_at. Raw bearer tokens are returned once and never stored.

Browser session records may be in memory or in a bounded table containing only a session hash, CSRF binding, expiry, and revocation state.

### idempotency_records

Principal ID, operation, idempotency key hash, request hash, status, response code, redacted response JSON, resource ID, created_at, expires_at. Unique: principal ID, operation, idempotency key hash.

## Audit and events

### audit_events

Append-only columns: audit_id, timestamp, principal type and ID, integration client ID, action, resource type and ID, outcome, request ID, safe metadata JSON, previous revision nullable, resulting revision nullable.

Audit metadata never includes raw credentials, full environment values, arbitrary file contents, or model prompts.

### event_outbox

| Column | Purpose |
| --- | --- |
| sequence | monotonically increasing primary event cursor |
| event_type | stable SSE event name |
| schema_version | payload contract version |
| occurred_at | UTC ordering evidence |
| resource_type, resource_id | invalidation target |
| resource_revision | latest committed revision |
| request_id | correlation |
| payload_json | minimal non-secret data |
| published_at | delivery bookkeeping |

Outbox rows are retained long enough for normal SSE replay and then compacted by policy. Resource state remains available through REST.

## Optional AI tables

### ai_provider_profiles

Profile ID, provider type, endpoint, selected model names, capability settings, privacy settings, timeout, concurrency, keep_alive, retention, enabled state, revision. Credentials are referenced by secret-store handle only.

### ai_context_records

Context ID, task type, instance scope, evidence ID list, category counts, redaction counts, context byte count, estimated token count, provider profile ID, created_at, expires_at, raw_content_stored false by default.

### ai_assistance_results

Result ID, context ID, provider profile ID, model name and digest, task type, schema ID and version, validation status, generated status, confidence nullable, structured_result_json, evidence IDs, created_at, expires_at, saved_by_user flag.

Structured result JSON is redacted and bounded. Invalid provider output is not stored except for safe failure metadata.

## Database configuration

### SQLite

- foreign_keys enabled;
- journal_mode WAL on a local filesystem;
- busy_timeout configured;
- synchronous setting selected through durability testing;
- automatic and shutdown checkpoint policy;
- one application writer coordinator;
- file and containing directory user-only;
- backup through SQLite-supported snapshot or backup API.

### PostgreSQL

- supported version range declared by release policy;
- credentials in secret storage;
- TLS required for non-loopback connections in future server mode;
- connection pool bounded;
- transaction isolation and locking selected per repository operation;
- compatibility suite runs migrations and core transaction tests.

## Migrations and compatibility

- Alembic is the only schema migration authority.
- Every release records application schema version and minimum compatible version.
- Migrations back up embedded data before destructive transformation.
- A migration either completes or leaves a documented recovery path.
- Downgrade is supported only where data preservation is proven; application rollback otherwise restores the pre-upgrade backup.
- JSON payloads carry their own schema_version and migration function.

## Retention

Default runtime history is seven days and configurable. Current reservations, active leases, open conflicts, policies, roots, projects, audit events required by policy, and user-saved AI artifacts are not removed by observation-history cleanup. AI raw prompts are not retained by default. Users can purge all AI-derived data without deleting authoritative records.

## Data security

- No secrets in normal tables.
- Paths are returned only to authorized local clients and redacted in portable exports.
- Diagnostic exports use explicit allowlists.
- Database files, backups, token stores, and config directories use user-only permissions.
- No telemetry exporter reads persistence data.
