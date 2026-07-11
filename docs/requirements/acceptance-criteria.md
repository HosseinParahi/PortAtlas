# PortAtlas Acceptance Criteria

## Acceptance policy

The fifteen founder scenarios are canonically identified as `AC-001` through `AC-015`. Their executable UAT counterparts are `UAT-001` through `UAT-015` in `docs/testing/uat-plan.md`; this document defines the product outcome while the test plan defines setup and execution procedure.

`AC-001` through `AC-009` are unconditional core scenarios. `AC-010` always verifies graceful operation without AI. `AC-011` through `AC-015` become release-blocking when optional local AI ships; otherwise they remain the approved acceptance contract for the first AI-enabled release.

Evidence must identify build, machine/profile, fixture/project, relevant record IDs, timestamps, commands or interaction recording, and pass/fail result. No scenario may pass from a screenshot alone when a contract, state, concurrency, or secret-safety assertion requires machine-readable evidence.

## Initial acceptance scenarios

### AC-001 — Find the owner of a port

**Given** TCP 3000 is actively listening in the supported macOS test environment
**When** the user searches or navigates to TCP 3000
**Then** PortAtlas shows:

- protocol and port;
- process and executable;
- PID plus process start time;
- project and service association with confidence;
- safely redacted command;
- bound address and exposure classification;
- native/Docker status;
- timestamped collector/association evidence; and
- last-seen time.

The owner and source must be reachable in no more than two interactions, and permission-limited data must be labeled rather than invented.

- **Requirements:** `SRS-COL-001`, `SRS-COL-002`, `SRS-UI-002`, `SRS-NFR-001`
- **UAT:** `UAT-001`
- **Gate:** Gate 4 for collector accuracy; Gate 7 for complete UI flow

### AC-002 — Detect a future declared conflict

**Given** inactive `ProjectInstance` A and inactive `ProjectInstance` B, which may belong to the same or different logical `Project` records, both have exact evidence declaring host TCP 8080
**When** scanning/reconciliation completes
**Then** the conflict center shows one normalized declared-declared conflict, links both project/service/file-location evidence records, explains that the conflict will occur if both claim the same host binding, and recommends an explained policy-compliant alternative.

No runtime listener may be invented, and a recommendation must be labeled as unreserved until the user reserves or leases it.

- **Requirements:** `SRS-SCN-003`, `SRS-REG-002`, `SRS-CNF-001`, `SRS-UI-003`, `SRS-SCN-005`
- **UAT:** `UAT-002`
- **Gate:** Gate 5 for detection; Gate 6 for conflict/suggestion; Gate 7 for UI

### AC-003 — Detect Docker and native process conflict

**Given** a native process currently owns host TCP 5432 and a Compose project declares a published host mapping on TCP 5432
**When** the user preflights the Compose project before Docker startup
**Then** PortAtlas reports a Docker-native host-binding conflict, identifies the native process and Compose file/service evidence, distinguishes the container port from the host port, explains startup impact, and offers a safe response.

- **Requirements:** `SRS-COL-003`, `SRS-SCN-003`, `SRS-CNF-001`, `SRS-UI-003`, `SRS-SCN-005`
- **UAT:** `UAT-003`
- **Gate:** Gate 5 for declaration; Gate 6 for conflict; Gate 7 for UI

### AC-004 — Agent chooses and leases a safe port

**Given** an authorized agent needs a new TCP API port for an approved `ProjectInstance`/service
**When** it follows the MCP workflow to resolve the instance, inspect policy/state, preflight, request a suggestion, and acquire a lease
**Then** it receives a policy-compliant explained port and unique atomic lease with owner/expiry/evidence; no source file change, service launch, process termination, Docker lifecycle mutation, or global configuration edit capability is present in the MVP workflow.

- **Requirements:** `SRS-REG-002`, `SRS-ALC-001`, `SRS-MCP-001`, `SRS-MCP-002`, `SRS-SEC-003`, `SRS-NFR-004`
- **UAT:** `UAT-004`
- **Gate:** Gate 6 for lease integrity; Gate 8 for agent workflow

### AC-005 — Scan environment configuration without exposing secrets

**Given** an approved `.env` file contains `PORT=3000` and seeded credential values
**When** the environment parser scans the file and the finding is viewed through UI, API, MCP, logs, audit, export, and diagnostic checks
**Then** PortAtlas records the port-related declaration and safe source evidence while no credential, unrelated value, or complete sensitive line is persisted or exposed.

