# PortAtlas Non-functional Requirements

## Conventions

These requirements constrain every applicable functional requirement. Priority uses MoSCoW relative to the MVP. Verification IDs are defined in [Acceptance criteria](acceptance-criteria.md), component IDs in the [SRS](srs.md#7-architecture-component-identifiers), and metric methods in [Success metrics](../product/success-metrics.md).

## Privacy and security

### SRS-SEC-001 — Local-first privacy and offline core

- **Priority:** Must
- **Description:** Project/process/path/configuration/port data shall stay on the machine unless a separately approved remote feature is explicitly enabled; core inventory, discovery, conflict, registry, UI, API, CLI, and MCP shall operate without internet.
- **Rationale:** Local repository and process metadata is sensitive, and offline use is a core value.
- **Inputs:** Supported local installation with network egress unavailable; Docker and Ollama may be absent.
- **Preconditions:** A supported local installation is available; remote features have not been separately enabled.
- **Normal flow:** Resolve the task locally, avoid remote dependencies, and return core results through local interfaces.
- **Outputs:** Core capabilities remain usable and no automatic remote call, cloud fallback, telemetry, model install, or GitHub API dependency occurs.
- **Error flow:** A feature requiring an unavailable optional local/external endpoint is marked degraded without blocking core.
- **Security constraints:** Any future remote capability requires explicit opt-in, threat/privacy review, and separate data disclosure.
- **Acceptance:** `SM-09`; `AC-010` for AI absence.
- **Backlog:** `US-092`.
- **Related tests:** `VT-SRS-SEC-001`, `UAT-010`.
- **Components:** All, led by `CMP-SEC`, `CMP-CFG`, `CMP-API`.

### SRS-SEC-002 — Secret non-disclosure

- **Priority:** Must
- **Description:** No secret value or complete environment file shall appear in default logs, API/MCP responses, UI, telemetry, model context, embeddings, snapshots, exports, diagnostic bundles, test snapshots, or bug reports.
- **Rationale:** Discovery touches high-risk sources and a single leakage path breaks local trust.
- **Inputs:** Canary-secret fixtures across environment, process arguments, URLs, files, model prompts/results, backups, and diagnostics.
- **Preconditions:** A component is about to parse, persist, transport, render, export, log, or summarize potentially sensitive data.
- **Normal flow:** Minimize input, detect and redact secrets before persistence/transport, and rescan every outward artifact.
- **Outputs:** Only minimum port-relevant safe metadata survives; unrelated values and complete lines are absent.
- **Error flow:** Secret detection blocks or redacts the operation and records only safe redaction metadata.
- **Security constraints:** Redaction happens before persistence/transport and again around AI context/output; raw prompts remain off by default.
- **Acceptance:** Zero seeded-secret matches under `SM-08`; `AC-005` and `AC-014`.
- **Backlog:** `US-033`, `US-092`.
- **Related tests:** `VT-SRS-SEC-002`, `UAT-005`, `UAT-014`.
- **Components:** `CMP-SEC`, `CMP-SCN`, `CMP-AUD`, `CMP-AI`, `CMP-CFG`.

### SRS-SEC-003 — Least privilege and attack resistance

- **Priority:** Must
- **Description:** PortAtlas shall bind locally by default, scan only canonical approved roots, use argument arrays and limits for subprocesses, authenticate mutating HTTP, validate origin/scope/tool/path inputs, require dry-run/confirmation for mutation, and never automatically elevate, expose Docker, kill processes, or execute arbitrary model/repository instructions.
- **Rationale:** Local web, filesystem, Docker, MCP, and model integrations form a privileged attack surface.
- **Inputs:** Path traversal, symlink escape, command injection, malicious project file, ReDoS/oversize, unauthorized HTTP/origin/token, Docker socket, prompt injection, malicious model output, and resource-exhaustion fixtures.
- **Preconditions:** A filesystem, subprocess, HTTP, Docker, MCP, configuration, or model request enters a trust boundary.
- **Normal flow:** Canonicalize scope, authenticate/authorize, validate and bound input, then execute only the allowlisted read or confirmed transaction.
- **Outputs:** Attacks are rejected with stable safe errors; unaffected core remains available; mutation/audit state is unchanged unless an authorized transaction commits.
- **Error flow:** Fail closed for unsafe mutation and fail safely/degraded for read-only capability limitations.
- **Security constraints:** No untrusted text can redefine policy, permissions, system instructions, or fixed tool allowlists.
- **Acceptance:** Security suite passes; `AC-013` rejects repository prompt injection and `AC-007` identifies unsafe exposure.
- **Backlog:** `US-072`, `US-092`.
- **Related tests:** `VT-SRS-SEC-003`, `UAT-007`, `UAT-013`.
- **Components:** `CMP-SEC` plus every input adapter.

## Performance and capacity

### SRS-NFR-001 — Responsiveness and bounded work

- **Priority:** Must
- **Description:** Scans shall be incremental/cancellable; file/subprocess/provider work shall not block the API event loop; concurrency/output/context shall be bounded; watchers debounced; lists paginated; targeted parsers preferred; runtime changes shall appear within two seconds under normal load.
- **Rationale:** A developer control center must remain interactive during machine and repository work.
- **Inputs:** Reference normal-load dataset, controlled listener changes, scan storms, slow collector/provider, large but permitted files.
- **Preconditions:** The documented normal-load dataset and supported machine profile are active.
- **Normal flow:** Schedule bounded incremental work, debounce/cache/paginate as applicable, support cancellation, and publish the reconciled update.
- **Outputs:** `SM-04` meets its latency target; UI/API remain responsive and cancellation terminates work safely.
- **Error flow:** Backpressure, cancellation, timeout, or partial progress is visible; queues/retries do not grow indefinitely.
- **Security constraints:** Limits also defend denial-of-service paths.
- **Acceptance:** 95th-percentile runtime update at or below two seconds under documented normal load.
- **Backlog:** `US-023`, `US-091`.
- **Related tests:** `VT-SRS-NFR-001`.
- **Components:** `CMP-COL`, `CMP-DKR`, `CMP-SCN`, `CMP-API`, `CMP-WEB`, `CMP-AI`.

### SRS-NFR-002 — Developer-laptop scale

- **Priority:** Must
- **Description:** The MVP shall manage at least 500 repositories, 2,000 declarations, and 1,000 runtime observations on the documented reference laptop without noticeable UI lag.
- **Rationale:** The primary user runs many simultaneous projects and services.
- **Inputs:** Versioned synthetic/reference dataset at or above all three target counts.
- **Preconditions:** The versioned 500-repository, 2,000-declaration, 1,000-observation reference dataset is loaded.
- **Normal flow:** Index and query the reference data through normal pagination/cache paths while measuring interaction and reconciliation behavior.
- **Outputs:** Filter, sort, search, pagination, row/project navigation, reconciliation, and conflict queries remain within the performance-plan thresholds and founder UAT feels responsive.
- **Error flow:** Resource pressure is reported; background work remains bounded/cancellable rather than starving interaction.
- **Security constraints:** Scaling shall not require wider scan scope or remote processing.
- **Acceptance:** `SM-10` benchmark and UAT record pass.
- **Backlog:** `US-091`.
- **Related tests:** `VT-SRS-NFR-002`.
- **Components:** `CMP-DB`, `CMP-DOM`, `CMP-API`, `CMP-WEB`, `CMP-SCN`.

## Reliability and integrity

### SRS-NFR-003 — Failure isolation and recoverability

- **Priority:** Must
- **Description:** Collector, Docker, watcher, optional AI, and individual parser failures shall not crash the service; last-known-good timestamped state shall remain, restart shall reconcile, migrations/config corruption shall have recovery, and background tasks shall shut down cleanly.
- **Rationale:** Optional or platform-sensitive components will fail in normal local use.
- **Inputs:** Component exceptions, timeout, malformed data, provider restart, service restart, corrupt config, interrupted migration, shutdown during background work.
- **Preconditions:** The native service is running and one or more supervised components or background tasks are active.
- **Normal flow:** Supervise each component, retain timestamped last-good state, isolate failure, and reconcile after recovery or restart.
- **Outputs:** Failure is localized and visible; healthy components and authoritative state continue; recovery produces a reconciled state.
- **Error flow:** Bounded retry/backoff and explicit last-success/staleness; no indefinite background loop.
- **Security constraints:** Recovery artifacts/logs remain redacted and permissions preserved.
- **Acceptance:** Fault-injection suite; `AC-010`; lifecycle `SM-11`.
- **Backlog:** `US-023`, `US-100`.
- **Related tests:** `VT-SRS-NFR-003`, `UAT-010`.
- **Components:** All, led by `CMP-DOM`, `CMP-DB`, `CMP-AUD`.

### SRS-NFR-004 — Transactional allocation and idempotency

- **Priority:** Must
- **Description:** Reservations and leases shall be transaction-safe, atomic under concurrency, bounded by uniqueness/owner/expiry rules, and idempotent where client retries are expected.
- **Rationale:** Race-free coordination is the product's safety-critical differentiator for integrated clients.
- **Inputs:** Simultaneous same-range requests, duplicate idempotency keys, expiry/renew/release races, process appearing during a lease.
- **Preconditions:** Authorized clients share a healthy transactional persistence/registry boundary.
- **Normal flow:** Begin the transaction/lock, validate owner and uniqueness, commit one idempotent result, then publish audit/reconciliation state.
- **Outputs:** No two active conflicting leases commit; failed transactions leave no partial state; reconciliation reports external collisions.
- **Error flow:** Return stable collision/expired/stale errors and a re-evaluable alternative.
- **Security constraints:** Owner/scope authorization and audit for every mutation; AI has no direct lease authority.
- **Acceptance:** `SM-07`; `AC-004`, `AC-008`, `AC-009`.
- **Backlog:** `US-042`.
- **Related tests:** `VT-SRS-NFR-004`, `UAT-004`, `UAT-008`, `UAT-009`.
- **Components:** `CMP-REG`, `CMP-DB`, `CMP-AUD`.

## Usability and accessibility

### SRS-NFR-005 — WCAG 2.2 AA-oriented accessibility

- **Priority:** Must
- **Description:** Primary UI flows shall meet WCAG 2.2 AA where practical, including full keyboard navigation, visible focus, semantic/screen-reader labels, status/error announcements, contrast, reduced motion, responsive layouts, accessible table alternatives, and no color-only state.
- **Rationale:** Dense operational data must remain usable across input and assistive technologies.
- **Inputs:** Light/dark themes, keyboard-only, supported screen reader/browser, reduced-motion, narrow viewport, error/degraded/generated states.
- **Preconditions:** A primary UI flow is rendered in a supported browser and viewport.
- **Normal flow:** Render semantic structure, maintain focus/keyboard order, announce status/errors, and present equivalent text/icon information.
- **Outputs:** All primary flows are operable and understandable with equivalent state/action information.
- **Error flow:** Accessibility regressions block the relevant UI Definition of Done.
- **Security constraints:** Accessible labels/errors shall not reveal redacted data.
- **Acceptance:** `SM-15`; automated scan has no critical issue and manual checklist passes.
- **Backlog:** `US-063`, `US-090`.
- **Related tests:** `VT-SRS-NFR-005`.
- **Components:** `CMP-WEB`.

## Engineering quality and portability

### SRS-NFR-006 — Maintainable typed modular design

- **Priority:** Must
- **Description:** Backend shall use typed Python, frontend strict TypeScript, focused modules, stable interfaces, generated/validated contracts, parser fixtures, ADRs, clear ownership, and no giant service classes or duplicated business logic in clients/AI.
- **Rationale:** Multiple platform and integration surfaces require boundaries that can evolve safely.
- **Inputs:** Code/design review, type/lint/test runs, dependency and architecture changes.
- **Preconditions:** Approved architecture contracts and repository quality commands are available.
- **Normal flow:** Implement through typed focused boundaries, run quality/contract checks, review dependencies, and update tests/docs with behavior.
- **Outputs:** Components in the SRS can be tested independently; behavior changes update docs/tests/contracts in the same change.
- **Error flow:** Contract drift, type/lint failure, undocumented architectural change, or unreviewed significant dependency blocks completion.
- **Security constraints:** Security-sensitive areas require review and supply-chain/license checks.
- **Acceptance:** Gate 3 and Definition-of-Done quality checks pass.
- **Backlog:** `US-010`, `US-011`.
- **Related tests:** `VT-SRS-NFR-006`.
- **Components:** All.

### SRS-NFR-007 — Cross-platform architecture, macOS-first delivery

- **Priority:** Must
- **Description:** OS-specific collection/packaging code shall be isolated behind platform adapters, paths handled by platform libraries, and domain/policy/API logic shall contain no macOS-only assumptions.
- **Rationale:** Linux and Windows are planned without delaying macOS MVP.
- **Inputs:** Architecture/code review and platform-contract tests with simulated adapters.
- **Preconditions:** A platform adapter implements the common collector or packaging contract.
- **Normal flow:** Collect or package through the platform adapter, normalize to common contracts, and keep OS specifics outside domain logic.
- **Outputs:** macOS implementation satisfies the common collector contract; unsupported platforms fail with a clear capability result.
- **Error flow:** Platform-specific behavior remains in its adapter and cannot silently change normalized semantics.
- **Security constraints:** No lowest-common-denominator privilege escalation or unsafe shell portability shortcut.
- **Acceptance:** Platform-boundary tests and architecture review pass.
- **Backlog:** `US-020`, `US-022`.
- **Related tests:** `VT-SRS-NFR-007`.
- **Components:** `CMP-COL`, `CMP-OPS`, `CMP-DOM`.

### SRS-NFR-008 — Safe local observability and telemetry policy

- **Priority:** Must
- **Description:** Provide structured local logs, levels, correlation IDs, local metrics, and redacted diagnostic bundle; no external telemetry by default.
- **Rationale:** Local failures require diagnosis without turning machine data into a remote analytics feed.
- **Inputs:** Successful/failed requests, background work, collector/provider health, redaction events, diagnostic export.
- **Preconditions:** Local audit/log/metrics configuration and a correlation context are available.
- **Normal flow:** Create a correlation ID, classify and redact the event, record local logs/metrics/audit, and build diagnostics only on request.
- **Outputs:** A user can correlate a safe error to component activity and produce a redacted bundle.
- **Error flow:** Logging/metrics failure is visible and does not log raw rejected content as fallback.
- **Security constraints:** Anonymous telemetry requires separate privacy review and explicit opt-in; raw prompts and secrets are excluded.
- **Acceptance:** Correlation/diagnostic/redaction tests pass; outbound-network audit shows no default telemetry.
- **Backlog:** `US-053`.
- **Related tests:** `VT-SRS-NFR-008`.
- **Components:** `CMP-AUD`, `CMP-SEC`.

## Optional AI quality

### SRS-AI-004 — AI independence, validation, and bounded resources

- **Priority:** Must if AI ships; core independence is always Must
- **Description:** Ollama/model absence, invalid output, timeout, cancellation, overload, or restart shall not degrade core; accepted machine-readable output shall pass strict validation; AI calls shall use bounded context/output/time/concurrency and visible resource controls.
- **Rationale:** AI is optional and probabilistic, while core port state is safety-critical.
- **Inputs:** Provider absent/stopped, model missing, OOM, malformed/schema-invalid/adversarial output, slow response, cancellation, prompt injection, oversized context.
- **Preconditions:** Optional AI is explicitly enabled for a permitted capability, or a provider-failure profile is under test.
- **Normal flow:** Apply context/output/time/concurrency bounds, invoke the isolated provider, strictly validate the result, and preserve deterministic core authority.
- **Outputs:** Core state and capability remain unchanged; unsafe output is rejected; generated output is labeled and evidence-linked.
- **Error flow:** Typed safe error, bounded backoff, no permissive repair or indefinite retry.
- **Security constraints:** Read-only fixed tools, no arbitrary files/shell/network/process control, no secrets, no automatic download, no authority promotion.
- **Acceptance:** `SM-13`, `SM-14`; `AC-010`–`AC-015`.
- **Backlog:** `US-083`.
- **Related tests:** `VT-SRS-AI-004`, `UAT-010`–`UAT-015`.
- **Components:** `CMP-AI`, `CMP-SEC`, `CMP-DOM`.

## Delivery quality

### SRS-OPS-004 — Five-minute install and safe lifecycle

- **Priority:** Must
- **Description:** A first-time supported macOS user shall install and reach the dashboard in under five minutes; install, start/stop/restart/status/logs, upgrade, rollback, backup/restore, uninstall, and data/config locations shall be documented and tested.
- **Rationale:** Repository cloning or fragile service setup would prevent normal adoption.
- **Inputs:** Clean supported machine plus supported upgrade/rollback profiles and release artifact.
- **Preconditions:** A supported macOS profile and integrity-verifiable release artifact are available.
- **Normal flow:** Install, initialize, start and verify; exercise backup/upgrade/migration/rollback/restore; then uninstall with an explicit data choice.
- **Outputs:** `SM-01` and `SM-11` pass with deliberate data-retention/removal choices.
- **Error flow:** Failed install/migration preserves recoverable state and explains rollback/diagnostics.
- **Security constraints:** Least privilege, integrity verification/signing where practical, no automatic elevation.
- **Acceptance:** Clean-machine lifecycle matrix and founder UAT.
- **Backlog:** `US-100`, `US-101`.
- **Related tests:** `VT-SRS-OPS-004`.
- **Components:** `CMP-OPS`, `CMP-CFG`, `CMP-DB`.

### SRS-NFR-009 — Open-source release quality

- **Priority:** Must
- **Description:** The project shall include coherent README/quick start, architecture/development/contribution/security/governance/support/release docs, issue/PR templates, changelog/semantic versioning, locked reviewed dependencies, CI, security/license checks, and SBOM where practical.
- **Rationale:** Contributor and release infrastructure is part of the product.
- **Inputs:** Release candidate, repository policy, dependency inventory, documentation/link checks.
- **Preconditions:** A release candidate and complete dependency/documentation inventory are available.
- **Normal flow:** Run required CI, documentation, secret, dependency, license, security, artifact, and release checks before approval.
- **Outputs:** Fast required checks and separated extended tests pass; no committed secret; name/license/release decisions approved.
- **Error flow:** Failed required CI, security/license review, documentation command/link, or release checklist blocks publication.
- **Security constraints:** Bug/diagnostic templates warn about redaction; security disclosure process is available.
- **Acceptance:** Gate 9 release checklist and UAT pass.
- **Backlog:** `US-010`, `US-102`, `US-103`.
- **Related tests:** `VT-SRS-NFR-009`.
- **Components:** `CMP-OPS`, `CMP-AUD`, all engineering components.

### SRS-SCN-005 — Supported parser detection quality

- **Priority:** Must
- **Description:** Initial scanning shall identify at least 90% of exact declarations in the versioned supported MVP corpus while reporting precision, unsupported/error counts, parser versions, and confidence semantics.
- **Rationale:** A high-volume scanner without measured exact coverage or false-positive visibility is not trustworthy.
- **Inputs:** Reviewed labeled corpus spanning supported priority formats, malformed inputs, secrets, nesting, worktrees, and conflicts.
- **Preconditions:** The reviewed labeled supported-format corpus and parser-version manifest are available.
- **Normal flow:** Run each deterministic parser against labels, calculate exact recall/precision/errors, and publish results with parser versions.
- **Outputs:** `SM-03` threshold passes and every parser has fixtures; framework/catalog defaults remain hints rather than exact observations.
- **Error flow:** A parser below threshold remains unsupported/experimental or is excluded from MVP claims; no broad source literal fallback.
- **Security constraints:** Corpus and results contain no real secrets; parsers never execute project content.
- **Acceptance:** Corpus report shows at least 90% exact recall for supported declarations with quality breakdown.
- **Backlog:** `US-032`, `US-090`.
- **Related tests:** `VT-SRS-SCN-005`, `UAT-002`, `UAT-003`, `UAT-005`.
- **Components:** `CMP-SCN`, `CMP-SEC`.
