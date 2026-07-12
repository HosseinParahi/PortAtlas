# Assumptions Register

Assumptions are hypotheses to validate, not hidden requirements. Each item has an owner and a decision point.

| ID | Assumption | Evidence or rationale | Validation method | Owner | Decision point | Status |
|---|---|---|---|---|---|---|
| ASM-001 | The intentionally empty local and remote repository was the correct starting point. | Founder requested and approved the four-commit first-history documentation baseline. | Exact Gate 2 approval and provenance record. | Founder | Gate 2 | Validated at `e53f399` |
| ASM-002 | One local macOS user is a sufficient MVP operating boundary. | Founder locked macOS and one OS user for MVP. | Founder UAT on a clean supported macOS account. | Product | Gate 4 | Accepted |
| ASM-003 | Linux and Windows can remain adapter contracts without MVP runtime support. | Cross-platform domain boundaries reduce future coupling while keeping MVP focused. | Architecture review plus fixture-based adapter contract tests. | Architecture | Gate 3 | Accepted |
| ASM-004 | SQLite is sufficient for local authoritative state at target capacity. | Single-user, local-first workload and transactional leases fit embedded storage. | Performance and concurrency tests at documented limits. | Data | Gate 5 | Open validation |
| ASM-005 | PostgreSQL compatibility can be maintained without becoming a required local service. | Repository interfaces isolate dialects and core tests must run offline. | Shared repository contract suite against both profiles. | Data | Gate 4 | Accepted |
| ASM-006 | Host socket evidence plus project and Docker evidence can provide useful provenance despite observation races. | Multiple independent evidence sources improve confidence but cannot guarantee unmanaged state. | Fixture recall, live reconciliation, and stale-evidence UAT. | Collection | Gate 4 | Open validation |
| ASM-007 | The focused parser set covers the founder's initial project estate. | Parser list was explicitly locked for MVP. | Curated corpus plus founder project sample review. | Scanning | Gate 4 | Open validation |
| ASM-008 | Server-Sent Events are sufficient for one-way browser freshness. | Commands remain REST; the browser needs server-to-client invalidation rather than bidirectional messaging. | Reconnect, replay, ordering, and two-second refresh tests. | API | Gate 4 | Accepted |
| ASM-009 | A generated local token and browser bootstrap exchange can provide usable local authentication. | The browser cannot safely retain a long-lived bearer credential. | Threat review, permissions test, cookie and origin E2E tests. | Security | Gate 4 | Open validation |
| ASM-010 | Optional Ollama value can be evaluated without weakening deterministic core behavior. | AI is isolated, last, and non-authoritative. | All AI release gates and failure-isolation tests must pass. | AI | Gate 6 | Conditional |
| ASM-011 | Exact engineering dependency versions can be locked during Gate 3 without becoming public release or end-user compatibility promises. | Gate 2 recorded dated research; Gate 3 adds machine-readable pins and frozen locks, while Gate 9 revalidates the release candidate. | Reverify primary sources, install only from committed locks, run license/security checks, and compare clean CI versions. | Engineering | Gates 3 and 9 | Candidate-local validated; hosted confirmation and Gate 9 revalidation pending |
| ASM-012 | A different public name may be required. | Existing domain and trademark uses create meaningful collision risk. | Professional clearance and namespace inventory. | Founder | Before public release | Open |

## Rules

- An assumption becoming false triggers impact analysis across requirements, ADRs, tests, and release gates.
- A validated assumption should be converted into evidence or an accepted decision.
- No assumption overrides an explicit locked decision.
