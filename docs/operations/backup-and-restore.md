# Backup and Restore Contract

Status: **Proposed workflow requiring implementation and drill evidence**

## Scope

Backups protect authoritative reservations, leases, project and instance metadata, safe configuration, migrations, and eligible bounded history. They do not copy project source, Docker state, Ollama models, authentication bearer values, browser sessions, raw AI prompts, or unredacted diagnostics.

## SQLite proposal

The service coordinates a consistent SQLite snapshot using a database-supported backup mechanism or a quiesced atomic copy that includes the correct journal state. Copying only a live main database file is forbidden. The backup contains a format version, application schema version, creation time, integrity digest, and redacted inventory summary.

## PostgreSQL proposal

The optional profile documents a compatible logical backup method and server/version requirements when it becomes supported. The application never shells out with credentials embedded in process arguments. PostgreSQL backup support cannot be inferred merely from repository compatibility tests.

## Restore workflow

1. Inspect manifest, origin version, integrity digest, and compatibility without altering current state.
2. Authenticate and explicitly confirm replacement scope.
3. Restore into a new isolated target and run integrity and migration checks.
4. Start an isolated validation instance or repository check.
5. Atomically switch only after all checks pass.
6. Preserve the prior state until the user accepts the restored result.
7. Rotate local credentials when the restore crosses a machine or user boundary.

A corrupt, unsupported, or secret-bearing backup fails closed and leaves current state untouched.

## Retention and permissions

Backups are user-initiated by default and stored with user-only permissions. A future scheduled policy requires explicit opt-in, bounded count or age, visible storage use, and safe pruning. The project does not upload backups.

## Release drill

Tests cover empty and target-capacity databases, active and expired leases, interrupted backup, corrupt archive, incompatible schema, restore failure, path loss, credential rotation, and a round-trip comparison of authoritative records and revisions. Each supported release must publish the tested upgrade and restore range.
