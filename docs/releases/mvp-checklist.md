# MVP Release Checklist

Status: **Proposed pre-release checklist; product behavior remains unverified**

## How to use this checklist

An unchecked item means no release evidence has been accepted for that item. It is an explicit unverified state, not a claim that work exists. Gate dispositions may be checked when exact evidence and reviewer disposition exist; release-candidate items are checked only in the release pull request.

At this checkpoint:

- Gate 2 was founder-approved on 2026-07-11 at exact revision [`e53f399`](../project/gate-2-approval.md).
- Gate 3 candidate-local evidence is complete in the [evidence ledger](../project/gate-3-evidence.md); exact-revision hosted CI and founder binding remain open.
- Foundation contributor checks and private metadata/browser builds are verified. No native package, install, sign, publish, or release command is claimed.
- PortAtlas is a working title. Gate 9 and public release are ineligible while the public-name clearance gate remains blocking.

## A. Gate and scope control

- [x] Gate 2 founder approval links the exact requirements, architecture, MVP scope, threat model, test strategy, deployment strategy, and ADR revision at [`e53f399`](../project/gate-2-approval.md).
- [ ] Gate 3 records pinned toolchains, locked dependencies, supported contributor commands, exact-revision green hosted CI, and founder disposition. Local evidence is complete; hosted binding remains open.
- [ ] All Must requirements have stable SRS IDs and trace to AC, VT-SRS, or UAT evidence.
- [ ] Every included issue and pull request lists its US, SRS, AC, VT-SRS, UAT, ADR, and risk impact.
- [ ] Deferred Version 1 and future capabilities are absent from MVP claims.
- [ ] Gate 9 approval applies to one immutable candidate revision and artifact set.

## B. Public identity, license, and contribution provenance