- **Requirements:** `SRS-SCN-004`, `SRS-OPS-002`, `SRS-SEC-002`, `SRS-SCN-005`
- **UAT:** `UAT-005`
- **Gate:** Gate 5 for parser; security verification at every later gate

### AC-006 — Configure project roots through the UI

**Given** a fresh installation and an accessible `~/GitHub/personal` fixture/root
**When** the user selects it through the UI, sets scan policy, previews included/excluded logical Projects and concrete checkout/worktree `ProjectInstance` records, approves, and starts scanning
**Then** scanning remains inside the canonical approved root, requires no application source edit, reports progress/errors, and persists a valid versioned root configuration.

- **Requirements:** `SRS-SCN-001`, `SRS-UI-001`, `SRS-OPS-003`, `SRS-SEC-003`, `SRS-OPS-004`
- **UAT:** `UAT-006`
- **Gate:** Gate 5 for root behavior; Gate 7 for complete setup flow

### AC-007 — Warn about public database exposure

**Given** a local database listener is observed on `0.0.0.0` or `::` and policy prefers loopback
**When** reconciliation evaluates the observation
**Then** overview and conflict detail flag an exposure risk with process/container, address, project/service, policy and evidence, and offer reviewable manual guidance without changing firewall, binding, or process state.

- **Requirements:** `SRS-COL-002`, `SRS-REG-001`, `SRS-CNF-001`, `SRS-UI-003`, `SRS-SEC-003`
- **UAT:** `UAT-007`
- **Gate:** Gate 6 for classification; Gate 7 for UX

### AC-008 — Allocate race-safe concurrent leases

**Given** two authorized clients concurrently request a TCP port from the same eligible range
**When** both allocation transactions execute
**Then** each receives a different active lease, uniqueness and owner/expiry constraints hold, audit records correlate both outcomes, and no partial/duplicate lease remains after retry or rollback.

- **Requirements:** `SRS-ALC-001`, `SRS-MCP-001`, `SRS-NFR-004`
- **UAT:** `UAT-008`
- **Gate:** Gate 6

### AC-009 — Explain unmanaged-process limitation

**Given** PortAtlas suggests a currently free port but no reservation/lease is acquired, and an external unmanaged process binds it before the intended service starts
**When** reconciliation observes the new listener
**Then** PortAtlas reports the resulting conflict, identifies current evidence, states that a point-in-time suggestion did not reserve the port, and does not claim prevention was guaranteed.

- **Requirements:** `SRS-ALC-001`, `SRS-CNF-001`, `SRS-MCP-002`, `SRS-NFR-004`
- **UAT:** `UAT-009`
- **Gate:** Gate 6 for detection/explanation; Gate 8 for agent wording

### AC-010 — Preserve core operation when local AI is unavailable

**Given** Ollama is disabled, absent, stopped, unreachable, loading, missing a model, overloaded, or returning a provider error
**When** the user performs core inventory, scan, conflict, suggestion/reservation, project, API, CLI, or MCP work
**Then** all core capabilities remain operational; only AI capability shows a visible bounded degradation with safe retry/disable guidance and no indefinite background retry.

- **Requirements:** `SRS-AI-001`, `SRS-AI-003`, `SRS-SEC-001`, `SRS-NFR-003`, `SRS-AI-004`
- **UAT:** `UAT-010`
- **Gate:** Gate 8 and Gate 9

### AC-011 — Generate a grounded conflict explanation

**Given** the deterministic conflict engine has an evidence-backed conflict
**When** the user asks the enabled local model to explain it
**Then** the validated result identifies the correct process, project, port, reason, security/exposure implication where applicable, safe alternatives, automation-safety state, and evidence IDs; it is labeled generated/non-authoritative and makes no authoritative state change.

- **Requirements:** `SRS-AI-002`, `SRS-AI-003`, `SRS-AI-004`
- **UAT:** `UAT-011`
- **Gate:** Gate 8 if AI ships

### AC-012 — Reject invalid structured model output

**Given** the local model returns malformed JSON, schema-invalid fields, invalid port/protocol/path, unknown evidence IDs, or an unsupported tool/action
**When** PortAtlas validates the result
**Then** it rejects the result with a typed safe error, does not permissively repair safety-sensitive output, records redacted outcome metadata, and leaves authoritative state unchanged.

