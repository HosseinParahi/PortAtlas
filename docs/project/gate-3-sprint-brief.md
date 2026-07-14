# Gate 3 Engineering Foundation Sprint Brief

- **Status:** **OPEN** — local and hosted engineering evidence complete for exact candidate [`4adf1fb500b651e425735595db528fd42fffba73`](gate-3-evidence.md); exact-revision founder approval pending
- **Gate 2 input:** [Founder-approved revision `e53f399`](gate-2-approval.md)
- **Working branch:** `codex/gate3-engineering-foundation`
- **Gate owner:** Founder
- **Evidence rule:** No item passes from intent, file presence, or a narrower local check alone

## Goal

Establish a reproducible, typed Python and React monorepo foundation whose core checks run without Docker or Ollama. Gate 3 proves engineering coherence and quality controls. It does not prove host inventory accuracy, scanners, allocation behavior, primary user journeys, MCP integration, optional AI safety, packaging lifecycle, or release readiness.

## Scope boundaries

Gate 3 may add private working-title package metadata, dependency locks, domain and application contracts, persistence/configuration/authentication seams, adapter shells, a minimal versioned REST health surface, an accessible React foundation shell, synthetic fixtures, quality tooling, hooks, and CI.

Gate 3 must not:

- publish or reserve package, image, domain, bundle, manifest, Homebrew, MCP Registry, or other public namespaces;
- claim the `PortAtlas` working title is cleared;
- implement host or Docker collection, project scanning, reservation/lease behavior, conflict evaluation, production MCP tools, or optional AI behavior assigned to later gates;
- add source patching, managed launch, process termination, Docker lifecycle mutation, telemetry, remote AI, or a Tauri shell;
- treat a health shell or fixture UI as an implemented product workflow; or
- build, sign, notarize, install, publish, or lifecycle-test a release package.

Packaging in Gate 3 is limited to the bounded research spike in `G3-20`. Packaging selection and lifecycle proof remain Gate 9 work under [ADR 0007](../adr/0007-packaging.md).

## Evidence-bound work items

Every identifier is stable for this sprint. A status of **Evidence pending** means the work may be active but is not accepted.

| ID | Work item and boundary | Required evidence | Status |
| --- | --- | --- | --- |
| `G3-00` | Record exact Gate 2 approval and authorize only the Gate 3 engineering foundation. | [Approval record](gate-2-approval.md) identifies the immutable revision, date, branch, exclusions, and provenance treatment. | Accepted |
| `G3-01` | Maintain this sprint brief and one evidence ledger; do not expand the gate through implementation convenience. | All `G3-00`–`G3-21` rows have explicit scope, verification, and disposition. | Engineering evidence complete; exact-revision gate disposition open |
| `G3-02` | Pin supported Python, Node, uv, and pnpm toolchains. Pins are contributor inputs, not public product-runtime promises. | Machine-readable pins agree with lock metadata; clean-run evidence records actual versions and supported CI matrix. | Candidate-local passed |
| `G3-03` | Establish the private monorepo and deterministic Python/JavaScript locks. No package is publishable under the working title. | Workspace manifests are private/non-publishable, frozen installs succeed, lockfiles are committed, and drift checks fail on unlocked changes. | Candidate-local passed |
| `G3-04` | Add the typed Python modular-monolith foundation with inward dependency direction. No collector, scanner, allocator, or AI feature behavior enters this item. | Import/architecture tests and type checks prove the domain package has no web, SQL, OS, Docker, or model-provider dependency. | Candidate-local passed |
| `G3-05` | Implement foundational domain contracts: opaque IDs, injected time, revisions, `PortKey`, logical `Project`, and worktree-aware `ProjectInstance`. | Focused unit tests cover validation, identity separation, lifecycle vocabulary, deterministic time, and serialization boundaries. | Candidate-local passed |
| `G3-06` | Define repository and unit-of-work protocols plus SQLite/PostgreSQL-compatible persistence seams. Feature repositories and lease algorithms remain later work. | Contract tests exercise protocol fakes and the minimal SQLite adapter; migrations and PostgreSQL compatibility are opt-in where infrastructure is required. | Candidate-local passed, including PostgreSQL 18.3 profile |
| `G3-07` | Establish versioned configuration loading and platform path seams with secure defaults. No final public manifest namespace is created. | Tests prove loopback defaults, no telemetry, safe path/config validation, redacted errors, and isolated temporary state. | Candidate-local passed |
| `G3-08` | Establish authentication primitives and permission vocabulary without claiming complete browser, CLI, or MCP authentication flows. | Tests cover entropy, token hashing/verification, constant-time comparison, scopes, user-only credential-file permissions, and secret-safe failures. | Candidate-local passed |
| `G3-09` | Add CLI, MCP, collector, Docker, scanner, and optional-provider adapter interfaces that call inward. Interfaces are seams, not feature implementations. | Architecture/contract tests prove dependency direction, the MCP revision constant, and import-safe absence of optional integrations. | Candidate-local passed |
| `G3-10` | Add a minimal `/api/v1` REST application shell with canonical safe errors and health separation. No product resources or commands are implied. | Contract tests prove liveness is minimal, readiness is authenticated, OpenAPI is versioned, request IDs are safe, and contract drift is detected. | Candidate-local passed |
| `G3-11` | Add a strict React/Vite workspace and project-owned wrappers for TanStack Query, TanStack Table, and Radix behavior. This is a foundation/demo shell, not Gate 7 UX. | Type, component, accessibility, focus-return, reduced-motion, responsive, managed/unmanaged-copy, and API-client drift checks pass. | Candidate-local passed |
| `G3-12` | Select one machine-readable internal version authority and keep Python, REST/OpenAPI, CLI, MCP, web, and diagnostics seams consistent. No public product version or tag is assigned. | An automated drift check compares every implemented version surface to the authority and rejects mismatch. | Candidate-local passed |
| `G3-13` | Establish unit, contract, integration, architecture, security, and web test harnesses with deterministic clocks, state, and network boundaries. | Test collection proves each suite exists, failures propagate, temporary state is isolated, and default execution needs no live services. | Candidate-local passed |
| `G3-14` | Add synthetic fixture-family catalogs for future runtime evidence, projects/worktrees, parser inputs, redaction, conflicts, capacity, and optional providers without implementing later-gate behavior. | Catalog metadata is synthetic, deterministic, versioned, secret-canary-safe, and loadable by tests without private paths or services; behavioral payloads and goldens remain in their owning gates. | Candidate-local passed |
| `G3-15` | Provide one documented contributor command surface for bootstrap, format, lint, type, test, contract drift, docs, security, and aggregate checks. | Every documented supported command is executed from a clean state; help/output and failure behavior match the guide. | Candidate-local passed |
| `G3-16` | Add local hooks and hosted CI using the same contributor commands and locked installs. Hooks must not hide CI-only behavior. | Hook configuration is executable; CI covers supported toolchains, caches only locked inputs, uploads no private data, and records a green required run. | Engineering evidence complete; hosted CI, exact-history DCO, and aggregate successful |
| `G3-17` | Prove Docker, PostgreSQL, Ollama, Rust, and packaging tools are absent from the default core path. Optional profiles must report not executed rather than passing when unavailable. | Default bootstrap/checks pass with optional services disabled and imports blocked; targeted degradation tests leave authoritative state unchanged. | Candidate-local passed |
| `G3-18` | Add secret, dependency, license, vulnerability, and supply-chain controls proportionate to a foundation checkpoint. No result is treated as a release SBOM or security approval. | Frozen-lock, secret scan, dependency review, license review, vulnerability policy, workflow-permission, and generated-file provenance checks have recorded outcomes. | Engineering evidence complete; hosted dependency review successful on PR attempt 2 |
| `G3-19` | Close Phase 3 research decisions that affect the engineering foundation and carry later behavioral questions forward to their owning gates. | Decision/open-question registers identify selected stack/toolchain facts, deferred runtime validation, sources, date, and owning gate without contradicting Accepted ADRs. | Candidate-local passed |
| `G3-20` | Run a bounded native-packaging research spike only: test feasibility assumptions and document the Gate 9 experiment plan. Do not create a release-candidate artifact or select a final lifecycle. | [Research memo](gate-3-packaging-research.md) records hypotheses, a disposable experiment, constraints, risks, and Gate 9 measurements; no native-packaging dependency enters default runtime or checks. | Research evidence complete; Gate 9 packaging acceptance deferred |
| `G3-21` | Assemble the Gate 3 evidence record and obtain an explicit disposition for one exact revision. | Evidence includes commands, versions, lock state, test/check counts, durations, CI URL/revision, skipped optional profiles, risks, docs validation, Git state, and founder disposition. | **OPEN** — engineering evidence complete; exact-revision founder approval pending |

