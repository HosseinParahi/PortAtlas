# ADR 0020: Embeddings deferral

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Semantic search and vector storage

## Context

Embeddings can improve semantic search over project descriptions and summaries, but they add a model lifecycle, derived sensitive data, chunk provenance, storage migration, rebuild, and deletion concerns. The MVP already needs deterministic inventory, filtering, fuzzy finding, and optional explanation. Selecting a vector store before evaluating real search value would add persistence complexity without a proven requirement.

## Decision

Defer embeddings and semantic search to Version 1:

- The MVP creates no embeddings, vector index, embedding-model download, or vector-store dependency.
- MVP search uses structured fields, deterministic filters, ordinary text search, and fuzzy matching over safe indexed metadata.
- PostgreSQL and pgvector are not required for local mode.
- Version 1 embeddings are opt-in and local-only with no cloud fallback.
- Before selecting an embedded vector store, compare search quality, storage, memory, startup, backup, migration, deletion, and cross-platform packaging using the real project corpus.
- Eligible input is allowlisted to user-approved descriptions, PortAtlas-generated redacted summaries, service names, framework metadata, manifest descriptions, conflict notes, and user-confirmed labels.
- Complete source files, environment files, credentials, secret-bearing process arguments, terminal history, private keys, database contents, and unapproved paths are ineligible.
- A future index must record ProjectInstance, source evidence, chunk provenance, redaction version, embedding provider, model digest, dimensions, creation time, and staleness.
- Users need per-project opt-out, storage limits, rebuild, model-migration, and complete-delete controls.

A later ADR selects the store only after the privacy and evaluation gates pass.

## Alternatives considered

### Embedded vector index in the MVP

This could demonstrate semantic search early but adds packaging and data-governance work before deterministic discovery is complete.

### PostgreSQL with pgvector

This is mature for server deployments but contradicts zero-setup embedded local mode and makes PostgreSQL mandatory.

### Send embeddings to a cloud service

This exposes sensitive local metadata and violates the default local-only policy.

### Use SQLite FTS only forever

Full-text search is a strong MVP baseline but may not satisfy future semantic queries or vocabulary mismatch.

## Consequences

### Positive

- MVP persistence and packaging remain smaller.
- No derived vector corpus exists before consent and deletion semantics are designed.
- The store choice follows measured value and real data.
- Core search remains available without any model.

### Costs and risks

- Natural-language semantic retrieval is unavailable in the MVP.
- Version 1 may require a new migration and packaging dependency.
- Users may expect semantic search because optional AI exists.
- Deferral requires resisting accidental embedding creation through provider APIs.

## Verification

- Search release dependencies, database schema, provider calls, configuration, and UI for vector-index creation or automatic embedding.
- Run all MVP search workflows with no model installed.
- Confirm the Ollama embedding operation in ADR 0017 is unreachable from MVP user workflows.
- Before a Version 1 proposal, benchmark deterministic search against candidate embedding models and stores on a redacted real corpus.
- Require secret-leakage, deletion, rebuild, model-change, backup, restore, storage-limit, and per-project-consent tests in the successor ADR.

## Revisit triggers

- Deterministic and fuzzy search fail measured discovery tasks.
- Users approve semantic search as a Version 1 priority.
- A safe embedded store satisfies packaging and deletion requirements.
- Provider or model changes alter privacy, dimensions, or local resource costs.

## Sources

- [Ollama embeddings capability](https://docs.ollama.com/capabilities/embeddings)
- [Ollama embedding API](https://docs.ollama.com/api/embed)
- [SQLite FTS5 extension](https://www.sqlite.org/fts5.html)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
