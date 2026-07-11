# PortAtlas Functional Requirements

## Conventions

- **Priority** uses MoSCoW relative to the MVP.
- **Acceptance** is normative and may reference founder scenarios in [Acceptance criteria](acceptance-criteria.md).
- **Verification** IDs are defined in the verification catalog in that document.
- **Component** IDs are defined in the [SRS](srs.md#7-architecture-component-identifiers).
- These requirements define intended behavior; they do not assert implementation completion.

## Runtime inventory

### SRS-COL-001 — Host listener inventory

- **Priority:** Must
- **Description:** Collect and normalize currently listening TCP and UDP sockets on macOS, including IPv4/IPv6, address, port, state, collection time, and collector source; define equivalent future Linux/Windows contracts.
- **Rationale:** Runtime truth is the authoritative basis for current ownership and collision analysis.
- **Inputs:** OS socket/process APIs and safe argument-array subprocess results.
- **Outputs:** Timestamped `PortObservation` records and collector capability metadata.
- **Preconditions:** Native service is running; only platform permissions already granted are used.
- **Normal flow:** Collect → validate → normalize protocol/address/state → reconcile with prior snapshot → publish changes.
- **Error flow:** A command timeout, malformed/unsupported output, or permission failure becomes a scoped degraded result; last-known-good state remains timestamped.
- **Security constraints:** No shell-interpolated untrusted value, automatic elevation, or unbounded command output.
- **Acceptance:** TCP/UDP and IPv4/IPv6 test listeners appear with correct address/protocol/port; `AC-001` can begin from the observation.
- **Backlog:** `US-020`.
- **Related tests:** `VT-SRS-COL-001`, `UAT-001`.
- **Component:** `CMP-COL`, `CMP-DOM`.

### SRS-COL-002 — Process identity, interface semantics, and exposure

- **Priority:** Must
- **Description:** Associate observations where permitted with PID plus start time, executable, redacted command, user, working directory, parent, project/service, and distinguish loopback, wildcard, LAN, protocol, and host/container semantics.
- **Rationale:** PID alone is reused, and interface semantics determine ownership, collision, and exposure risk.
- **Inputs:** Normalized observation plus process metadata and project evidence.
- **Outputs:** `ProcessIdentity`, safe association evidence, permission limits, and exposure facts.
- **Preconditions:** `SRS-COL-001` produced an observation.
- **Normal flow:** Resolve PID/start/executable → redact arguments → classify address → associate evidence → expose uncertainty.
- **Error flow:** Missing metadata yields Unknown or permission-limited fields, never invented ownership.
- **Security constraints:** Redact sensitive arguments; do not persist secrets or imply elevated visibility.
- **Acceptance:** `AC-001` shows the required owner fields; `AC-007` flags a database on `0.0.0.0`; IPv4/IPv6 wildcard fixtures classify correctly.
- **Backlog:** `US-021`.
- **Related tests:** `VT-SRS-COL-002`, `UAT-001`, `UAT-007`.
- **Component:** `CMP-COL`, `CMP-DOM`, `CMP-SEC`.

### SRS-COL-003 — Docker and Compose inventory

- **Priority:** Must
- **Description:** When Docker is available, collect running/stopped containers, published host bindings, internal/exposed ports, interfaces, networks, Compose project/service labels, health, image/tag, start time, restart policy, and project association.
- **Rationale:** Docker host bindings collide with native listeners while internal ports do not necessarily consume a host port.
- **Inputs:** Docker Engine API or approved maintained client events/snapshots.
- **Outputs:** `ContainerIdentity`, Docker observations, bindings, capability/error state.
- **Preconditions:** Docker integration is enabled and the local endpoint is reachable; core does not require it.
- **Normal flow:** Connect → enumerate/subscribe → normalize container versus host bindings → associate Compose/project → reconcile.
- **Error flow:** Missing Docker, stopped Desktop, permission denial, or event loss marks Docker degraded and falls back to safe reconciliation without crashing core.
- **Security constraints:** Treat socket access as privileged; never expose an unauthenticated remote Docker-control surface.
- **Acceptance:** `AC-003` distinguishes native 5432 from a Compose host publication; an internal-only port is not reported as a host collision.
- **Backlog:** `US-022`.
- **Related tests:** `VT-SRS-COL-003`, `UAT-003`.
- **Component:** `CMP-DKR`, `CMP-DOM`.

### SRS-COL-004 — Refresh, reconciliation, and degraded state

- **Priority:** Must
- **Description:** Combine periodic reconciliation, Docker events where available, filesystem watcher events, manual refresh, debounce, caching, and last-known-good snapshots; publish changes through the event layer.
- **Rationale:** Runtime/project state changes continuously and individual collectors can fail independently.
- **Inputs:** Collector snapshots/events, watcher events, manual commands, configuration and cache versions.
- **Outputs:** Reconciled current state, staleness, progress, update events, and named degraded status.
- **Preconditions:** Native service and persistence are available.
- **Normal flow:** Receive event/interval → debounce → collect/scan affected scope → transactionally reconcile → emit update.
- **Error flow:** Preserve timestamped prior evidence, back off bounded retries, show affected/unaffected capabilities, and support manual recovery.
- **Security constraints:** Bound concurrency, time, output, queue growth, and scan scope.
- **Acceptance:** Runtime changes reach the UI within `SM-04`; collector failure does not crash API or erase prior evidence.
- **Backlog:** `US-023`.
- **Related tests:** `VT-SRS-COL-004`.
- **Component:** `CMP-DOM`, `CMP-DB`, `CMP-API`, `CMP-AUD`.

## Project discovery and evidence

### SRS-SCN-001 — Approved project-root management

- **Priority:** Must
- **Description:** Let the user add, remove, pause, tag, preview, approve, rescan, and configure depth/include/exclude/symlink policy for one or more project roots through UI and configuration interfaces.
- **Rationale:** Users need configuration without source edits and PortAtlas must not scan arbitrary paths.
- **Inputs:** User-selected path and scan-policy settings.
- **Outputs:** Versioned `ProjectRoot`, preview inventory, progress, exclusions, and permission errors.
- **Preconditions:** User has local filesystem access to the selected path.
- **Normal flow:** Choose path → canonicalize/validate → preview candidates/exclusions → explicit approval → persist → scan.
- **Error flow:** Reject nonexistent/out-of-scope/symlink-escaped paths; report partial permission errors; allow cancellation and pause.
- **Security constraints:** Never scan beyond approved canonical roots; default-exclude VCS internals, dependencies, virtual environments, builds, caches, binaries, hidden system, and configured sensitive paths.
- **Acceptance:** `AC-006` selects `~/GitHub/personal`, previews projects, and starts scanning without a source edit.
- **Backlog:** `US-030`.
- **Related tests:** `VT-SRS-SCN-001`, `UAT-006`.
- **Component:** `CMP-SCN`, `CMP-CFG`, `CMP-SEC`, `CMP-WEB`.

### SRS-SCN-002 — Project, ProjectInstance, service, repository, and worktree identity

- **Priority:** Must
- **Description:** Model one stable logical `Project` with one or more concrete checkout, worktree, or standalone-directory `ProjectInstance` records; detect monorepo/workspace services beneath the relevant instance and never use absolute path as the only identity.
- **Rationale:** Renames, multiple checkouts, and nested services require durable associations.
- **Inputs:** Approved-root filesystem/Git metadata and manual registration.
- **Outputs:** `Project`, `ProjectInstance`, and `Service` identities with aliases, canonical paths, evidence, and worktree relationship.
- **Preconditions:** Root is approved under `SRS-SCN-001`.
- **Normal flow:** Inspect recognized identity markers → resolve logical Project → create or reconcile concrete ProjectInstance → normalize workspace/service relationships → preserve stable identity/aliases.
- **Error flow:** Ambiguous nesting or worktree identity is surfaced as Unknown/decision-required, not silently merged.
- **Security constraints:** No mandatory GitHub API/network call and no path traversal outside roots.
- **Acceptance:** Fixture corpus proves one logical Project can own multiple distinct worktree ProjectInstances; scans, runtime associations, policy, reservations, and leases remain instance-scoped; rename preserves identity where evidence permits.
- **Backlog:** `US-031`.
- **Related tests:** `VT-SRS-SCN-002`.
- **Component:** `CMP-SCN`, `CMP-DOM`.

### SRS-SCN-003 — Deterministic static declaration scanners

- **Priority:** Must
- **Description:** Use isolated parsers with fixtures for exactly the locked MVP catalog: Compose; Dockerfile `EXPOSE`; safe `.env*` port keys; `package.json` scripts/workspaces; Vite, Next, Nuxt, and SvelteKit; recognized Python launcher commands and `pyproject.toml`; Tauri configuration; Makefile, Taskfile, Procfile, and justfile. Development proxies, devcontainers, VS Code launch/tasks, and other adapters are deferred.
- **Rationale:** Future conflicts require configuration evidence even when projects are inactive.
- **Inputs:** Targeted files under approved project roots plus data-driven service catalog hints.
- **Outputs:** `PortDeclaration` candidates with host/container distinction, service, protocol, value, source location, parser, timestamp, and confidence.
- **Preconditions:** Project/service identity exists and file meets size/type/scope rules.
- **Normal flow:** Route recognized file → parse typed syntax/pattern → validate port/protocol/semantics → emit evidence.
- **Error flow:** Malformed/unsupported files produce bounded parser errors and no broad numeric fallback by default.
- **Security constraints:** Do not execute project files, interpolate shell, or treat framework defaults/catalog hints as runtime observations.
- **Acceptance:** Supported corpus meets `SM-03`; `AC-002` identifies two inactive declarations and `AC-003` reads Compose host mapping.
- **Backlog:** `US-032`, `US-034`.
- **Related tests:** `VT-SRS-SCN-003`, `UAT-002`, `UAT-003`.
- **Component:** `CMP-SCN`, `CMP-SEC`.

### SRS-SCN-004 — Evidence, confidence, and environment safety

- **Priority:** Must
- **Description:** Attach provenance and Exact/High/Medium/Low/User-confirmed confidence to every declaration/association; environment parsing extracts only port-relevant data and never persists or exposes unrelated/secret values.
- **Rationale:** Static discovery has varying certainty and environment files commonly contain credentials.
- **Inputs:** Parser result, file/location metadata, redaction policy, user confirmation.
- **Outputs:** Safe `DiscoveryEvidence`, confidence, validation state, and redaction events.
- **Preconditions:** Parser has an approved minimal input.
- **Normal flow:** Classify evidence → secret-detect/redact → retain safe port fields/source references → expose confidence.
- **Error flow:** Possible secret or unsafe source location suppresses the value/snippet; user can disable environment scanning.
- **Security constraints:** Never log full lines, return full environment contents over any interface, persist secrets, or send environment content to MCP/model.
- **Acceptance:** `AC-005` discovers `PORT=3000` with no credential exposure; `AC-014` provides only redacted model context.
- **Backlog:** `US-033`.
- **Related tests:** `VT-SRS-SCN-004`, `UAT-005`, `UAT-014`.
- **Component:** `CMP-SCN`, `CMP-SEC`, `CMP-AUD`.

## Registry, allocation, and conflicts

### SRS-REG-001 — Configurable port policy

- **Priority:** Must
- **Description:** Support UI/CLI/import configuration for global, project, service-category and worktree rules covering allowed/preferred/forbidden/system/ephemeral ranges, interface, protocol, stability, severity, suggestion, timeout, and reuse.
- **Rationale:** Safe allocation is contextual and cannot rely on hard-coded defaults.
- **Inputs:** Versioned policy configuration and project/service context.
- **Outputs:** Validated `PortPolicy`, precedence/explanation, and policy findings.
- **Preconditions:** Actor is authorized to modify local configuration.
- **Normal flow:** Validate schema/ranges/precedence → preview change → persist version → re-evaluate affected records.
- **Error flow:** Reject overlapping/invalid/unsafe policy with stable errors; retain last-known-good policy.
- **Security constraints:** Mutation requires local authentication where applicable and audit; no silent global changes.
- **Acceptance:** Suggestion and exposure scenarios respect configured range/interface policy.
- **Backlog:** `US-040`.
- **Related tests:** `VT-SRS-REG-001`, `UAT-007`, `UAT-008`.
- **Component:** `CMP-REG`, `CMP-CFG`.

### SRS-REG-002 — Safe suggestion and persistent reservation

- **Priority:** Must
- **Description:** Explain a deterministic suggestion that preserves valid existing assignment and avoids observations, reservations, leases, forbidden/system/ephemeral ports; allow scoped reservation and release.
- **Rationale:** Recommendations must be stable, policy-aware, and convertible into explicit ownership.
- **Inputs:** ProjectInstance/service/protocol request, policy, reconciled inventory, reservations and leases.
- **Outputs:** Explained suggestion or stable failure; persistent `PortReservation` on authorized confirmation.
- **Preconditions:** Current registry/policy state is available; reservation request has an owner/scope.
- **Normal flow:** Resolve context → order candidates deterministically → exclude conflicts → explain candidate → transactionally reserve if requested.
- **Error flow:** Recheck failure/concurrent claim returns conflict and alternative without partial state.
- **Security constraints:** Suggestion is labeled point-in-time; reservation mutation is authenticated, idempotent where appropriate, and audited.
- **Acceptance:** `AC-002` recommends a safe alternative and `AC-004` provides an explained suggestion before lease.
- **Backlog:** `US-041`.
- **Related tests:** `VT-SRS-REG-002`, `UAT-002`, `UAT-004`.
- **Component:** `CMP-REG`, `CMP-DB`, `CMP-AUD`.

### SRS-ALC-001 — Atomic port leases

- **Priority:** Must
- **Description:** Acquire, renew where authorized, expire, convert between allowed reservation/lease states, and release short-lived port leases through a database transaction or equivalent lock. The MVP lease coordinates cooperating PortAtlas clients and does not reserve an operating-system socket or launch a service.
- **Rationale:** Availability checks alone race; cooperating clients need atomic registry coordination while unmanaged processes remain outside the guarantee.
- **Inputs:** Scoped allocation request, policy/state, lease owner, requested TTL and idempotency key.
- **Outputs:** Unique `PortLease`, expiry/status, or typed collision/expiry result.
- **Preconditions:** Persistence transaction capability is healthy and client is authorized.
- **Normal flow:** Begin transaction/lock → re-evaluate candidate → insert unique active lease → commit → expose expiry → reconcile/convert/release.
- **Error flow:** Collision retries deterministic next candidate; rollback leaves no partial lease; abandoned lease expires.
- **Security constraints:** Explicit scope, bounded TTL, audit, owner checks, and no model-direct lease authority.
- **Acceptance:** `AC-008` gives concurrent clients different leases; `AC-004` agent acquires a lease; `AC-009` explains unmanaged limitation.
- **Backlog:** `US-042`.
- **Related tests:** `VT-SRS-ALC-001`, `UAT-004`, `UAT-008`, `UAT-009`.
- **Component:** `CMP-REG`, `CMP-DB`.

### SRS-CNF-001 — Deterministic conflict and exposure engine

- **Priority:** Must
- **Description:** Normalize active/declaration/reservation/lease, declared-declared, Docker/native, protocol/interface/wildcard/IPv4/IPv6, forbidden/ephemeral, exposure, stale, unknown-owner, permission-limited, and host/container-semantic findings.
- **Rationale:** Users need current and future conflicts explained consistently rather than inferred by UI or model code.
- **Inputs:** Reconciled observations, declarations, policies, reservations, leases, evidence and timestamps.
- **Outputs:** `Conflict` with severity, machine code, affected records, evidence, explanation, actions, automation-safety, dry-run where supported, audit, and suppression state.
- **Preconditions:** Relevant input records exist; incomplete evidence remains explicit.
- **Normal flow:** Evaluate deterministic rules → de-duplicate/normalize → assign severity/code → link evidence/actions → publish change.
- **Error flow:** Insufficient evidence produces Unknown/permission-limited finding; ignored conflict requires reason and optional expiry.
- **Security constraints:** Never execute resolution automatically, terminate processes, or accept model output as conflict truth.
- **Acceptance:** `AC-002`, `AC-003`, `AC-007`, and `AC-009` produce their specified finding/explanation.
- **Backlog:** `US-043`, `US-044`.
- **Related tests:** `VT-SRS-CNF-001`, `UAT-002`, `UAT-003`, `UAT-007`, `UAT-009`.
- **Component:** `CMP-CNF`, `CMP-DOM`, `CMP-AUD`.

## Human experience

### SRS-UI-001 — First-run setup wizard

- **Priority:** Must
- **Description:** Guide privacy, host capability/permission, Docker, project roots/preview, port policy, scan cadence, client integration, security review, and completion without source editing.
- **Rationale:** Installation must produce value quickly with informed consent and safe scope.
- **Inputs:** Local capability checks and user selections.
- **Outputs:** Validated configuration, approved roots, integration choice, and dashboard transition.
- **Preconditions:** Local service/UI are reachable on loopback.
- **Normal flow:** Present steps in order → validate/preview each decision → persist atomically → open overview.
- **Error flow:** User can go back/cancel; failed optional capability does not block completion; invalid config identifies recovery.
- **Security constraints:** No automatic elevation, Docker/model install, global client edit, or scan before approval.
- **Acceptance:** `AC-006`, `SM-01`, and `SM-02` pass on clean supported macOS.
- **Backlog:** `US-060`.
- **Related tests:** `VT-SRS-UI-001`, `UAT-006`.
- **Component:** `CMP-WEB`, `CMP-CFG`, `CMP-SEC`.

### SRS-UI-002 — Overview and ports inventory

- **Priority:** Must
- **Description:** Provide overview status/counts/conflicts/exposures/changes/actions and a paginated high-density port view with search, filter, sort, group, columns, detail, and state/evidence navigation.
- **Rationale:** Daily utility depends on fast machine-wide understanding.
- **Inputs:** API projections and event updates.
- **Outputs:** Accessible rendered state and user query/filter state.
- **Preconditions:** UI can reach local API; demo data is explicitly isolated when enabled.
- **Normal flow:** Load current projection → render freshness/degradation → apply query controls → open record/evidence without losing context.
- **Error flow:** API/event interruption shows last-known-good time and retry; large lists stay paginated.
- **Security constraints:** No secret-bearing command/environment content or unsafe path in UI/URL.
- **Acceptance:** `AC-001` is completed within `SM-05`; update and scale targets `SM-04`/`SM-10` hold.
- **Backlog:** `US-061`.
- **Related tests:** `VT-SRS-UI-002`, `UAT-001`.
- **Component:** `CMP-WEB`, `CMP-API`.

### SRS-UI-003 — Project and conflict detail

- **Priority:** Must
- **Description:** Show logical Project and concrete ProjectInstance identity, Git/worktree/stack/services/paths/ports/policy/evidence/activity and conflict severity/cause/impact/evidence/alternative/manual/suppression/audit controls. A proposed manifest is not shown as a working MVP capability.
- **Rationale:** Ownership and conflict resolution require context beyond an inventory row.
- **Inputs:** Project, service, state, conflict, evidence and audit projections.
- **Outputs:** Navigable detail and explicitly scoped actions.
- **Preconditions:** Selected ID exists and actor may view its approved-root metadata.
- **Normal flow:** Load detail → group authoritative/advisory state → show evidence/uncertainty → offer policy-safe actions.
- **Error flow:** Deleted/stale IDs return a safe not-found/stale view and refresh path.
- **Security constraints:** Mutating controls require preview/confirmation; paths and environment evidence remain redacted where needed.
- **Acceptance:** `AC-002`, `AC-003`, and `AC-007` show cause, evidence, impact, and safe response.
- **Backlog:** `US-062`, `US-063`.
- **Related tests:** `VT-SRS-UI-003`, `UAT-002`, `UAT-003`, `UAT-007`.
- **Component:** `CMP-WEB`, `CMP-CNF`, `CMP-API`.

### SRS-UI-004 — Search, configuration portability, and demo mode

- **Priority:** Must
- **Description:** Provide fuzzy keyboard search/command palette; import/export non-secret versioned configuration; and a polished synthetic demo isolated from real state.
- **Rationale:** Large inventories need rapid navigation, configurations need portability, and contributors need safe exploration.
- **Inputs:** Query text; validated import/export selection; explicit demo-mode choice.
- **Outputs:** Ranked typed results; versioned redacted bundle; clearly labeled synthetic projection.
- **Preconditions:** Actor can access relevant local interface.
- **Normal flow:** Search typed indexes; preview/validate import; select export categories; enter/leave isolated demo.
- **Error flow:** Invalid/newer schema is rejected with migration guidance; demo state never writes authoritative machine records.
- **Security constraints:** Export excludes secrets and AI-derived data unless selected; search does not expose unapproved roots.
- **Acceptance:** Search reaches required objects/actions; import round trip is stable; demo E2E proves no unlabeled mixing.
- **Backlog:** `US-052`, `US-064`.
- **Related tests:** `VT-SRS-UI-004`.
- **Component:** `CMP-WEB`, `CMP-CFG`, `CMP-SEC`.

## API, CLI, MCP, and integrations

### SRS-API-001 — Versioned REST API and real-time events

- **Priority:** Must
- **Description:** Expose versioned `/api/v1` resources for system, collectors, roots, projects/services, observations/declarations/reservations/leases, conflicts, policies, scans, integrations, audit, optional AI, and events.
- **Rationale:** UI and external adapters require one stable application contract.
- **Inputs:** Validated HTTP requests, auth/idempotency/concurrency metadata.
- **Outputs:** OpenAPI-defined safe responses, cursor pages, stable error codes, correlation IDs, and event updates.
- **Preconditions:** Native service and relevant component are available.
- **Normal flow:** Authenticate/authorize where needed → validate → call application service → map result/error → audit mutation → emit event.
- **Error flow:** Invalid, unauthorized, stale, conflict, unavailable, timeout, and cancellation cases use stable non-secret errors.
- **Security constraints:** Loopback default, local auth for mutations, origin/CSRF protections, no secret responses, dry-run endpoints.
- **Acceptance:** Contract/drift tests pass; `AC-001`–`AC-015` interfaces receive no unauthorized/secret state changes.
- **Backlog:** `US-050`.
- **Related tests:** `VT-SRS-API-001`.
- **Component:** `CMP-API`, `CMP-DOM`, `CMP-SEC`.

### SRS-CLI-001 — Command-line interface

- **Priority:** Must
- **Description:** Provide MVP commands for status, ports, projects/show, scan, conflicts, check, suggest, reserve, release, preflight, config show/validate, integrations, `mcp serve`, and demo.
- **Rationale:** Terminal and automation users require stable local access without UI dependence.
- **Inputs:** Parsed options/arguments and local configuration/API context.
- **Outputs:** Human-readable or JSON result, stable exit code, clear degradation/permission/conflict diagnostics.
- **Preconditions:** Command is installed; service connection or supported direct adapter mode is available.
- **Normal flow:** Parse without shell interpolation → validate → call shared application/API service → format output.
- **Error flow:** Piped output requires no ANSI; connection/permission/conflict/config errors remain machine-readable.
- **Security constraints:** No arbitrary shell execution, secret output, or behavior drift from API/MCP.
- **Acceptance:** Command contract tests cover every MVP command and JSON schema/exit code.
- **Backlog:** `US-051`.
- **Related tests:** `VT-SRS-CLI-001`.
- **Component:** `CMP-CLI`, `CMP-DOM`.

### SRS-MCP-001 — MCP transports and typed capabilities

- **Priority:** Must
- **Description:** Support STDIO and authenticated Streamable HTTP bound to loopback, using MCP revision 2025-11-25 with Origin validation for HTTP, concise safety instructions, typed resources/tools/prompts, errors, consent, capability negotiation, and cancellation/progress where useful.
- **Rationale:** MCP is the client-neutral agent integration boundary.
- **Inputs:** MCP requests and connection/permission context.
- **Outputs:** Structured inventory/project/availability/suggestion/preflight/conflict/policy/evidence responses and guarded reservation/lease mutation results.
- **Preconditions:** MCP server is configured for the selected transport and policy.
- **Normal flow:** Negotiate → enforce instructions/scope/tool schema → call application service → return structured evidence/error.
- **Error flow:** Invalid argument, unavailable component, unauthorized mutation, path escape, cancellation, and stale state are rejected safely.
- **Security constraints:** Fixed tool allowlists, bearer token rotation, read-only default, and no source-patch, managed-launch, process-termination, Docker-lifecycle, arbitrary-shell, arbitrary-file, or complete-environment capability.
- **Acceptance:** `AC-004` and `AC-008` complete through MCP; transport/auth/input contract tests pass.
- **Backlog:** `US-070`, `US-071`.
- **Related tests:** `VT-SRS-MCP-001`, `UAT-004`, `UAT-008`.
- **Component:** `CMP-MCP`, `CMP-SEC`.

### SRS-MCP-002 — Agent-safe workflow and client setup

- **Priority:** Must
- **Description:** Implement resolve ProjectInstance → inspect policy and evidence → preflight → diagnose → suggest → reserve or lease → return the current managed/unmanaged limitation; provide copy-ready Codex-first and client-neutral MCP setup, connection test, rollback, disable, and uninstall instructions without editing client configuration.
- **Rationale:** Tools are safe only when orchestrated with explicit scope and user authority.
- **Inputs:** Current project/client selection, transport/permission mode, agent task, user approval where required.
- **Outputs:** Redacted client-config instructions, connection-test result, rollback/disable guidance, explained reservation/lease and evidence, and safe audit record.
- **Preconditions:** ProjectInstance scope and selected client/transport are known and authorized.
- **Normal flow:** Generate redacted instructions → user applies configuration outside PortAtlas → test the connection → provide disable/rollback guidance; during a task enforce instance scope, inspect evidence, and use only approved reservation/lease commands.
- **Error flow:** Client format mismatch or failed test returns safe corrective and rollback guidance without changing client files; repository/model text cannot change policy; unmanaged race is explained.
- **Security constraints:** No global or project client-config write, project-source edit, managed launch, process termination, Docker lifecycle mutation, scope broadening, or model-controlled mutation.
- **Acceptance:** `AC-004`, `AC-009`, and `AC-013` preserve approval and authority boundaries; `SM-06` passes.
- **Backlog:** `US-072`, `US-073`, `US-074`.
- **Related tests:** `VT-SRS-MCP-002`, `UAT-004`, `UAT-009`, `UAT-013`.
- **Component:** `CMP-MCP`, `CMP-CFG`, `CMP-SEC`, `CMP-AUD`.

## Optional local AI

### SRS-AI-001 — Optional Ollama provider configuration

- **Priority:** Should; conditional MVP
- **Description:** Offer default-off Ollama endpoint configuration (loopback default), health/version/model discovery, metadata/capability probing, model role selection, benchmark, timeout/concurrency/keep-alive/cancellation/resource controls, disable/forget, and explicit download approval.
- **Rationale:** Local model availability and capability vary and cannot be assumed.
- **Inputs:** Explicit user configuration and local provider responses.
- **Outputs:** `AIProviderProfile`, provider/model/capability status and safe errors.
- **Preconditions:** User chooses to enable AI; no automatic provider/model installation.
- **Normal flow:** Validate endpoint → test health/version → list/inspect models → probe capabilities → save approved profile.
- **Error flow:** Absent/stopped/overloaded/missing model/timeout/cancellation is visible and bounded; no indefinite retry.
- **Security constraints:** Loopback default, bounded context/output/concurrency, isolated event-loop calls, no auto model activation/download.
- **Acceptance:** `AC-010` proves absence/unavailability does not affect core.
- **Backlog:** `US-080`.
- **Related tests:** `VT-SRS-AI-001`, `UAT-010`.
- **Component:** `CMP-AI`, `CMP-CFG`, `CMP-WEB`.

### SRS-AI-002 — Read-only AI inventory and explanations

- **Priority:** Should; conditional MVP
- **Description:** Translate natural-language requests into a bounded read-only PortAtlas query sequence and generate evidence-grounded inventory answers, conflict explanations, and project summaries labeled non-authoritative.
- **Rationale:** Natural language can improve comprehension but must not replace deterministic services.
- **Inputs:** Typed user task and minimized redacted authoritative records/tools.
- **Outputs:** Generated result with provider/model/version, timestamp, evidence, validation, confidence/staleness/warnings, request ID.
- **Preconditions:** `SRS-AI-001` enabled compatible provider and user granted the capability.
- **Normal flow:** Build safe context → allow bounded read-only tools → generate structured result → validate → display with deterministic evidence.
- **Error flow:** Unsupported question/tool, insufficient evidence, timeout, or invalid output yields typed failure with no state mutation.
- **Security constraints:** No hidden chain-of-thought return, arbitrary file/network/shell/process tool, or authority over conflicts/availability/reservations.
- **Acceptance:** `AC-011` explains the exact deterministic conflict without changing state; `AC-014` returns no secret.
- **Backlog:** `US-081`.
- **Related tests:** `VT-SRS-AI-002`, `UAT-011`, `UAT-014`.
- **Component:** `CMP-AI`, `CMP-DOM`, `CMP-SEC`.

### SRS-AI-003 — AI context, validation, injection defense, and retention

- **Priority:** Must if any AI ships
- **Description:** Enforce typed task, minimum context, approved roots, redaction, untrusted-data delimiters, evidence IDs, strict JSON/schema/semantic/path/port/protocol validation, non-authoritative storage, bounded tools/time, safe retention/deletion, and core-state isolation.
- **Rationale:** Repository/model output is untrusted and small-model failure must not cross the authority boundary.
- **Inputs:** Typed task, authoritative evidence, privacy/retention policy, provider output.
- **Outputs:** Validated advisory result or typed safe error; context/audit metadata without raw prompt by default.
- **Preconditions:** AI capability explicitly enabled and inputs resolve within approved scope.
- **Normal flow:** Secret-check → minimize/redact/delimit → generate → strict parse/validate/evidence-check → label/store under policy.
- **Error flow:** Malformed/unknown fields, invalid evidence/path/port/tool request, prompt injection, or provider failure is rejected; core state remains byte/transactionally unaffected.
- **Security constraints:** Fixed read-only allowlist, no permissive repair in safety-sensitive output, no secrets/full environment/source tree/raw prompt default, purge control.
- **Acceptance:** `AC-010`, `AC-012`, `AC-013`, `AC-014`, and `AC-015` pass; an AI candidate remains `AI suggested` until deterministic/user confirmation.
- **Backlog:** `US-082`, `US-083`, `US-084`.
- **Related tests:** `VT-SRS-AI-003`, `UAT-010`, `UAT-012`, `UAT-013`, `UAT-014`, `UAT-015`.
- **Component:** `CMP-AI`, `CMP-SEC`, `CMP-AUD`.

## Operations, audit, and configuration

### SRS-OPS-001 — macOS installation and lifecycle

- **Priority:** Must
- **Description:** Provide a normal-user macOS package and documented start, stop, restart, status, logs, upgrade, rollback, backup, restore, uninstall, and data/config-location lifecycle without requiring a repository clone.
- **Rationale:** A local utility succeeds only when installation and recovery are reliable.
- **Inputs:** Release artifact, local user choice, existing compatible state/backup.
- **Outputs:** Installed/controlled service, verified migration or rollback, documented retained/removed data.
- **Preconditions:** Supported macOS and verified package integrity; signing strategy follows approved ADR.
- **Normal flow:** Install → initialize/restore → start/status → operate → back up → upgrade/migrate/verify → rollback/restore if needed → uninstall by choice.
- **Error flow:** Failed install/migration/service start preserves recoverable state and returns documented diagnostics.
- **Security constraints:** Least privilege, no automatic `sudo`, clear executable/data locations, signed releases where practical.
- **Acceptance:** `SM-01` and `SM-11` pass on clean and upgrade profiles.
- **Backlog:** `US-100`, `US-101`.
- **Related tests:** `VT-SRS-OPS-001`.
- **Component:** `CMP-OPS`, `CMP-DB`, `CMP-CFG`.

### SRS-OPS-002 — Audit trail and safe local observability

- **Priority:** Must
- **Description:** Record meaningful read, write, reservation/lease, conflict suppression, integration, configuration, agent, and AI metadata events with actor/source, scope, result, time, correlation, and evidence references.
- **Rationale:** Sensitive local automation needs accountability and diagnosability.
- **Inputs:** Application actions, component health/errors, correlation context.
- **Outputs:** Queryable `AuditEvent`, structured local logs/metrics, redacted diagnostic bundle.
- **Preconditions:** Local persistence/logging is writable or degradation is reportable.
- **Normal flow:** Classify event → redact/minimize → attach correlation/evidence → persist/emit local metric.
- **Error flow:** Audit/log failure is visible and cannot leak the rejected payload; safety-critical mutation may fail closed per policy.
- **Security constraints:** No secrets, full environment lines, raw prompts, hidden model reasoning, or external telemetry by default.
- **Acceptance:** Mutation and integration scenarios have correlated safe audit records; seeded secret scan remains empty.
- **Backlog:** `US-053`.
- **Related tests:** `VT-SRS-OPS-002`.
- **Component:** `CMP-AUD`, `CMP-SEC`.

### SRS-OPS-003 — Versioned configuration, migration, backup, and reset

- **Priority:** Must
- **Description:** Manage platform-appropriate versioned configuration for roots, ignore/scan/collector rules, ranges/catalog/refresh/retention, integrations/security/UI/demo/plugins/AI; support validation, migration, import/export, backup/restore, defaults, and read-only policy mode. The proposed project-manifest schema is a separate unpublished design contract, not an MVP parser or public configuration namespace.
- **Rationale:** No important behavior should require editing application source, and upgrades must preserve user control.
- **Inputs:** UI/CLI request, config file/import, defaults, current schema and secret-store references.
- **Outputs:** Validated versioned config, migration/backup record, safe export, or recovery guidance.
- **Preconditions:** Actor is locally authorized; secrets remain in separate storage.
- **Normal flow:** Parse → validate schema/semantics → preview change/migration → back up → atomically persist → notify affected components.
- **Error flow:** Corrupt/unsupported configuration preserves last-known-good state and offers restore/reset; no partial migration.
- **Security constraints:** Secret storage separated, exports redacted, global agent config never silently edited, mutation audited.
- **Acceptance:** Configuration round-trip, migration recovery, backup/restore, and reset verification pass; `AC-006` uses UI configuration.
- **Backlog:** `US-052`.
- **Related tests:** `VT-SRS-OPS-003`, `UAT-006`.
- **Component:** `CMP-CFG`, `CMP-DB`, `CMP-SEC`.
