# Gate 4 Runtime Inventory Sprint Brief

- **Status:** **PROPOSED — founder review required; no Gate 4 behavior authorized**
- **Planning date:** 2026-07-14
- **Planning authority:** Gate 3 [passed on 2026-07-14](gate-3-evidence.md) at immutable engineering candidate `4adf1fb500b651e425735595db528fd42fffba73` and authorized Gate 4 sprint planning only
- **Planning base:** Integrated Gate 3 closure successor `461243541d6b63ddebf54598c6860ba73abcd012`; this administrative successor does not replace the approved Gate 3 engineering candidate
- **Proposed working branch:** `codex/gate4-runtime-inventory`
- **Gate owner:** Founder
- **Implementation authority:** None until the founder accepts this brief at an exact revision
- **Evidence rule:** Every `G4-*` item starts as **Evidence pending**; intent, file presence, fixture-only success, or a narrower local check cannot satisfy an item

## Goal and increment sequence

Gate 4 proposes one runtime-inventory delivery contract split into two sequential two-week-equivalent increments:

1. **Increment A — host vertical slice:** typed runtime contracts, persistence and reconciliation, macOS host collection, safe process/interface evidence, a bounded authenticated API/CLI projection, transactional event outbox/SSE delivery, and real-machine proof.
2. **Increment B — optional Docker and integrated reconciliation:** Docker API negotiation, container/port normalization, event plus periodic reconciliation, optional-service isolation, and combined scale/failure evidence.

Increment B depends on the accepted state and reconciliation semantics produced by Increment A. Neither increment may begin while this brief remains Proposed. The gate is intended to prove accurate, privacy-safe runtime evidence on the supported macOS profile while keeping Docker optional. It does not authorize project discovery, source scanning, conflict computation, allocation, product UI journeys, MCP, AI, packaging, release, or publication.

## Proposed decisions pending founder acceptance

Acceptance of this brief would ratify only the following Gate 4 delivery decisions. They remain Proposed until then.

| Topic | Proposed Gate 4 resolution |
| --- | --- |
| Branch and historical base | Implement from integrated closure successor `461243541d6b63ddebf54598c6860ba73abcd012` on `codex/gate4-runtime-inventory`; retain `4adf1fb500b651e425735595db528fd42fffba73` as the immutable approved Gate 3 engineering candidate. |
| Host collector | Use `psutil` behind `CMP-COL` as the primary macOS source, with tested `lsof -nP` argument-array fallback and validation. Record capability, source, permission, timeout, and parse limitations rather than inventing evidence. |
| Acceptance-scenario scope | Advance only the collector-evidence portion of `AC-001`/`UAT-001` and the runtime-observation prerequisite of `AC-003`/`UAT-003`; both scenarios remain open for final Gate 7 acceptance. Make no Gate 4 claim for `AC-007`/`UAT-007`. |
| API and CLI | Implement only authenticated system status/capabilities, collectors, refresh, and cursor-paginated observation inventory under `/api/v1`; limit the CLI to `status`, `ports`, and `collectors refresh`. This is a partial disposition of `SRS-API-001` and `SRS-CLI-001`, not the complete MVP surfaces. |
| `SRS-COL-004` boundary | Implement runtime collector intervals, manual refresh, Docker events, periodic reconciliation, last-known-good state, and update events. Filesystem watcher, scanner debounce, scan cache, and project-scan behavior remain Gate 5 work. |
| Association boundary | Store only nullable, association-ready evidence seams from validated, redacted, source-attributed runtime or Docker metadata. Do not discover or assign projects, worktrees, repositories, roots, source declarations, or concrete `ProjectInstance` relationships in Gate 4. Unknown association remains Unknown; Gate 5 owns identity resolution and association. |
| Partial-result semantics | A partial collection may atomically add or refresh verified positive facts but cannot retire prior facts merely because they are absent. Only a complete, comparable snapshot may mark prior facts stale; hard deletion is outside reconciliation. Every result records completeness, capability, source, collection time, and safe degradation details. |
| Conflict boundary | Reconciliation may emit affected port/resource keys and schema-versioned invalidation events. It must not compute, classify, store, or display Gate 6 conflicts or exposure warnings. |
| Real integrations | Require a documented real Apple-silicon macOS profile and at least one real Docker Engine API negotiation run when Docker evidence is assessed. The default core suite still runs and passes with Docker unavailable. |
| SSE replay | Keep the exact replay-retention duration as a Gate 4 research result to lock from measured reconnect/restart behavior. Preserve the accepted bounded `Last-Event-ID`/resynchronization contract; record any material contract change through the ADR process. |

