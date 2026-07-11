# ADR 0002: Persistence

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Local state, migrations, and future server compatibility

## Context

PortAtlas needs transactional reservations and leases, durable configuration, normalized observations and declarations, evidence, conflicts, and audit metadata. Requiring PostgreSQL for a single-user local utility would add installation work and consume a port before PortAtlas can run. Using SQLite directly throughout the domain would make a future server profile expensive and could hide concurrency differences.

## Decision

Use SQLite as the default embedded local database and keep PostgreSQL as an optional compatibility profile:

- SQLAlchemy repositories are the only persistence interface used by application services.
- Alembic owns versioned, forward-tested migrations.
- SQLite uses foreign keys, bounded busy timeouts, and write-ahead logging after platform validation.
- Lease and reservation mutations use explicit transactions and database constraints; ADR 0009 defines allocation semantics.
- PostgreSQL runs in CI for repository and migration compatibility tests.
- Domain rules do not branch on database vendor.
- Database URLs, credentials, and engine-specific settings remain outside normal API responses and diagnostics.
- Backup and restore operate on a quiesced or transactionally consistent store and are tested across schema upgrades.

SQLite is the supported zero-setup profile. PostgreSQL is not required for the MVP and is not presented as a network listener unless a PostgreSQL profile is actually configured.

## Alternatives considered

### PostgreSQL only

PostgreSQL provides stronger multi-client concurrency and operational tooling, but makes local installation heavier and introduces the very kind of service-port dependency the product is intended to coordinate.

### SQLite only with direct SQL

This is the smallest implementation, but it couples domain behavior to one dialect and makes the promised server profile and compatibility testing costly.

### Separate local and server data models

Different models could optimize each mode but would duplicate migrations and allow behavioral drift in reservations, conflicts, and audit semantics.

## Consequences

### Positive

- A first installation requires no database daemon.
- Transactions and constraints can make PortAtlas-managed leases race-safe.
- Repository contracts provide a deliberate path to PostgreSQL.
- Backup and uninstall behavior are understandable for local users.

### Costs and risks

- SQLite permits one writer at a time and requires short, disciplined transactions.
- SQLAlchemy abstraction does not automatically eliminate SQL dialect differences.
- WAL and filesystem behavior must be validated on supported data locations.
- PostgreSQL compatibility expands the CI matrix even though it is not the default.

## Verification

- Apply every migration from an empty database on SQLite and PostgreSQL.
- Upgrade representative databases from each released schema and verify rollback or documented recovery.
- Run repository contract tests against both engines.
- Stress concurrent lease and reservation writes and prove uniqueness invariants.
- Simulate interruption, locked databases, corrupt configuration, backup, restore, and low-disk conditions.
- Check generated SQL and migrations for accidental vendor-specific domain logic.

## Revisit triggers

- Team/server mode becomes an approved delivery target.
- Measured local write contention exceeds the two-second update target.
- A required feature cannot be implemented safely on supported SQLite versions.
- PostgreSQL compatibility repeatedly distorts the local model without a committed server roadmap.

## Sources

- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)
- [SQLite isolation](https://www.sqlite.org/isolation.html)
- [SQLite write-ahead logging](https://www.sqlite.org/wal.html)
- [SQLAlchemy dialect documentation](https://docs.sqlalchemy.org/en/20/dialects/)
- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/)
