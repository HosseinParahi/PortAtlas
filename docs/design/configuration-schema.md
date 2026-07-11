# PortAtlas Configuration Schema

## Objectives

PortAtlas behavior is configurable through UI, CLI, and versioned files rather than source edits. Configuration is:

- local-first and exportable without secrets;
- schema-versioned and migratable;
- validated before application;
- protected by optimistic concurrency;
- recoverable after corruption;
- separated from credentials and generated tokens.

## Locations

The implementation uses platform-appropriate user directories resolved at runtime. Documentation and diagnostics show the effective paths. No founder-specific or repository-specific absolute path is hard-coded.

Logical stores:

- config: versioned non-secret settings;
- data: SQLite database, caches, and migrations;
- state: runtime PID or socket metadata;
- logs: redacted local logs;
- secrets: platform credential store or user-only secret file;
- backups: versioned local backups under retention policy.

## Precedence

From lowest to highest:

1. installed schema defaults;
2. user configuration file;
3. explicitly supported environment overrides for deployment mechanics;
4. one-command CLI overrides that do not persist;
5. request-specific options allowed by policy.

UI writes the user configuration through the application service. Unknown environment variables do not alter behavior. Security policy cannot be weakened by repository files or project manifests.

## Top-level schema

~~~yaml
schema_version: 1
revision: 1

service:
  bind_host: 127.0.0.1
  port: auto
  browser_open_on_start: true

persistence:
  profile: sqlite
  sqlite:
    journal_mode: wal
    busy_timeout_ms: 5000
  postgresql:
    connection_secret_ref: null

project_roots: []

scanning:
  enabled: true
  default_max_depth: 8
  max_candidate_file_bytes: 1048576
  max_total_bytes_per_scan: 67108864
  follow_symlinks: false
  environment_files: true
  focused_parser_groups:
    - compose
    - environment
    - package_scripts
    - python_launch
    - framework_config
    - tauri

collectors:
  host:
    enabled: true
    interval_seconds: 5
    psutil_primary: true
    lsof_fallback: true
  docker:
    enabled: true
    interval_seconds: 15
    event_refresh: true

registry:
  default_lease_seconds: 120
  maximum_lease_seconds: 900
  avoid_ephemeral_ranges: true

policies:
  global:
    allowed_ranges:
      - start: 1024
        end: 49151
    forbidden_ports: []
    loopback_required_categories:
      - database
      - admin

events:
  replay_retention_seconds: 3600
  heartbeat_seconds: 20
  per_client_buffer: 256

history:
  runtime_days: 7
  audit_days: 30

integrations:
  mcp_stdio_enabled: true
  mcp_http_enabled: false

security:
  non_loopback_bind_enabled: false
  diagnostic_paths_redacted: true

ai:
  enabled: false
  provider: ollama
  endpoint: http://127.0.0.1:11434
  assistant_model: null
  structured_model: null
  timeout_seconds: 30
  max_concurrency: 1
  keep_alive: 5m
  store_raw_prompts: false
  store_conversations: false
  background_analysis: false
  capabilities:
    natural_language_query: false
    conflict_explanation: false
    project_summary: false
    assisted_extraction: false
    embeddings: false

ui:
  theme: system
  reduced_motion: system
  page_size: 50
~~~

This example demonstrates shape and safe defaults. Release defaults are pinned by schema fixtures and acceptance tests.

## Project root entry

~~~yaml
- root_id: root_generated_id
  path: ~/GitHub/personal
  state: active
  category: personal
  tags:
    - local
  max_depth: 8
  include:
    - "**"
  exclude:
    - .git
    - node_modules
    - .venv
    - dist
    - build
  follow_symlinks: false
  environment_files: true
~~~

Paths are expanded, canonicalized, and persisted in a platform-safe form by the application service. A configuration import cannot approve a path silently: new or widened roots require preview and explicit confirmation.

## Persistence profile

### SQLite

Default embedded profile. The database lives on a local filesystem with user-only permissions. WAL, foreign keys, checkpoint policy, busy timeout, and backup behavior are validated at startup.

### PostgreSQL

Optional explicit profile. Configuration stores only a secret reference, never the database credential. Startup verifies connection and migration compatibility. Failure does not silently fall back to SQLite because that would split authoritative state.

## Collector configuration

Host collector controls:

- enabled;
- interval;
- protocols;
- psutil primary;
- lsof fallback;
- timeout and output limits;
- permitted process metadata fields.

Docker controls:

- enabled;
- interval;
- event refresh;
- endpoint secret reference if non-default;
- stopped-container retention;
- selected label allowlist.