These resolutions do not rename or weaken an accepted upstream requirement. Where Gate 4 implements only a subset, the unimplemented remainder retains its original owner and final gate.

## Evidence-bound work items

The identifiers and boundaries below are stable for this proposed sprint. **Evidence pending** is a factual status: no Gate 4 implementation or acceptance evidence exists yet.

| ID | Increment | Work item and boundary | Dependencies | Required evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `G4-00` | A | Confirm Gate 3 closure, exact planning base, branch, working-title/publication restrictions, and all later-gate exclusions before behavior begins. | Founder acceptance of this brief at an exact revision; closure successor `461243541d6b63ddebf54598c6860ba73abcd012` | Branch ancestry and clean-state record prove the closure base; scope audit finds no Gate 5–9 behavior or public namespace action. | Evidence pending |
| `G4-01` | A | Maintain this brief, one Gate 4 evidence ledger, requirement/test crosswalk, and explicit partial dispositions without expanding the gate through implementation convenience. | `G4-00` | Every `G4-00`–`G4-17` row has scope, verification, evidence link, and final disposition; traceability validators pass. | Evidence pending |
| `G4-02` | A | Define typed runtime contracts for collector capabilities/results, socket/process/container identities, observations, snapshot completeness, freshness/staleness, and safe degradation. | Accepted Gate 3 domain/adapter seams; `G4-01` | `TEST-ARCH-001`, `UT-DOM-001`, and contract/property tests prove normalized invariants, opaque identity, revision/time injection, optional metadata, and inward dependency direction. | Evidence pending |
| `G4-03` | A | Add runtime-observation persistence, migrations, repositories, unit-of-work behavior, last-known-good snapshots, transactional audit/outbox writes, structured local logs with correlation IDs, and bounded local collector metrics. Allocation, registry, conflict, project-discovery repositories, diagnostic export, and the complete later-action audit surface remain excluded. | `G4-02`; ADR 0002 | `IT-SQL-001`, the Gate 4 subsets of `VT-SRS-OPS-002` and `VT-SRS-NFR-008`, and redaction/failure tests prove migration, rollback, atomic snapshot/audit/outbox commit, restart recovery, stale marking, correlated safe logs/local metrics, no external telemetry, and repository contracts; `IT-PG-001` remains opt-in compatibility evidence. | Evidence pending |
| `G4-04` | A | Normalize protocol, address family, bind/interface semantics, TCP/UDP state, timestamps, source/capability, PID plus start time, and container/host distinctions without inventing unavailable fields. | `G4-02` | `UT-DOM-001`, `UT-COL-001`, `VT-SRS-COL-001`, and `VT-SRS-COL-002` cover IPv4/IPv6, TCP/UDP, loopback/wildcard/specific binds, malformed/unknown values, PID reuse, and deterministic serialization. | Evidence pending |
| `G4-05` | A | Implement the macOS `psutil` collector behind `CMP-COL`, using only existing user permissions and bounded read-only inspection. Linux and Windows remain adapter contracts only. | `G4-04` | Fake/fixture tests plus `VT-SRS-COL-001` and `VT-SRS-COL-002` real controlled-listener evidence show correct facts, named permission gaps, bounded execution, and no elevation. | Evidence pending |
| `G4-06` | A | Implement and compare a bounded `lsof -nP` fallback/validation adapter using argument arrays, strict parsing, timeout/output limits, and safe errors. It is not an arbitrary subprocess facility. | `G4-04`; capability/failure output from `G4-05` | `UT-COL-001` and real comparison evidence cover source selection, fallback, drift/malformed output, timeout, missing binary, permission denial, and redacted diagnostics. | Evidence pending |
| `G4-07` | A | Collect and minimize the permitted `SRS-COL-002` process facts—PID plus start time, executable, redacted command, user, working directory, and parent—before persistence or transport; permit only nullable project/service/`ProjectInstance` evidence seams and never perform project/root/worktree discovery or relationship assignment. | `G4-02`–`G4-06`; accepted `CMP-SEC` controls | `SEC-T-SECRET-001`, `VT-SRS-SEC-002`, `VT-SRS-COL-002`, permission/exit/PID-reuse fixtures, and canary scans prove each permitted field is accurate or explicitly Unknown. Working-directory/user data is minimized and restricted to authenticated local product surfaces; unsafe arguments, credentials, environment values, and unredacted personal paths remain absent from logs, audit payloads, diagnostics, and evidence artifacts. | Evidence pending |
| `G4-08` | A | Implement the runtime collection coordinator, intervals/manual refresh, atomic reconciliation, last-known-good/degraded state, bounded cancellation/backoff, and the proposed partial-result semantics. Do not invoke filesystem scanning or compute conflicts. | `G4-03`–`G4-07` | `UT-COL-001`, `IT-SQL-001`, `TEST-ISO-001`, and runtime subset of `VT-SRS-COL-004` cover complete/partial/failure results, no absence-based retirement, restart, cancellation, retry bounds, and unchanged authoritative state on failure. | Evidence pending |
| `G4-09` | A | Expose the bounded authenticated REST/CLI subset: system status/capabilities, collectors, refresh, cursor-paginated observation inventory; CLI `status`, `ports`, and `collectors refresh`. No other advertised MVP command/resource becomes implemented. | `G4-08`; Gate 3 auth/API/CLI seams | `CT-API-001`, `CT-CLI-001`, `SEC-T-AUTH-001`, bounded `VT-SRS-API-001`, `VT-SRS-CLI-001`, and `VT-SRS-SEC-003`, plus `PERF-API-001`, prove loopback binding, origin/CSRF/session and credential scopes, safe errors, pagination, human/JSON/piped output, stable exits, and no secret-bearing response. | Evidence pending |
| `G4-10` | A | Publish committed runtime changes through a transactional outbox and authenticated dashboard SSE invalidation stream with event ID/type/time/resource identity/revision/schema version, bounded replay, and resynchronization. Events are hints, not full source-of-truth snapshots. | `G4-03`, `G4-08`, `G4-09`; ADR 0005 | `CT-API-001`, `SEC-T-AUTH-001`, `VT-SRS-SEC-003`, `PERF-SSE-001`, and restart/gap/duplicate/out-of-order/slow-consumer tests prove commit ordering, `Last-Event-ID`, expired-cursor resync, authorization, origin/session enforcement, and no event-secret leakage. Replay-duration research is recorded. | Evidence pending |
| `G4-11` | A | Produce real-machine host evidence on the supported Apple-silicon macOS profile for the complete host vertical slice. Synthetic and fixture evidence remains necessary but is insufficient alone. | `G4-02`–`G4-10` | Controlled TCP/UDP IPv4/IPv6 listener matrix, bind/interface variants, PID/start-time and permission cases, `psutil`/`lsof` comparison, API/CLI/SSE projections, last-good recovery, `PERF-COL-001`, and a redacted machine profile. | Evidence pending |
| `G4-12` | B | Add an optional Docker SDK probe with Engine API negotiation, read-only capability reporting, timeouts, permission-safe failure, and clean degradation when absent/stopped/denied. No Docker lifecycle command is allowed. | Accepted `G4-02`–`G4-11`; ADR 0004 | `TEST-ISO-001`, `IT-DKR-001`, fake endpoint tests, Docker-unavailable default profile, and one real negotiation run prove version negotiation and unchanged authoritative core state on failure. | Evidence pending |
| `G4-13` | B | Normalize running/stopped container identity, safe name and image/tag, health, start time, restart policy, internal/exposed ports, published host bindings/interfaces, networks, and safe Compose project/service labels while preserving native/container distinctions. Labels may supply nullable association evidence but cannot trigger project discovery. | `G4-04`, `G4-07`, `G4-12` | `UT-DOM-001`, `UT-COL-001`, `IT-DKR-001`, and `VT-SRS-COL-003` cover every listed identity/state field and distinguish internal/exposed/published state, multiple bindings, IPv4/IPv6, stopped/unhealthy containers, missing/unknown metadata, malformed or secret labels, and unknown associations. | Evidence pending |
| `G4-14` | B | Combine Docker events with periodic complete-snapshot reconciliation, deduplication, revision ordering, event-loss recovery, last-known-good state, and the same partial-result rule used for host collection. | `G4-08`, `G4-10`, `G4-12`, `G4-13` | `IT-DKR-001`, `CT-API-001`, `TEST-ISO-001`, and runtime subset of `VT-SRS-COL-004` cover missed/duplicate/out-of-order events, daemon restart, reconciliation convergence, backpressure, and SSE invalidation. | Evidence pending |
| `G4-15` | B | Prove optional Docker integration security and failure isolation: read-only API use, no lifecycle operations, no remote unauthenticated surface, bounded resources, redacted labels/errors, and core independence. | `G4-12`–`G4-14` | `TEST-ARCH-001`, `TEST-ISO-001`, `SEC-T-AUTH-001`, `SEC-T-SECRET-001`, applicable Gate 4 subsets of `VT-SRS-SEC-001`–`003` and `VT-SRS-NFR-008`, negative API/CLI tests, dependency review, and outbound/lifecycle-operation audit show no Docker mutation, secret leakage, or external telemetry. | Evidence pending |
| `G4-16` | B | Run the integrated macOS/Docker evidence profile for accuracy, update latency, cursor paging, restart/recovery, churn/event loss, and 1,000 runtime observations. This is only the runtime subprofile of `SM-10`. | `G4-11`–`G4-15` | `PERF-COL-001`, `PERF-SSE-001`, `PERF-API-001`, storage portion of `PERF-DB-001`, applicable Gate 4 subsets of `VT-SRS-NFR-001`–`003` and `VT-SRS-NFR-006`–`008`, real Docker negotiation, Docker-absent profile, accuracy matrix, resource report, and zero canary leakage all pass their Gate 4 thresholds. | Evidence pending |
| `G4-17` | Closure | Assemble the exact-revision Gate 4 evidence record and obtain a founder disposition without implying Gate 5 behavior, final UAT, packaging, release, publication, or name clearance. | `G4-00`–`G4-16` | Exact candidate revision, local/hosted commands and counts, environments, optional-profile disposition, evidence links/hashes, risks, clean/synced Git state, and exact founder approval are recorded. | Evidence pending |