- [ ] ADR 0023 is Accepted with dated repository, registry, domain, and trademark/name-collision evidence.
- [ ] The accepted public name is consistent across repository, packages, executables, services, bundle identifiers, MCP identity, manifest filename, documentation, and domains.
- [ ] The official Apache-2.0 LICENSE text and required NOTICE material are included.
- [ ] Dependency, asset, model, and bundled-tool license evidence is reviewed.
- [ ] Documentation states that Apache-2.0 allows commercial use without payment to the maintainers.
- [ ] Sponsorship is described as voluntary and is not tied to use, commercial rights, features, updates, security handling, support, or telemetry.
- [ ] Every post-baseline contribution has a matching Developer Certificate of Origin `Signed-off-by` trailer; the unchanged root commit is covered by the reviewed [forward provenance attestation](../project/gate-2-approval.md#provenance-attestation-for-the-root-commit).
- [ ] CODEOWNERS review is satisfied for release, requirement, architecture, security, and GitHub-governance changes.

## C. Product truth and managed/unmanaged boundary

- [ ] Observed, declared, reserved, leased, desired, conflicted, stale, unknown, and ignored states remain distinct in domain, storage, API, UI, CLI, MCP, export, and documentation.
- [ ] Reservation and lease claims are limited to coordination among PortAtlas-aware clients.
- [ ] Source-patching tools and endpoints are absent from the MVP.
- [ ] Managed-launch tools, endpoints, and commands are absent from the MVP and identified only as Version 1 candidates.
- [ ] Process-termination tools and endpoints are absent from the MVP.
- [ ] Docker lifecycle tools and endpoints for start, stop, remove, exec, pull, or equivalent mutation are absent from the MVP.
- [ ] Unmanaged terminals, IDEs, scripts, Docker commands, and applications are described as able to ignore or race the registry.
- [ ] No surface promises zero conflicts or guaranteed continued availability for an unmanaged launch.
- [ ] Runtime and static findings display evidence, confidence, freshness, and permission limitations.

## D. Core functional evidence

- [ ] Host collection proves TCP and UDP, IPv4 and IPv6, bind address, PID plus start time, process identity, and permission degradation on supported macOS.
- [ ] Docker mapping proves host versus container ports, Compose identity, events plus reconciliation, and correct Docker-disabled behavior.
- [ ] Approved-root discovery, canonical paths, symlink policy, worktree identity, scan preview, pause, cancellation, and exclusions pass.
- [ ] The locked parser corpus meets exact-detection thresholds and reports precision, misses, confidence, evidence, and parser versions.
- [ ] Policies, suggestions, reservations, releases, leases, expiry, idempotency, conflict types, exposure, and audit pass deterministic tests.
- [ ] Concurrent clients cannot receive the same scoped active lease.
- [ ] REST, SSE, CLI, and MCP expose the same application semantics and typed errors.
- [ ] Browser setup, overview, ports, projects, conflicts, reservations, settings, integrations, demo, keyboard, and responsive flows pass.

## E. Security and privacy

- [ ] Local HTTP and MCP bind to loopback by default and reject unauthorized Host and Origin behavior.
- [ ] Root, browser, CLI, and MCP credentials satisfy storage, scope, rotation, revocation, replay, CSRF, and redaction tests.
- [ ] Approved-root, canonical-path, symlink, traversal, command-injection, output-bound, timeout, and denial-of-service tests pass.
- [ ] Docker-socket authority is isolated and no unauthenticated daemon-control surface exists.
- [ ] Secret canaries are absent from database, API, SSE, CLI, MCP, UI, logs, audit, backups, exports, diagnostics, snapshots, and AI context.
- [ ] Outbound-network evidence proves no telemetry, analytics, crash upload, project data, process data, or model context leaves the machine by default.
- [ ] Diagnostic bundles are local, explicitly generated, previewed, redacted, and never uploaded automatically.
- [ ] Critical and High security findings are zero; Medium findings have founder-approved disposition.
- [ ] Private vulnerability reporting instructions are available and public templates warn against secret or exploit disclosure.

## F. Conditional AI

- [ ] Release notes explicitly state whether AI is excluded or included but disabled by default.
- [ ] Core suites pass with Ollama absent, stopped, invalid, overloaded, and disabled.
- [ ] No provider, model, model download, remote endpoint, or cloud fallback activates automatically.

If AI is excluded, the preceding three items complete the MVP AI disposition. If AI is included, every following item is also mandatory:

- [ ] ADRs 0016 through 0022 are implemented and security-reviewed.
- [ ] AI-EVAL-SAFE-001 and applicable AC-011 through AC-015 evidence pass for the exact provider version and model digest.
- [ ] AI receives only the fixed read-only tool allowlist and cannot mutate state, read arbitrary files, run shell commands, control processes, or broaden roots.
- [ ] Context minimization, secret redaction, prompt-injection defenses, strict structured-output validation, evidence checks, cancellation, and resource bounds pass.
- [ ] Raw prompts and complete responses are not stored by default; user-selected artifacts, retention, invalidation, export exclusion, and complete deletion work.
- [ ] Provider failure leaves authoritative core state unchanged and generated output is visibly advisory.

## G. Test and verification evidence

- [ ] UT-DOM-001, UT-COL-001, UT-SCN-001, and UT-ALC-001 pass.
- [ ] IT-SQL-001 passes; IT-PG-001 and IT-DKR-001 pass when included in the candidate profile.
- [ ] CT-API-001 and CT-MCP-001 pass across supported transports and auth failures.
- [ ] E2E-CORE-001 passes without Docker and without AI.
- [ ] SEC-T-AUTH-001 and all mapped security/privacy checks pass.
- [ ] PERF-INV-001 records the reference 500-project, 2,000-declaration, and 1,000-observation result.
- [ ] All applicable VT-SRS records include exact invocation, environment, counts, failures, duration, hashes, and reviewer.
- [ ] UAT-001 through UAT-015 have founder dispositions; conditional AI cases follow the inclusion rule.
- [ ] Screenshots supplement assertions and contain no secrets or private machine data.

## H. Packaging, migration, and lifecycle

The bounded Gate 3 packaging spike is research input only and checks none of the items in this section. These are Gate 9 evidence requirements.

- [ ] ADR 0007 is Accepted with selected macOS artifact, service lifecycle, signing, notarization, update, rollback, and uninstall design.
- [ ] Clean installation succeeds on each supported macOS architecture without repository clone, system Python, Node, Docker, Ollama, cloud account, or persistent administrator access.
- [ ] Artifact signature, notarization, checksum, SBOM, provenance, LICENSE, and NOTICE checks pass.
- [ ] Service start, stop, restart, status, logs, browser bootstrap, crash recovery, and credential rotation pass.
- [ ] Database and configuration migrations pass from every supported source version.
- [ ] Failed migration preserves prior data and produces the documented rollback or recovery behavior.
- [ ] Backup, restore, upgrade, rollback, diagnostic export, and uninstall drills pass.
- [ ] Uninstall asks separately about local state and never deletes project sources, Docker resources, Ollama models, or global toolchains.
- [ ] Residue inspection matches the documented data-retention choice.

## I. Documentation and release communication

- [ ] README, architecture, requirements, operations, security, testing, release, contribution, governance, support, and code-of-conduct documents match the candidate.
- [ ] Supported platforms, permissions, data locations, configuration locations, limitations, backup, restore, troubleshooting, and uninstall are documented.
- [ ] Release notes identify source revision, artifact hashes, migrations, rollback limit, known issues, managed/unmanaged assurance, telemetry policy, and AI state.
- [ ] Security instructions direct vulnerability reports away from public issues and warn against attaching secrets.
- [ ] Bug and feature forms request requirement/test references and reproducible redacted evidence.
- [ ] Every documented user or contributor invocation was executed in the stated environment; planned invocations are not presented as working.

## J. Final approval

- [ ] The release evidence record contains candidate version, source revision, artifact and SBOM hashes, environments, exact executed invocations, test IDs, results, reviewers, deviations, and risk dispositions.
- [ ] Candidate artifact hashes match the signed and notarized files proposed for publication.
- [ ] Release manager, QA reviewer, security reviewer, maintainer reviewer, and founder dispositions are recorded.
- [ ] Gate 9 is explicitly approved for the exact candidate.
- [ ] Publication targets are the cleared namespaces and no artifact is silently replaced after release.

## Immediate abort conditions

Do not publish when any of these is true:

- the public-name gate is unresolved;
- a Must requirement lacks evidence;
- a mandatory test or UAT case fails;
- a Critical or High finding is open;
- a secret, token, private path, or unredacted exploit appears in evidence;
- unauthorized telemetry or remote AI traffic occurs;
- managed/unmanaged claims are misleading;
- AI is included without its complete conditional gate;
- artifacts are unsigned, mismatched, unreproducible, or lifecycle recovery fails.

## Related documents

- [Release process](release-process.md)
- [Versioning policy](versioning.md)
- [Roadmap](../product/roadmap.md)
- [Traceability matrix](../requirements/traceability-matrix.md)
- [Acceptance criteria](../requirements/acceptance-criteria.md)
- [Test strategy](../testing/test-strategy.md)
- [UAT plan](../testing/uat-plan.md)
