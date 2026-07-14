# Test Strategy

Status: **Gate 3 foundation suites accepted on 2026-07-14 for exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](../project/gate-3-evidence.md); later-gate quality contract proposed**

## Objectives

Testing proves deterministic correctness, managed allocation assurance, honest treatment of unmanaged evidence, privacy, accessibility, degradation, and portability of adapter contracts. Core suites must run on a clean development machine with no Docker daemon and no Ollama service.

The Gate 3 disposition accepts only the bounded foundation evidence identified in its sprint brief. It does not claim a runtime inventory, later-gate feature behavior, a completed security review, full `SRS-NFR-009`, packaging acceptance, or release readiness.

## Test pyramid and stable suites

| Test ID | Suite | Scope | Default dependencies | Release role |
|---|---|---|---|---|
| TEST-ARCH-001 | Foundation architecture | Inward dependency direction, adapter isolation, prohibited implementation surfaces | Standard-library source inspection | Every foundation change |
| TEST-ISO-001 | Optional-integration isolation | Docker/provider absence, explicit degradation, and unchanged authoritative state | Synthetic failing adapters; no live services | Every integration-boundary change |
| UT-DOM-001 | Domain unit and property tests | Entities, value objects, revisions, confidence, state transitions | Python standard test process | Every change |
| UT-CFG-001 | Configuration unit tests | Schema version, strict parsing, loopback/origin bounds, secret exclusion, platform-path seams | Temporary files and synthetic paths | Every configuration change |
| UT-COL-001 | Collector unit tests | Normalization, freshness, identity, safe error mapping | Recorded fixtures and fakes | Every change |
| UT-SCN-001 | Scanner unit and fixture tests | Each locked parser, path policy, provenance | Synthetic project trees | Every change |
| UT-ALC-001 | Allocator property tests | Range rules, exclusion, determinism, exhaustion | In-memory repository fake | Every change |
| IT-SQL-001 | SQLite integration | Migrations, transactions, crashes, leases, repository contracts | Temporary SQLite database | Every change |
| IT-PG-001 | PostgreSQL compatibility | Same repository contract and migration semantics | Opt-in PostgreSQL profile | Release candidate |
| IT-DKR-001 | Docker integration | API negotiation, normalization, permissions, degradation | Fake API by default; optional daemon | Release candidate |
| CT-API-001 | REST/SSE contract | Schemas, errors, idempotency, revisions, replay | In-process service | Every change |
| CT-CLI-001 | CLI contract | Version identity, help surface, stable machine output, prohibited commands | In-process CLI runner | Every CLI change |
| CT-MCP-001 | MCP contract | STDIO and HTTP protocol, scopes, copy, cancellation | In-process transports | Every change |
| E2E-CORE-001 | Core browser journey | Onboard, scan fixtures, inspect evidence, reserve, release | Packaged-like local stack; no Docker or AI | Release candidate |
| SEC-T-AUTH-001 | Security suite | Auth, origin, CSRF, permissions, traversal, secrets | Local adversarial fixtures | Every release candidate |
| SEC-T-SECRET-001 | Secret-boundary suite | Redaction canaries across configuration, errors, fixtures, logs, contracts, and diagnostics | Synthetic canaries only | Every security-boundary change |
| PERF-INV-001 | Capacity and latency | 500 repositories, 2,000 declarations, 1,000 observations | Generated deterministic corpus | Performance gate |
| AI-EVAL-SAFE-001 | Optional AI evaluation | Privacy, injection, grounding, schemas, isolation | Fake provider; optional local Ollama profile | AI inclusion gate only |

## Required techniques

- Example-based unit tests for normal and error flows
- Property tests for port ranges, lease transitions, idempotency, pagination, and revision ordering
- Golden and adversarial fixtures for each parser and collector
- Repository contract tests reused by SQLite and PostgreSQL
- Consumer-visible REST, SSE, CLI, and MCP contract tests
- Integration tests for transaction, migration, crash, permission, and degradation behavior
- Browser E2E tests for keyboard, accessibility, stale state, and user-visible copy
- Security and privacy canary testing at every serialization boundary
- Performance tests with fixed data generation, warm/cold distinction, and machine profile
- Manual founder UAT for product truth and real project coverage

## Quality thresholds

- All mandatory tests pass; flaky-test reruns do not convert failure to acceptance.
- Zero authorization bypass, secret canary leakage, symlink escape, forbidden mutation, or corrupting degradation.
- Parser recall is at least 90% on the labeled supported-format corpus; precision and per-parser misses are reported.
- Runtime changes reach the browser within two seconds under normal-load conditions defined in the performance plan.
- At target capacity, the ports table interaction remains within the documented latency budget and exposes no missing rows.
- Every acceptance scenario AC-001 through AC-015 passes its UAT mapping.
- Optional AI can fail or be absent while core state and all core suites remain green.

## Test environments

The default CI-equivalent environment uses temporary directories, synthetic identities, fixture clocks, an ephemeral SQLite database, fake host/Docker/provider adapters, and loopback networking. Separate opt-in profiles cover a live macOS host, Docker, PostgreSQL, and Ollama. Absence of an opt-in profile is reported as not executed, never as a passing integration.

## Evidence

Each gate records command, revision, environment profile, test counts, failures, duration, and artifact hashes. Screenshots supplement but do not replace assertions. Secret-bearing logs are never attached.