## Traceability and partial dispositions

Gate 4 proposes primary product work for `US-011`, `US-012`, and `US-020` through `US-023`. It also advances only the internal audit/observability prerequisite of `US-053`; that story's complete reviewer workflow and diagnostic interfaces remain Gate 7 and release work. Primary requirements are `SRS-COL-001` through `SRS-COL-004`; components are `CMP-DOM`, `CMP-COL`, `CMP-DKR`, `CMP-DB`, `CMP-API`, `CMP-AUD`, and `CMP-SEC`, with bounded use of `CMP-CLI` and `CMP-CFG`. The authoritative detailed mapping is in the [traceability matrix](../requirements/traceability-matrix.md#gate-4-runtime-inventory-traceability).

| Contract | Proposed Gate 4 disposition | Verification | Final owner |
| --- | --- | --- | --- |
| `SRS-COL-001` | Full macOS host-collector behavior for the stated platform, while Linux/Windows remain contract-only. | `VT-SRS-COL-001`; `UT-COL-001`; `PERF-COL-001` | Gate 4 |
| `SRS-COL-002` | PID plus start time, executable, redacted command, user, working directory, parent, bind/interface facts, and nullable project/service/`ProjectInstance` association evidence; no project discovery/assignment and no `AC-007` warning claim. | `VT-SRS-COL-002`; `UT-DOM-001`; `SEC-T-SECRET-001` | Gate 4 runtime facts/evidence; Gate 5 identity association; Gate 7 UAT presentation |
| `SRS-COL-003` | Optional Docker identity/state, bindings, networks, safe Compose-label association evidence, health, image/tag, start time, and restart policy; no project assignment or conflict computation. | `VT-SRS-COL-003`; `IT-DKR-001`; `TEST-ISO-001` | Gate 4 runtime facts/evidence; Gate 5 identity association; Gate 6 conflict computation; Gate 7 `AC-003` completion |
| `SRS-COL-004` | Runtime intervals, manual refresh, Docker events, periodic reconciliation, last-good/degraded state, and SSE; filesystem watcher/scan/debounce/cache behavior remains excluded. | Runtime subset of `VT-SRS-COL-004`; `CT-API-001`; `PERF-SSE-001` | Gate 4 runtime subset; Gate 5 scanner subset |
| `SRS-API-001` | Authenticated system/capability, collector/refresh, observation-page, and event endpoints only. | Bounded `VT-SRS-API-001`; `CT-API-001`; `PERF-API-001` | Later gates complete remaining resources/commands |
| `SRS-CLI-001` | `status`, `ports`, and `collectors refresh` only, in safe human and machine modes. | Bounded `VT-SRS-CLI-001`; `CT-CLI-001` | Later gates complete remaining commands |
| `SRS-SEC-001`–`003` | Apply offline core, zero secret disclosure, least privilege, read-only subprocess/Docker access, local authenticated API/SSE, and no telemetry to every Gate 4 surface. Later UI, path-scanner, MCP, model, export, and release surfaces remain with their owning gates. | Gate 4 subsets of `VT-SRS-SEC-001`–`003`; `TEST-ISO-001`; `SEC-T-AUTH-001`; `SEC-T-SECRET-001` | Partial Gate 4 evidence; full cross-cutting verification continues through release |
| `SRS-NFR-001`, `003`, `006`, `007` | Apply bounded runtime/API responsiveness, collector/Docker/persistence failure isolation, typed modularity, and macOS-first collector adapter isolation. Scanner/UI/provider/packaging portions remain later work; `SRS-NFR-006` applies fully to each Gate 4 change. | Gate 4 subsets of `VT-SRS-NFR-001`, `003`, `006`, and `007`; architecture, isolation, collector, API/CLI, and performance suites below | Partial Gate 4 evidence except per-change engineering quality; full cross-cutting verification continues through release |
| `SRS-NFR-008` | Implement correlated structured local logs, bounded local collector metrics, redaction, and no-external-telemetry audit for Gate 4 surfaces. User-facing diagnostic bundle/export and later-action coverage remain Gates 7 and 9. | Gate 4 subset of `VT-SRS-NFR-008`; `VT-SRS-OPS-002`; `SEC-T-SECRET-001`; outbound-network audit | Partial Gate 4 evidence; Gates 7 and 9 complete diagnostics |
| `SRS-OPS-002` | Record correlated, minimized audit events for Gate 4 reads, refreshes, collector/Docker integration state, results, and failures. Reservation/conflict/configuration/agent/AI events and complete audit/diagnostic interfaces remain later work. | Gate 4 subset of `VT-SRS-OPS-002`; `IT-SQL-001`; correlation/redaction/local-metrics checks | Partial Gate 4 evidence; later behavior gates and Gate 9 complete the audit contract |
| `SRS-NFR-002` | Only the 1,000-runtime-observation storage/query/reconciliation subprofile; repository/declaration scale, browser interaction, and founder scale UAT remain open. | Gate 4 subset of `VT-SRS-NFR-002`; `PERF-API-001`; storage portion of `PERF-DB-001`; `G4-16` | Gates 7 and 9 complete `SM-10` |