## Traceability

Gate 3 primarily implements `US-010` through `US-013`, `SRS-NFR-006`, and the foundation subset of `SRS-NFR-009`. It establishes seams for other requirements without claiming their behavior. Detailed mapping is maintained in the [traceability matrix](../requirements/traceability-matrix.md#gate-3-foundation-traceability).

The evidence catalog uses the accepted verification records `VT-SRS-NFR-006` and `VT-SRS-NFR-009`. More focused automated test IDs may be added by the implementation, but they must be defined once in the test documentation and may not replace the upstream verification records.

## Verification and command-promotion rule

The expected Gate 3 evidence categories are:

1. frozen dependency installation from both committed lockfiles;
2. Python and TypeScript formatting, lint, and strict type checks;
3. unit, contract, integration, architecture, security, and browser tests;
4. REST/OpenAPI and generated-client drift checks;
5. documentation, internal-link, stable-ID, placeholder, path, and secret checks;
6. default core execution with Docker, PostgreSQL, Ollama, Rust, and packaging tools disabled;
7. local hook execution and a required hosted-CI run for the exact candidate revision; and
8. clean Git/lock state with no public artifact or namespace publication.

Commands are promoted to supported contributor instructions only after they exist and their successful invocation is recorded in [Development setup](../operations/development-setup.md). Until then, this brief describes evidence outcomes rather than executable syntax.

## Risks and stop conditions

- Stop if the private package metadata can publish accidentally or claims a cleared public name.
- Stop if business rules enter REST, CLI, MCP, or React adapters instead of shared application/domain services.
- Stop if a default check reaches Docker, PostgreSQL, Ollama, a remote model, or telemetry endpoint.
- Stop if fixture/log/error output includes a credential, private project path, or secret-bearing process content.
- Stop if the managed allocation boundary is presented as a guarantee for unmanaged processes.
- Stop if the native-packaging spike produces or distributes a release-like artifact.
- Do not close Gate 3 from local checks alone when the gate contract requires hosted CI evidence.

## Demo and exit disposition

The Gate 3 demo is an engineering evidence review, not a product demo: reproduce the locked bootstrap, exercise the minimal authenticated service/client seams, show the accessible foundation shell with synthetic data, run the aggregate quality command without optional services, and trace failures to stable checks.

Gate 3 passes only when `G3-00` through `G3-21` have accepted evidence, the exact candidate revision is recorded, required CI is green for that revision, the worktree is clean, and the founder explicitly approves the disposition. Until then, the repository status remains **Gate 3 in progress**.
