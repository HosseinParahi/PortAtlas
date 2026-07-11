# Open Questions

These questions are intentionally unresolved inputs. None may be answered by inventing founder identity, credentials, namespaces, or release state.

## Founder decisions required before engineering or release gates

| ID | Question | Why it matters | Needed by | Default while open |
|---|---|---|---|---|
| OQ-001 | Is the Gate 2 documentation baseline approved without changes? | Phase 3 implementation is blocked on acceptance. | Gate 3 start | Stop at Gate 2 |
| OQ-002 | Which replacement-name candidates should receive professional clearance if `PortAtlas` is not usable? | Current searches found domain and software-related trademark collisions. | Before public namespace creation | Use working title internally only |
| OQ-003 | What public signing identity and release email should artifacts use? | Packages and signed releases need verifiable ownership. | Packaging gate | Do not generate identities |
| OQ-004 | Which package, image, MCP, Homebrew, and domain namespaces are founder-approved after clearance? | Namespace squatting and accidental publication are irreversible external actions. | Public release | Publish nothing |
| OQ-005 | Which sponsorship platform and active handle should be advertised? | Funding metadata must point to a real account. | Funding configuration | Omit funding file |
| OQ-006 | What quantitative parser corpus represents the founder's real projects? | Recall and precision targets require labeled ground truth. | Scanner acceptance | Use synthetic fixtures plus founder-selected sample later |
| OQ-007 | What target inventory capacity is representative beyond the baseline test envelope? | Performance thresholds should match real local estates. | Performance gate | Test documented baseline and report scaling curve |
| OQ-008 | Is optional PostgreSQL intended only for compatibility or for a supported multi-process profile? | Support level affects migrations and operations. | Persistence implementation | Compatibility profile only |
| OQ-009 | Should browser sessions expire on service restart or survive within a bounded duration? | Affects usability, token rotation, and local threat surface. | Authentication implementation | Short bounded session, invalidated on credential rotation |
| OQ-010 | Which local model families and hardware envelopes should AI evaluation cover? | Inclusion must be based on reproducible performance, safety, and privacy evidence. | AI evaluation | No model is endorsed or required |

## Research questions owned by Phase 3

- Which Python web stack satisfies SSE, typed validation, secure cookies, and packaging constraints with the smallest supported surface?
- Which SQLAlchemy and migration versions support Python 3.14 and both storage profiles at lock time?
- Does `psutil` expose sufficient macOS socket/process ownership fidelity for the target OS, and where must `lsof -nP` validate or supplement it?
- What signed macOS service and packaging path achieves the installation-time target without elevated persistent privileges?
- What replay duration and resynchronization behavior give the simplest reliable SSE contract?