The founder-facing scenario disposition is deliberately partial:

- `AC-001`/`UAT-001`: Gate 4 may prove that accurate host/process evidence exists and is queryable. Gate 7 must still prove the complete two-interaction UI journey, accessibility, and final presentation.
- `AC-003`/`UAT-003`: Gate 4 may prove native and Docker runtime facts required by the scenario. Gate 6 must add conflict computation, and Gate 7 must complete the founder-facing conflict journey.
- `AC-007`/`UAT-007`: no Gate 4 acceptance claim. Gate 4 may normalize bind/interface facts, but exposure policy, warning classification, and user presentation remain later-gate work.

Metrics are similarly bounded: `SM-04` is measured at collector, commit, API-event, and test-subscriber boundaries in Gate 4 and completes with visible browser timing in Gate 7; `SM-08` requires zero seeded-secret matches across every implemented Gate 4 boundary; `SM-10` covers only the 1,000-observation runtime storage/query/reconciliation subprofile.

## Verification contract

Core checks must run without Docker, PostgreSQL, Ollama, Rust, packaging tools, or network access to public services. Live macOS and Docker profiles are explicit integration evidence and cannot turn absence into a passing result. Exact commands become supported only after implementation and successful execution are recorded in [Development setup](../operations/development-setup.md).