- **Requirements:** `SRS-AI-003`, `SRS-AI-004`
- **UAT:** `UAT-012`
- **Gate:** Gate 8 if AI ships

### AC-013 — Resist repository prompt injection

**Given** approved repository content instructs a model to ignore policy, reveal data, execute a command, expand paths, or request a mutating tool
**When** that content is included as minimal untrusted data in an AI-assisted workflow
**Then** PortAtlas preserves system policy and fixed read-only tools, rejects unauthorized arguments/actions, exposes no arbitrary shell/file/network/process capability, and makes no permission or state change.

- **Requirements:** `SRS-MCP-002`, `SRS-AI-003`, `SRS-SEC-003`, `SRS-AI-004`
- **UAT:** `UAT-013`
- **Gate:** Gate 8 if AI ships

### AC-014 — Generate a secret-safe project summary

**Given** an approved project contains secret-bearing environment/configuration and process metadata
**When** the user requests an enabled local-model project summary
**Then** the context builder provides only minimum redacted port-related evidence, the generated summary contains no seeded secret/unrelated environment value, and the user can inspect the context categories/evidence and delete the derived result.

- **Requirements:** `SRS-SCN-004`, `SRS-AI-002`, `SRS-AI-003`, `SRS-SEC-002`, `SRS-AI-004`
- **UAT:** `UAT-014`
- **Gate:** Gate 8 if AI ships

### AC-015 — Keep AI-assisted extraction unconfirmed

**Given** a small unsupported custom launcher is inside an approved root and deterministic parsers cannot confirm its port
**When** an enabled local model returns a schema-valid, evidence-linked declaration candidate
**Then** PortAtlas stores/displays it as `AI suggested` and `Unconfirmed` with provider/model/schema/confidence/evidence/validation metadata; it does not become an exact declaration, reservation, conflict truth, or file change until deterministic evidence or explicit user confirmation promotes it.

- **Requirements:** `SRS-AI-003`, `SRS-AI-004`
- **UAT:** `UAT-015`
- **Gate:** Gate 8 if AI-assisted extraction is included

## Functional verification catalog

| ID | Requirement | Required verification evidence |
| --- | --- | --- |
| VT-SRS-COL-001 | SRS-COL-001 | Unit normalization plus real/controlled TCP/UDP IPv4/IPv6 collector integration |
| VT-SRS-COL-002 | SRS-COL-002 | PID-start identity, redaction, permission, bind/exposure and association fixtures |
| VT-SRS-COL-003 | SRS-COL-003 | Fake/real Docker profiles for container state, Compose labels, internal/published/interface mapping and failure |
| VT-SRS-COL-004 | SRS-COL-004 | Watcher/event/poll debounce, cancellation, last-good, restart and event-latency integration |
| VT-SRS-SCN-001 | SRS-SCN-001 | Root preview/add/remove/pause/depth/include/exclude/symlink/path-security E2E |
| VT-SRS-SCN-002 | SRS-SCN-002 | Git, rename, monorepo, nested service, non-Git and worktree identity fixtures |
| VT-SRS-SCN-003 | SRS-SCN-003 | Fixture test per supported parser plus malformed/unsupported/large input behavior |
| VT-SRS-SCN-004 | SRS-SCN-004 | Evidence/confidence classification and canary-secret redaction across interfaces |
| VT-SRS-REG-001 | SRS-REG-001 | Policy schema, precedence, range/interface/protocol/reuse/timeout and migration tests |
| VT-SRS-REG-002 | SRS-REG-002 | Deterministic suggestion, explanation, reservation idempotency/recheck/release tests |
| VT-SRS-ALC-001 | SRS-ALC-001 | Property/concurrency tests for uniqueness, expiry, renewal, conversion, rollback and external collision |
| VT-SRS-CNF-001 | SRS-CNF-001 | Rule/fixture coverage for every conflict type, severity, evidence, suppression and symmetry |
| VT-SRS-UI-001 | SRS-UI-001 | Clean-profile setup E2E including optional capability failure and cancellation |
| VT-SRS-UI-002 | SRS-UI-002 | Overview/table/search/filter/pagination/events/degraded/accessibility/interaction-count E2E |
| VT-SRS-UI-003 | SRS-UI-003 | Project/conflict detail evidence, safe actions, stale/not-found and context-preservation E2E |
| VT-SRS-UI-004 | SRS-UI-004 | Search ranking, config round-trip/schema rejection and demo-isolation E2E |
| VT-SRS-API-001 | SRS-API-001 | OpenAPI/client drift, validation, pagination, errors, auth/origin/idempotency/dry-run/events contracts |
| VT-SRS-CLI-001 | SRS-CLI-001 | Every MVP command in human/JSON/piped modes with exit/error contract tests |
| VT-SRS-MCP-001 | SRS-MCP-001 | STDIO/HTTP/auth/token/schema/consent/cancellation and tool/resource/prompt contract tests |
| VT-SRS-MCP-002 | SRS-MCP-002 | Agent workflow plus copy-ready client setup/test/rollback/uninstall guidance and proof that unauthorized client/source/process/Docker writes are absent |
| VT-SRS-AI-001 | SRS-AI-001 | Provider health/version/model/capability/config/resource/cancellation and no-auto-download tests |
| VT-SRS-AI-002 | SRS-AI-002 | Grounded query/explanation/summary evaluation with evidence and generated labels |
| VT-SRS-AI-003 | SRS-AI-003 | Context minimization, redaction, injection, schema/semantic/evidence, retention/purge and state-isolation tests |
| VT-SRS-OPS-001 | SRS-OPS-001 | Clean install and full lifecycle matrix with recovery/data-location verification |
| VT-SRS-OPS-002 | SRS-OPS-002 | Audit correlation, integrity, safe logging/local metrics and redacted diagnostics tests |
| VT-SRS-OPS-003 | SRS-OPS-003 | Config validation/version/migration/backup/restore/reset/import/export/read-only-mode tests |

