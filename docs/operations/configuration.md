# Configuration Operations Contract

Status: **Proposed before implementation**

This document describes behavior to implement; it does not claim that a configuration file, command, or UI already exists.

## Sources and precedence

Proposed precedence, highest first:

1. Explicit command invocation options for that process
2. Authenticated user settings stored by the application
3. Environment overrides from an allowlisted operational namespace
4. User-scoped configuration file
5. Safe built-in defaults

Project manifests express project intent and policy but cannot override authentication, network binding, redaction, retention maxima, or forbidden mutation. The proposed `.portatlas.yaml` name is unpublished while the working-name gate remains open.

## Configuration groups

| Group | Examples | Security and validation |
|---|---|---|
| Service | loopback port, startup, log level | Loopback only; safe default; typed range; no credential in URL |
| Authentication | rotation metadata, session duration, token scopes | Secret values write-only; protected permissions; bounded duration |
| Storage | SQLite state location, optional PostgreSQL profile, backup policy | Canonical user-scoped path; credential URL never returned; migrations versioned |
| Collection | refresh cadence, host and Docker enablement, timeouts | Bounded values; Docker optional; denial shown as degraded |
| Scanning | registered roots, parser enablement, budgets, ignore policy | Explicit consent; canonical confinement; safe limits |
| Allocation | ranges, exclusions, protocol and scope policies, lease duration | Validate full range and overlap; atomic revisioned changes |
| UI | density, theme, accessibility preferences | No effect on semantic state or authorization |
| MCP | STDIO enablement, HTTP enablement, credential scopes | HTTP loopback, Origin validation, authentication mandatory |
| AI | global enable, loopback endpoint, model choice, timeouts, retention | Disabled by default; no auto-download; context preview and strict bounds |

## Schema behavior

Configuration is versioned, parsed strictly, and validated before replacement. Unknown keys produce a safe error rather than being silently ignored. Changes use optimistic concurrency and an atomic write. Exported configuration omits credentials, sessions, project contents, and machine-specific private paths unless a user explicitly chooses a local migration export with preview.

## Recovery

An invalid user configuration does not trigger unsafe defaults or overwrite the file. The service starts in a bounded recovery mode that identifies safe field-level errors and permits restoring the last valid configuration. Authentication and loopback restrictions stay enforced in recovery mode.
