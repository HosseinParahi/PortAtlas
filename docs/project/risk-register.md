# Risk Register

Scores use likelihood and impact from 1 (low) to 5 (high). Exposure is their product before mitigation.

| ID | Risk | L | I | Exposure | Mitigation and evidence | Owner | Gate |
|---|---|---:|---:|---:|---|---|---|
| RSK-001 | Working-name collision causes legal, registry, or trust problems. | 4 | 5 | 20 | Block all public namespaces; complete professional trademark and registry clearance; retain rename plan. | Founder | Public release |
| RSK-002 | UI language overstates control of unmanaged processes or ports. | 3 | 5 | 15 | Enforce managed/unmanaged copy in requirements, API schemas, MCP instructions, UAT, and validator review. | Product | Every release |
| RSK-003 | Race between observation and allocation creates a port conflict. | 4 | 4 | 16 | Atomic registry leases, explicit confidence, reconciliation, and no guarantee outside managed allocation. | Allocator | Gate 5 |
| RSK-004 | Project scanning leaks secrets or follows hostile symlinks. | 3 | 5 | 15 | Safe path policy, size and depth limits, allowlisted parsers, redaction before persistence or output, adversarial fixtures. | Security | Gate 4 |
| RSK-005 | Localhost services are treated as inherently trusted. | 3 | 5 | 15 | Loopback-only binding, origin validation, generated credentials, secure browser exchange, scoped tokens, negative tests. | Security | Gate 4 |
| RSK-006 | Docker socket access expands host authority. | 3 | 5 | 15 | Read-only API usage, capability isolation, no lifecycle commands, surfaced permission warning, clean degradation. | Docker | Gate 4 |
| RSK-007 | Parser false negatives undermine inventory confidence. | 4 | 4 | 16 | Per-parser fixtures, provenance, unsupported-pattern reporting, recall metric on a labeled corpus, manual evidence paths. | Scanning | Gate 4 |
| RSK-008 | Parser false positives create noisy conflicts. | 3 | 3 | 9 | Typed evidence, confidence, value validation, context-specific extraction, precision threshold. | Scanning | Gate 4 |
| RSK-009 | SQLite concurrency or corruption breaks authoritative leases. | 2 | 5 | 10 | WAL and transaction research, crash-injection tests, backups, integrity checks, repository contracts. | Data | Gate 5 |
| RSK-010 | SSE loss or reordering leaves browser state stale. | 3 | 3 | 9 | Event IDs, revisions, replay window, reconnect invalidation, visible freshness, polling recovery. | API | Gate 4 |
| RSK-011 | Optional AI ingests sensitive context or follows injected project text. | 3 | 5 | 15 | Explicit opt-in, minimized redacted context, untrusted-content framing, schema validation, non-authoritative output, kill switch. | AI | Gate 6 |
| RSK-012 | AI or Docker outage corrupts or blocks core state. | 2 | 5 | 10 | Separate failure domains and queues; authoritative writes never depend on either integration; degradation E2E tests. | Architecture | Gate 5 |
| RSK-013 | Package or platform versions drift before implementation. | 4 | 2 | 8 | Reverify primary sources and lock exact versions during Gate 3. | Engineering | Gate 3 |
| RSK-014 | Packaging or macOS permission behavior makes installation slow or fragile. | 3 | 4 | 12 | Prototype signed installation and service lifecycle early; measure clean-machine time. | Release | Gate 5 |
| RSK-015 | Diagnostics or logs expose paths, arguments, environment data, or tokens. | 3 | 5 | 15 | Structured redaction, safe defaults, export preview, secret canaries, retention controls, security tests. | Operations | Gate 5 |
| RSK-016 | Accessibility regressions block keyboard or assistive-technology users. | 3 | 4 | 12 | Radix primitives, semantic tables, focus tests, non-color indicators, automated and manual accessibility gates. | UI | Gate 5 |

## Escalation rule

An exposure of 15 or more is release-blocking until mitigation evidence reduces likelihood or impact, or the founder explicitly accepts the residual risk in writing.