## Non-functional verification catalog

| ID | Requirement | Required verification evidence |
| --- | --- | --- |
| VT-SRS-SEC-001 | SRS-SEC-001 | External-network-disabled core E2E with Docker/Ollama absent |
| VT-SRS-SEC-002 | SRS-SEC-002 | Canary-secret scan across persistence, UI, API, MCP, logs, audit, export, diagnostics, AI and tests |
| VT-SRS-SEC-003 | SRS-SEC-003 | Threat-model security suite for path/symlink/command/origin/token/Docker/MCP/model/resource attacks |
| VT-SRS-NFR-001 | SRS-NFR-001 | Update-latency benchmark, event-loop responsiveness, cancellation, bounds, debounce and pagination |
| VT-SRS-NFR-002 | SRS-NFR-002 | Reference 500/2,000/1,000 dataset benchmark and founder responsiveness UAT |
| VT-SRS-NFR-003 | SRS-NFR-003 | Fault injection, restart reconciliation, corrupt config/migration recovery and shutdown tests |
| VT-SRS-NFR-004 | SRS-NFR-004 | Concurrent/idempotent reservation/lease transaction and rollback property suite |
| VT-SRS-NFR-005 | SRS-NFR-005 | Automated accessibility scan plus keyboard, screen-reader, contrast, motion and responsive manual review |
| VT-SRS-NFR-006 | SRS-NFR-006 | Format/lint/type/unit/contract/architecture/dependency/documentation review evidence |
| VT-SRS-NFR-007 | SRS-NFR-007 | Platform-adapter contract and OS-isolation architecture tests |
| VT-SRS-NFR-008 | SRS-NFR-008 | Correlation/diagnostic/redaction/local-metrics checks plus outbound-network audit |
| VT-SRS-AI-004 | SRS-AI-004 | AI absence/error/adversarial/timeout/cancellation/resource/validation/core-isolation evaluation |
| VT-SRS-OPS-004 | SRS-OPS-004 | Timed clean install and lifecycle/rollback/backup/uninstall matrix |
| VT-SRS-NFR-009 | SRS-NFR-009 | Required CI, docs links/commands, secret/dependency/license/security/SBOM and release checklist |
| VT-SRS-SCN-005 | SRS-SCN-005 | Versioned supported corpus report with exact recall, precision, errors, confidence and parser versions |

## Release acceptance summary

- Gate 7 requires the core human workflows and applicable `AC-001` through `AC-009` evidence.
- Gate 8 requires `AC-004`, `AC-008`, `AC-009`, and `AC-010`; when AI ships it also requires `AC-011` through `AC-015`.
- Gate 9 requires all applicable scenarios, all Must verification records, lifecycle/security/accessibility/performance evidence, and founder UAT approval.
