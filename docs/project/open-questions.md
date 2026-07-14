# Open Questions

These questions are intentionally unresolved inputs. None may be answered by inventing founder identity, credentials, namespaces, or release state.

## Founder decisions required for later gates

| ID | Question | Why it matters | Needed by | Default while open |
|---|---|---|---|---|
| OQ-002 | Which replacement-name candidates should receive professional clearance if `PortAtlas` is not usable? | Current searches found domain and software-related trademark collisions. | Before public namespace creation | Use working title internally only |
| OQ-003 | What public signing identity and release email should artifacts use? | Packages and signed releases need verifiable ownership. | Packaging gate | Do not generate identities |
| OQ-004 | Which package, image, MCP, Homebrew, and domain namespaces are founder-approved after clearance? | Namespace squatting and accidental publication are irreversible external actions. | Public release | Publish nothing |
| OQ-005 | Which sponsorship platform and active handle should be advertised? | Funding metadata must point to a real account. | Funding configuration | Omit funding file |
| OQ-006 | What quantitative parser corpus represents the founder's real projects? | Recall and precision targets require labeled ground truth. | Scanner acceptance | Use synthetic fixtures plus founder-selected sample later |
| OQ-007 | What target inventory capacity is representative beyond the baseline test envelope? | Performance thresholds should match real local estates. | Performance gate | Test documented baseline and report scaling curve |
| OQ-008 | Should PostgreSQL expand beyond the accepted optional compatibility profile in a future server mode? | A supported multi-process profile would change operations, concurrency evidence, and product scope. | Version 1/server-mode decision | Compatibility profile only |
| OQ-010 | Which local model families and hardware envelopes should AI evaluation cover? | Inclusion must be based on reproducible performance, safety, and privacy evidence. | AI evaluation | No model is endorsed or required |

## Resolved gate questions

| ID | Resolution | Evidence |
| --- | --- | --- |
| OQ-001 | Gate 2 was founder-approved on 2026-07-11 at exact revision `e53f39916b2348e8626375bb33cac147e27bd217`; Gate 3 subsequently passed on 2026-07-14 at exact engineering candidate `4adf1fb500b651e425735595db528fd42fffba73`. | [Gate 2 approval](gate-2-approval.md), [Gate 3 evidence](gate-3-evidence.md) |
| OQ-009 | MVP browser sessions are in-memory and invalidated on service restart, logout, or credential rotation, with a configurable bounded inactivity timeout. | [ADR 0011](../adr/0011-auth.md) |

The Python web/runtime stack, SQLite default, PostgreSQL compatibility-only profile, React data/accessibility primitives, and MCP revision are Accepted decisions rather than open Phase 3 selections. Exact locked dependency versions and verification outcomes are implementation evidence, not founder product decisions.

## Gate 3 verification dispositions

| Question | Engineering evidence disposition | Evidence |
| --- | --- | --- |
| Exact dependency set | Frozen uv and pnpm graphs satisfy the accepted foundation stack; all groups/extras passed advisory and license inventory. | [Gate 3 evidence](gate-3-evidence.md) |
| Internal version authority | `pyproject.toml` `0.0.0.dev0` drives or is checked against every implemented product-version surface. | [Versioning](../releases/versioning.md) |
| Dependency direction | Import-linter plus AST architecture checks enforce inward domain/application and no sibling-adapter imports. | `TEST-ARCH-001` in [test strategy](../testing/test-strategy.md) |
| Browser-session inactivity | The accepted bounded contract remains unchanged; Gate 3 deliberately implements token primitives rather than a complete browser session. | [ADR 0011](../adr/0011-auth.md) and `G3-08` |
| Optional-dependency isolation | Default checks pass without Docker, PostgreSQL, Ollama, Rust, MCP, host-collector, or packaging modules; synthetic Docker/provider failure leaves authoritative state unchanged. | `TEST-ISO-001` and [Gate 3 evidence](gate-3-evidence.md) |