No configuration grants Docker mutation in the MVP.

## Scan configuration

Global defaults and per-root overrides control:

- recursion depth;
- candidate count and byte budgets;
- include and exclude patterns;
- symlink policy;
- environment scanning;
- enabled focused parser groups;
- watcher and debounce behavior;
- sensitive path exclusions.

Regex-like user patterns are validated against complexity and length limits. Built-in protected excludes cannot be removed without explicit advanced confirmation.

## Registry and policy configuration

Ranges are inclusive integers from 1 through 65535 with start less than or equal to end. Configuration validation rejects overlaps only where policy semantics require disjoint categories. Effective policy reports provenance for every value.

Ephemeral ranges are platform-configurable and detected where safe. An unavailable detection source leaves uncertainty visible rather than applying an invented range.

Lease duration must be positive and no greater than maximum_lease_seconds. Registry-only assurance wording is fixed and not configurable.

## API and event configuration

- Loopback bind is default and non-loopback is disabled.
- Service port may be auto-selected from an installation-specific safe range.
- SSE replay retention is longer than expected disconnect windows.
- Heartbeat and buffer values have safe minimum and maximum constraints.
- Event payload schema version is not user-configurable.

## Authentication and integrations

Configuration stores token metadata and secret references, never raw bearer tokens. Integration clients define transport, scopes, approved ProjectInstance scope, expiry policy, and enabled state. Browser session and bootstrap secrets are generated state, not exportable configuration.

## Local AI configuration

AI remains disabled by default. Enabling requires:

- explicit provider test;
- selected installed model;
- capability-specific user consent;
- privacy notice acknowledgement;
- security gate satisfied by the release;
- endpoint policy validation.

The endpoint defaults to loopback. Model download, install, pull, or activation never occurs from configuration import. Raw prompt and conversation storage remain false unless a future reviewed feature allows a clear opt-in. Embeddings are Version 1 and remain false in the MVP schema profile.

## Secret separation

Secret examples:

- bootstrap token;
- CLI and MCP bearer tokens;
- PostgreSQL password or connection credential;
- future provider credentials.

The main configuration contains only opaque secret references. Export, logs, API, MCP, support bundle, and UI never resolve a secret reference into a secret value.

## Validation

Validation phases:

1. parse syntax with size and depth limits;
2. validate schema version;
3. reject unknown fields unless an extension namespace explicitly permits them;
4. validate scalar constraints and enumerations;
5. validate cross-field invariants;
6. validate path syntax without expanding scope;
7. verify secret references exist without reading them into diagnostics;
8. calculate a redacted effective configuration;
9. return warnings and migration plan.

Cross-field examples:

- mcp_http_enabled requires authenticated loopback service;
- postgresql profile requires a valid connection secret reference;
- Docker event refresh requires Docker collector enabled;
- AI capability true requires AI enabled and a validated provider profile;
- store_raw_prompts cannot be enabled in the MVP release profile.

## Telemetry exclusion

The current schema contains no telemetry setting, endpoint, exporter, consent flag, or installation identifier. PortAtlas emits no telemetry. A future telemetry proposal requires a new ADR, privacy review, explicit founder approval, and a new schema version before any configuration surface can exist.

## Update flow

1. Client fetches configuration and revision.
2. Client submits a patch with If-Match or expected_revision.
3. Service applies patch to an in-memory copy.
4. Full schema and invariant validation runs.
5. Service returns a dry-run diff for security-sensitive changes.
6. Authorized apply writes a temporary file, fsyncs as supported, atomically replaces the original, and retains a bounded backup.
7. Runtime modules receive a configuration-changed event.
8. Settings requiring restart are reported explicitly.

The service never writes a partially valid configuration.

## Migration and recovery

Each schema version has an explicit pure migration. Migration:

- preserves a pre-migration backup;
- records source and target versions;
- produces a redacted preview;
- fails closed on ambiguous security settings;
- never invents an approved ProjectRoot;
- is covered by round-trip and fixture tests.

If the file is corrupt, PortAtlas starts safe recovery mode with collectors, scans, mutations, and integrations paused. The user may inspect a redacted validation report, restore a backup, or reset to defaults while preserving the data store.

## Import and export

Portable export includes:

- schema version;
- non-secret roots and policy after path-redaction choice;
- scan rules;
- collector preferences;
- service catalog overrides;
- UI preferences;
- disabled or redacted integration metadata;
- AI settings without model conversations, raw prompts, or secrets.

Import never activates non-loopback binding, new roots, MCP mutation scopes, AI, or model download without explicit local confirmation. Telemetry cannot be activated because the schema has no telemetry capability.
