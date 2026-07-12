# Work Log

## 2026-07-11 — First checkpoint

### Intent

Convert the founder's master brief into a reviewable, traceable documentation baseline and stop before production implementation.

### Completed research activities

- Verified the local toolchain snapshot without adopting it as a product minimum.
- Reviewed official baselines for Python, React, Vite, Docker Engine, MCP transports and Python SDK, accessibility primitives, packaging, and Ollama structured output.
- Compared system utilities, container tooling, proxy-first tools, and lightweight port managers with the proposed inventory-and-evidence position.
- Performed preliminary exact-name searches across source and package registries, domains, and trademark indexes. The results triggered a release-blocking naming ADR rather than a claim of availability.
- Reconciled licensing with the founder's open-source decision: Apache-2.0 permits commercial use without payment; sponsorship is voluntary.

### Checkpoint deliverables

- Repository governance and contributor policy
- Product, UX, requirements, and fifteen-scenario traceability
- Architecture, contracts, domain and data models, and ADRs 0001–0023
- Security, testing, operations, release, and delivery proposals
- Standard-library documentation validation with automated tests

### Explicitly excluded

- Application scaffolding, production code, and dependency installation
- Package, image, domain, and manifest publication
- Remote push or release creation
- Phase 3 engineering work

### Handoff condition

The founder reviews decisions and open questions, approves or rejects Gate 2, and supplies release-gate inputs where required. Gate 3 work begins only after explicit approval.

### Validation record

The completed checkpoint was checked with the standard-library documentation validator, its adversarial regression suite, Git whitespace validation, stable-ID and fifteen-scenario audits, ADR sequence/content checks, internal link and asset checks, secret/personal-path scans, and a repository-content audit confirming that the only Python files are documentation tooling and tests.

The local history is intentionally organized as:

1. `chore: establish project governance and research baseline`
2. `docs: define PortAtlas product and requirements`
3. `docs: record architecture security and test strategy`
4. `docs: add delivery roadmap and release gates`

No dependency was installed, no application scaffold or production code was added, no namespace or package was published, and no remote push was performed in the Gate 2 checkpoint. At the time the checkpoint was committed, Gate 3 was blocked on explicit founder approval.

## 2026-07-11 — Gate 2 approval and Gate 3 authorization

### Founder disposition

The founder approved the exact Gate 2 revision `e53f39916b2348e8626375bb33cac147e27bd217` and authorized Gate 3 engineering-foundation work. The immutable approval scope and initial-history provenance treatment are recorded in [Gate 2 founder approval](gate-2-approval.md).

The first commit, `8081f409f54f088d61f9a36433b7e56f2410e66f`, has no `Signed-off-by` trailer. The founder approved retaining the accepted history and recording a forward provenance attestation instead of rewriting the root commit. Later commits remain subject to the repository sign-off rule.

### Gate 3 start

Gate 3 work is isolated on `codex/gate3-engineering-foundation` and governed by the evidence-bound [Gate 3 sprint brief](gate-3-sprint-brief.md). Authorization to start is not evidence that the gate passed. Implementation, toolchain, locks, commands, tests, hooks, CI, optional-dependency isolation, security checks, and exact-revision disposition remain to be recorded before Gate 3 can close.

Packaging is a bounded Gate 3 research spike only. Distributable artifacts, signing, notarization, install/service lifecycle, migration/recovery, SBOM, and release packaging acceptance remain Gate 9 work. No package or public namespace publication is authorized, and `PortAtlas` remains a working title.

## 2026-07-13 — Gate 3 candidate-local verification

### Foundation assembled

- Pinned CPython 3.13.14 with a 3.14.6 compatibility matrix, uv 0.11.28, Node 24.18.0, and Corepack pnpm 11.10.0.
- Committed private uv/pnpm dependency graphs and enforced lock drift, non-publication metadata, SHA-pinned actions, digest-pinned service images, least privilege, matching DCO history, dependency review, and supported automated updates.
- Added the typed modular-monolith domain/application foundation, repository/UoW fakes, SQLAlchemy identity persistence, Alembic/metadata drift protection, strict schema-versioned configuration, token/security primitives, adapter interfaces, minimal REST health/readiness, CLI/MCP contracts, generated OpenAPI/client types, and an accessible synthetic React shell.
- Added deterministic unit, contract, integration, architecture, security, browser, optional-degradation, and documentation/foundation validator suites.

### Independent-review remediation

The closure audit found and corrected false-green gaps: the toolchain command now executes the selected Python; migrated databases match repository tables; PostgreSQL uses the same migration; trusted origins reject credentials/query/fragment/invalid ports; readiness 503 matches OpenAPI; adapter siblings cannot import one another; safe errors/events recursively snapshot data and reject secret-shaped/non-finite values; focused test IDs must be defined; secret scanning covers source and locks; advisory/license checks cover development, build, optional, and packaging dependencies; Python 3.14 tests use the selected matrix interpreter; job-level workflow permissions cannot grant writes; and PR DCO checks inspect authored commits rather than GitHub's synthetic merge commit.

### Candidate-local results

The final default aggregate passed in 25.49 seconds. The Python suite passed 101 tests with one explicit PostgreSQL deselection and 87.63% coverage; API-client and browser suites passed 4 and 7 tests. Format, lint, import architecture, strict types, generated contracts, service smoke, locked private builds, optional-integration isolation, clean offline frozen installs, Python 3.14 compatibility, PostgreSQL 18.3 migration/repository compatibility, installed local hooks, the disposable packaging repeat, complete advisory audits, and license inventory passed. Detailed hashes, durations, profiles, and limitations are in the [Gate 3 evidence ledger](gate-3-evidence.md).

Hosted CI, the exact candidate revision, final clean Git state, and immutable disposition remain open. No Gate 4 behavior, package, image, domain, manifest namespace, model, release artifact, or publication was created.