These engineering dispositions were accepted when Gate 3 passed on 2026-07-14 at exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](gate-3-evidence.md). Gate 4 sprint planning is authorized, but Gate 4 behavior remains prohibited until its proposed sprint brief receives founder acceptance.

## Proposed Gate 4 planning dispositions

The following delivery choices are **Proposed — pending founder acceptance** of the [Gate 4 sprint brief](gate-4-sprint-brief.md) at an exact revision. They are not Accepted decisions and do not authorize behavior while the brief remains Proposed.

| Planning topic | Proposed disposition if the brief is accepted | Remaining evidence or later owner | Status |
| --- | --- | --- | --- |
| Implementation base | Branch from integrated Gate 3 closure successor `461243541d6b63ddebf54598c6860ba73abcd012`, while `4adf1fb500b651e425735595db528fd42fffba73` remains the immutable approved Gate 3 engineering candidate. | Branch ancestry and clean-state evidence in `G4-00` | Proposed — pending founder acceptance |
| Acceptance scenarios | Advance only collector evidence for `AC-001`/`UAT-001` and runtime observations for `AC-003`/`UAT-003`; both complete at Gate 7. Make no Gate 4 `AC-007`/`UAT-007` claim. | Gate 6 conflict computation; Gate 7 founder-facing journeys | Proposed — pending founder acceptance |
| API and CLI subset | Limit REST to authenticated system status/capabilities, collectors/refresh, cursor-paginated observations, and events; limit CLI behavior to `status`, `ports`, and `collectors refresh`. | Later gates complete `SRS-API-001` and `SRS-CLI-001` | Proposed — pending founder acceptance |
| `SRS-COL-004` split | Gate 4 owns runtime intervals/manual refresh, Docker events, periodic reconciliation, last-good/degraded state, and events. | Gate 5 owns filesystem watcher, scanner debounce, scan cache, and project-scan behavior | Proposed — pending founder acceptance |
| Project association | Permit only nullable association-ready evidence from validated, redacted, source-attributed runtime or Docker metadata; never discover or assign a root, repository, project, checkout, worktree, or concrete `ProjectInstance` relationship. | Project/`ProjectInstance` discovery, identity resolution, and association are Gate 5 | Proposed — pending founder acceptance |
| Partial collector results | Atomically add or refresh verified positive facts, but never retire prior facts because they are absent from a partial result; only a complete comparable snapshot may mark prior facts stale. | Fault, restart, and reconciliation evidence in `G4-08`/`G4-14` | Proposed — pending founder acceptance |
| Conflict boundary | Emit affected resource/port keys and invalidation events only; do not compute, classify, persist, or display conflicts/exposure warnings. | Conflict and exposure behavior are Gate 6 | Proposed — pending founder acceptance |
| Real profiles | Require a documented real Apple-silicon macOS profile and at least one real Docker Engine API negotiation run, while core remains green with Docker absent. | `G4-11`, `G4-12`, and `G4-16` evidence | Proposed — pending founder acceptance |
| SSE replay duration | Preserve bounded `Last-Event-ID` plus resynchronization and use Gate 4 reconnect/restart measurements to lock the exact retention duration. | Gate 4 research result; material contract change requires ADR treatment | Proposed — pending founder acceptance |

## Research questions carried to later gates

- Gate 4: Does `psutil` expose sufficient macOS socket/process ownership fidelity for the supported OS, and where must `lsof -nP` validate or supplement it?
- Gates 4 and 7: What replay duration and resynchronization behavior give the simplest reliable SSE contract under real reconciliation and browser use?
- Gate 5: Which founder-approved corpus represents real project/parser diversity beyond the synthetic foundation fixtures?
- Gate 8: Which local model families and hardware envelopes can satisfy every conditional privacy, safety, schema, grounding, resource, and isolation gate?
- Gate 9: Which signed macOS artifact, service lifecycle, update/rollback path, and distribution mechanism meets clean-machine targets without persistent elevated privilege?

Gate 3 accepted the bounded packaging research evidence in `G3-20` only as input to Gate 9 hypotheses and experiments. It did not select or accept a release package.