| Test or evidence ID | Gate 4 use |
| --- | --- |
| `TEST-ARCH-001` | Enforce collector/Docker/persistence/API/CLI dependency direction, interface isolation, no scanner/conflict/lifecycle behavior, and no adapter-owned policy. |
| `TEST-ISO-001` | Prove Docker absence/failure cannot corrupt or block host inventory, persistence, API, CLI, or SSE state. |
| `UT-DOM-001`, `UT-COL-001` | Prove typed observation identities, normalization, completeness/staleness, capability/error mapping, partial results, and deterministic revisions. |
| `IT-SQL-001` | Prove runtime migrations/repositories, transaction rollback, last-good recovery, and audit/outbox atomicity on ephemeral SQLite. |
| `IT-PG-001` | Reuse the runtime repository/migration contract as an opt-in compatibility profile; PostgreSQL is not required for Gate 4 core or product operation. |
| `IT-DKR-001` | Use fakes by default and one explicit real-engine profile for negotiation, normalization, events, reconciliation, permissions, and degradation. |
| `CT-API-001`, `CT-CLI-001` | Prove only the bounded Gate 4 REST/SSE/CLI surface, authentication, schemas, pagination, stable safe errors/exits, and no advertised later commands. |
| `SEC-T-AUTH-001` | Prove loopback-only binding, browser-origin/CSRF/session controls, bearer scope/permission checks, and unauthorized REST/SSE/refresh rejection for the bounded Gate 4 surface. |
| `SEC-T-SECRET-001` | Search canaries across collection, subprocess/Docker input, persistence, REST, SSE, CLI, audit, logs, diagnostics, and evidence artifacts. |
| `VT-SRS-SEC-001`, `VT-SRS-SEC-002`, `VT-SRS-SEC-003` | Prove the Gate 4 offline/no-telemetry, implemented-surface secret, and applicable least-privilege/origin/token/Docker/subprocess/resource boundaries without claiming later UI/path/MCP/model/export coverage. |
| `VT-SRS-NFR-001`, `VT-SRS-NFR-003`, `VT-SRS-NFR-006`, `VT-SRS-NFR-007` | Prove the bounded runtime/API responsiveness, applicable failure/restart recovery, per-change engineering quality, and macOS collector adapter isolation portions of their canonical records. |
| `VT-SRS-NFR-002` | Exercise only the 1,000-runtime-observation storage/query/reconciliation portion; the 500-repository/2,000-declaration/browser/founder-UAT portions remain open. |
| `VT-SRS-NFR-008`, `VT-SRS-OPS-002` | Prove Gate 4 correlation IDs, safe audit/log/local-metric records, redaction, and outbound no-telemetry behavior; user-facing diagnostic export and later action classes remain open. |
| `PERF-COL-001` | Require p95 collector-to-committed-normalized-state latency at or below 1.5 seconds under the documented Gate 4 normal-load profile. |
| `PERF-SSE-001` | Measure commit-to-test-subscriber invalidation and the server-side portion of the two-second target; visible browser completion remains Gate 7. |
| `PERF-API-001` | Require a warm p95 at or below 200 ms for a cursor page of 100 observation rows at the 1,000-observation runtime profile. |
| `PERF-DB-001` | Exercise only target-size runtime-observation migration/integrity/restart; packaging-related budget finalization remains Gate 9. |

