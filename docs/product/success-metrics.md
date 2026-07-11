# PortAtlas Success Metrics

## Measurement policy

Success metrics are evaluated locally or in controlled test/UAT environments. They do not authorize telemetry. Each result must record the build, machine profile, dataset/fixture, command or UAT script, timestamp, and pass/fail evidence. Anonymous external measurement would require a separate privacy review, explicit opt-in, ADR, and founder approval.

## MVP metrics

| ID | Outcome | Target | Measurement method | Evidence gate |
| --- | --- | --- | --- | --- |
| SM-01 | Time to first dashboard | Under 5 minutes for a first-time user | Clean supported macOS profile; time from installer start to usable overview | Packaging/UAT, Gate 9 |
| SM-02 | Root setup without code | User adds, previews, approves, and scans a root without source edits | Playwright flow plus founder UAT | UI, Gate 7 |
| SM-03 | Exact declaration coverage | At least 90% of exact port declarations in the supported MVP format corpus | Versioned labeled corpus; exact true positives divided by supported exact declarations | Discovery, Gate 5 |
| SM-04 | Runtime update latency | 95th percentile at or below 2 seconds under normal load | Start/stop controlled listeners; timestamp collector event and rendered update | Runtime/UI, Gates 4 and 7 |
| SM-05 | Ownership/source discoverability | Port owner and source reachable in no more than 2 interactions | Task-based UI test from overview or ports search | UI, Gate 7 |
| SM-06 | Agent coordination | Agent checks, receives an explained suggestion, and acquires a lease in one MCP workflow | Automated MCP contract scenario and Codex UAT | Integration, Gate 8 |
| SM-07 | Concurrent allocation safety | Zero duplicate active leases in the defined concurrent allocator suite | Property and integration tests across same-range simultaneous requests | Allocator, Gate 6 |
| SM-08 | Secret safety | Zero seeded secret values in default logs, API/MCP output, UI snapshots, exports, or AI context/results | Canary-secret fixtures and automated scans | Security, Gates 3–9 |
| SM-09 | Offline core | All core inventory, discovery, registry, conflict, UI, API, CLI, and MCP flows work with network egress unavailable | E2E profile with external network disabled and no AI provider | Release, Gate 9 |
| SM-10 | Developer-laptop scale | 500 repositories, 2,000 declarations, and 1,000 observations without noticeable UI lag | Reference dataset; interaction latency and resource profile recorded | Performance, Gates 7 and 9 |
| SM-11 | Lifecycle readiness | Fresh install, upgrade, backup, restore, rollback, and uninstall are documented and tested | Clean-machine matrix and artifact checklist | Packaging, Gate 9 |
| SM-12 | Future managed-launch safety | No collision in the defined Version 1 managed-runner concurrent tests when that capability ships | Preflight/lease/inject/start/verify/cleanup test with competing integrated clients | Version 1; not an MVP metric |
| SM-13 | AI independence | Core suite passes with Ollama absent, stopped, invalid, and disabled | Core-state comparison across provider-failure profiles | Conditional AI, Gate 8 |
| SM-14 | AI structured validity | 100% of accepted machine-readable AI results pass strict schema, semantic, scope, and evidence validation | Evaluation corpus; malformed and adversarial outputs must be rejected | Conditional AI, Gate 8 |
| SM-15 | Accessibility baseline | No critical automated accessibility violation in primary flows and all manual keyboard/screen-reader checks pass | Playwright/axe-equivalent plus manual WCAG checklist | UI/release, Gates 7 and 9 |

## Definitions and guardrails

### Supported declaration corpus

`SM-03` measures only the locked MVP set—Compose; Dockerfile `EXPOSE`; safe `.env*` port keys; `package.json` scripts/workspaces; Vite/Next/Nuxt/SvelteKit; Python launcher commands and `pyproject.toml`; Tauri configuration; Makefile, Taskfile, Procfile, and justfile—represented by reviewed labeled fixtures or founder-approved real-project samples. Framework defaults without explicit evidence and broad numeric literals do not count as exact declarations. Precision, false positives, unsupported files, permission failures, and parser version must be reported alongside recall.

### Normal load

For `SM-04`, normal load means the reference MVP dataset up to the `SM-10` scale target on a documented supported developer-laptop profile, without synthetic CPU or disk pressure. Collector detection, reconciliation, API event, and UI render timestamps must be separable so regressions can be located.

### Noticeable UI lag

For `SM-10`, acceptance requires the interaction thresholds set in the performance plan plus founder UAT. At minimum, filtering, sorting, opening a row, navigating to a project, and returning to the inventory must remain responsive, with long scans off the API event loop and cancellable.

### Secret

A secret includes passwords, tokens, keys, cookies, private keys, credential-bearing URLs, cloud/SSH credentials, and unrelated environment values. A pass requires absence of the seeded value, not merely masking a UI field while retaining it elsewhere.

### One MCP workflow

`SM-06` permits multiple typed tool calls within one continuous agent task. It requires project resolution, policy/state check, explained suggestion, atomic lease result, and no unauthorized edit. It does not require a managed service launch in MVP.

## Operational health indicators

These indicators guide quality but do not create external analytics:

- Collector success/failure, duration, capability gaps, and reconciliation age.
- Scan progress, cancellation, file/parser counts, cache hit/miss, and permission errors.
- Conflict counts by normalized type and severity.
- Lease acquisition, renewal, expiry, collision, and transaction rollback.
- API/CLI/MCP request latency, stable error codes, and cancellation.
- AI provider status, validation rate, timeout/cancellation, evidence-reference success, context size, and redaction events without raw prompt content.

## Metric ownership and review

| Metric family | Accountable role | Review point |
| --- | --- | --- |
| Product task success | Product/UX and founder | Gates 1, 7, and 9 |
| Collector/discovery accuracy | Collector/scanner and QA | Gates 4 and 5 |
| Allocation correctness | Domain/allocator and QA | Gate 6 |
| Security/privacy | Security reviewer and QA | Every implementation gate |
| Performance/reliability | Backend/frontend owners and QA | Gates 4, 7, and 9 |
| AI quality/safety | AI/security/QA owners | Gate 8 only if included |
| Install/release | Packaging/release owner | Gate 9 |

## Related documents

- [PRD](prd.md)
- [Acceptance criteria](../requirements/acceptance-criteria.md)
- [Non-functional requirements](../requirements/non-functional-requirements.md)
- [Traceability matrix](../requirements/traceability-matrix.md)