Evidence records must name the exact revision, environment profile, actual tool/runtime versions, command, count, duration, result, optional-profile status, and safe artifact hash. Real-machine evidence must be redacted and may not contain usernames, personal absolute paths, process secrets, environment values, tokens, or Docker label secrets.

## Required demonstrations

### Increment A host vertical slice

On the documented supported Apple-silicon macOS profile:

1. Create controlled TCP and UDP listeners spanning IPv4 and IPv6 plus loopback, wildcard, and specific-address binds.
2. Show normalized protocol/address/port/state/source/time plus PID/start time, executable, redacted command, user, working directory, parent, and nullable association evidence where permitted; show explicit Unknown/permission-limited fields where not.
3. Compare the `psutil` primary result with the bounded `lsof -nP` fallback/validator and explain any capability difference from recorded evidence.
4. Show authenticated cursor-paginated REST, CLI human/JSON output, SSE invalidation, manual refresh, and last-known-good/degraded recovery without implying managed allocation assurance.

### Increment B Docker and reconciliation

With a controlled local Docker profile, and then with Docker disabled:

1. Show negotiated API capability plus running/stopped identity, safe name and image/tag, health, start time, restart policy, networks, internal-only/exposed ports, published host bindings/interfaces, safe Compose labels, and native/container distinction.
2. Lose or reorder an event, reconcile from a complete snapshot, preserve revision/order semantics, and show last-known-good/degraded status while the core remains healthy.
3. Demonstrate that no Docker start/stop/restart/create/remove operation, project discovery, conflict result, exposure warning, or secret-bearing label is produced.

The demo must call runtime observations **unmanaged discovery evidence**. It must not describe observation, a free port, or reconciliation as a managed allocation guarantee.

## Explicit non-goals

Gate 4 does not authorize:

- Gate 5 approved-root management, repository/project/service/worktree discovery, `Project`/`ProjectInstance` creation, source scanners/parsers, Compose-file parsing, filesystem watchers, scan debounce/cache, or declaration evidence;
- Gate 6 registry policy, suggestions, reservations, atomic leases, conflict/exposure computation, warnings, suppression, or resolution;
- Gate 7 full browser UI, onboarding, inventory/conflict journeys, accessibility UAT, `AC-001`, `AC-003`, or `AC-007` completion;
- Gate 8 MCP transports/tools, client integration, Ollama, local-AI behavior, model evaluation, or AI inclusion;
- Gate 9 packaging, install/service lifecycle, distributable artifacts, signing, notarization, updates, rollback, release-candidate evidence, release, or publication;
- Linux or Windows runtime implementations, required PostgreSQL operation, remote/server mode, telemetry, or public network services;
- process termination, managed launch, source editing, Docker lifecycle mutation, arbitrary shell/file access, automatic elevation, or any mutation beyond the separately gated MVP reservation/lease boundary; or
- package/image/manifest/domain/MCP/Homebrew namespace claims, trademark clearance claims, funding metadata, or any public use of the `PortAtlas` working title.

## Risks and stop conditions

Stop Gate 4 work and preserve the last safe state if any of the following occurs:

- behavior starts before exact-revision founder acceptance of this brief;
- collection requires elevation, shell interpolation, unbounded subprocess/Docker output, or a public/remote unauthenticated surface;
- a partial or failed snapshot retires prior evidence by absence, corrupts authoritative state, or hides staleness/degradation;
- PID-only identity, invented process/project ownership, collapsed host/container semantics, or unknown-to-known coercion reaches persistence or an interface;
- any seeded secret, complete environment value, unsafe process argument, credential, private absolute path, or Docker label secret reaches persisted/output/evidence artifacts;
- Docker becomes a core dependency or any lifecycle operation is implemented or invoked;
- reconciliation computes Gate 6 conflicts/exposures or invokes Gate 5 project/scanner behavior;
- API/CLI surfaces advertise unimplemented later-gate resources, commands, guarantees, or mutation;
- runtime events and REST state cannot converge after loss/restart, or measured latency/capacity exceeds the documented threshold without an explicit founder disposition;
- a release-like artifact, public namespace, telemetry, remote AI call, or name-clearance claim is created; or
- local evidence is used to close the gate without required hosted CI, real-machine profiles, clean/synced Git state, and founder disposition for the exact candidate.

## Exit gate and founder dispositions

Gate 4 can pass only when all `G4-00` through `G4-17` rows are **Accepted** in both this brief and the Gate 4 evidence ledger; the controlled real macOS matrix and at least one real Docker negotiation profile pass; the Docker-absent core profile, security, accuracy, recovery, SSE/API, paging, and 1,000-observation runtime checks pass; required hosted CI is green for the exact candidate; Git is clean and synchronized; and the founder explicitly approves that exact candidate revision. The closing disposition must use `Gate4 Approved at` followed by the exact 40-character candidate revision. An administrative evidence successor must not replace that immutable engineering candidate.

Founder acceptance of this Proposed brief, which authorizes implementation but does not pass Gate 4, must identify the exact brief revision and include this exact continuation prompt:

`Implement the founder-accepted Gate 4 Runtime Inventory sprint brief on codex/gate4-runtime-inventory; stop at the Gate 4 founder disposition after every G4-00 through G4-17 check is green.`

Until that acceptance is recorded, stop here: planning may be reviewed or amended, but no Gate 4 behavior may begin.
