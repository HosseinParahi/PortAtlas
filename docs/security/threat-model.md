# Threat Model

Status: **Proposed pre-implementation security contract**
Review cadence: at every architecture gate and before each release candidate

## Security objectives

PortAtlas must preserve local confidentiality, integrity of authoritative reservations and leases, availability of the deterministic core, and truthfulness about evidence. It is a local application, but loopback traffic, project files, container metadata, model output, and same-user processes are not inherently trusted.

## Assets

- Reservation and lease state, revisions, and audit events
- Generated authentication material and browser sessions
- Project identities, checkout paths, parsed configuration evidence, process metadata, and container metadata
- User preferences, retention settings, backups, logs, and diagnostic exports
- Optional AI prompts, responses, and evaluation records
- The distinction between managed allocation assurance and unmanaged discovery evidence

## Trust boundaries

1. Browser or CLI to the loopback HTTP service
2. MCP client to STDIO server or authenticated loopback Streamable HTTP
3. Application services to SQLite or optional PostgreSQL repositories
4. Collectors to operating-system and Docker APIs
5. Scanner to untrusted project trees, files, and symlinks
6. Optional AI boundary from redacted context builder to Ollama and back
7. Export boundary from internal state to logs, backups, and diagnostic bundles

## Threat inventory

| ID | Surface and threat | Preventive controls | Detection and response | Release evidence |
|---|---|---|---|---|
| THR-001 | Malicious project file uses traversal, oversized input, encoding tricks, or parser ambiguity. | Root confinement, file type allowlist, byte/depth/count budgets, strict decoders, no evaluation, deterministic parsers. | Structured scan errors and adversarial fixture suite. | Scanner security tests pass. |
| THR-002 | Symlink escapes the selected `ProjectInstance` or creates a cycle. | Do not follow symlinks by default; canonicalize beneath root; track visited identities; reject escapes. | Record a redacted policy finding without reading the target. | Symlink escape and cycle tests pass. |
| THR-003 | Subprocess invocation permits shell injection or leaks environment data. | Prefer native APIs; fixed executable plus argument arrays; no shell; minimal environment; time and output limits. | Audit command identity and outcome, never raw sensitive arguments. | Negative metacharacter and timeout tests pass. |
| THR-004 | Environment parsing reads secrets while looking for port declarations. | Parse only allowlisted port-like keys; never persist unrelated values; redact before logs and responses. | Secret canaries in fixtures and output scans. | Zero canary leakage. |
| THR-005 | Docker socket access grants broader authority than intended. | Read-only SDK calls, no start/stop/remove/exec, explicit capability boundary, negotiated API version. | Surface degraded or permission-denied status without retry storms. | Docker authorization review and no-lifecycle contract tests pass. |
| THR-006 | Another local process calls loopback endpoints or steals a browser bootstrap token. | Generated high-entropy credentials, user-only file permissions, short single-use bootstrap, HttpOnly SameSite session, trusted-origin writes, CSRF defense. | Request IDs, bounded auth failure events, credential rotation. | Auth, origin, replay, and permissions tests pass. |
| THR-007 | DNS rebinding or hostile `Origin` reaches MCP Streamable HTTP. | Bind only loopback, validate `Origin`, authenticate every request, reject ambiguous host forwarding. | Security event without credential disclosure. | MCP transport conformance and negative-origin tests pass. |
| THR-008 | MCP client invokes a capability beyond its scope or confuses evidence with assurance. | Scoped credentials, explicit tool schemas, application-service authorization, managed/unmanaged labels in instructions and results. | Audit tool name, request ID, scope decision, and redacted resource identity. | Least-privilege and copy assertions pass. |
| THR-009 | Concurrent allocation or stale revision overwrites authoritative state. | Database transaction, uniqueness constraints, atomic leases, idempotency keys, optimistic concurrency. | Conflict response with current revision and request ID. | Race, retry, and crash tests pass. |
| THR-010 | AI prompt includes secrets or proprietary content beyond the user's intent. | Disabled by default, explicit scope preview, context minimization, redaction before provider call, local-only provider contract. | AI activity record stores categories and hashes rather than raw sensitive context. | Privacy canary suite passes. |
| THR-011 | Project text performs prompt injection or model output requests a dangerous action. | Treat project content as quoted untrusted data, fixed system policy, hard-limited read-only internal query allowlist, no MCP/external/mutating tools, strict output schema, semantic allowlist. | Reject and label unsafe or invalid output; deterministic core remains available. | Prompt-injection evaluation threshold passes. |
| THR-012 | Backup, log, or diagnostic export exposes secrets, paths, process arguments, or project contents. | Data minimization, field classification, mandatory redaction, preview, restrictive permissions, bounded retention. | Canary scanning and export manifest. | Export security suite reports zero leakage. |
| THR-013 | Corrupt backup or database produces silent loss or split authority. | Atomic snapshots, integrity metadata, schema version, restore-to-new-file workflow, migration transaction. | Integrity failure blocks replacement and preserves original. | Restore drill passes. |
| THR-014 | Collector, Docker, SSE, or Ollama outage blocks commands or corrupts state. | Separate failure domains, bounded queues and timeouts, last-known evidence labels, authoritative transactions independent of optional integrations. | Degraded health surfaced with freshness and recovery event. | Degradation E2E tests pass. |
| THR-015 | UI relies on color or inaccessible interactions, hiding security or conflict state. | Semantic roles, text/icon state, keyboard operation, visible focus, accessible names. | Automated accessibility scans plus manual keyboard and screen-reader UAT. | Accessibility gate passes. |
| THR-016 | PID reuse or a process exit race attributes a listener to the wrong owner. | Identify a process with PID plus start time and executable evidence, revalidate identity at reconciliation boundaries, and downgrade confidence when required fields are unavailable. | Conflicting or changed identity invalidates the association and records a safe permission/race limitation. | PID-reuse, rapid-exit, and permission-limited fixtures pass `UT-COL-001` and `UAT-001`. |

## Abuse cases that remain out of scope

- Defense against an operating-system administrator or an attacker who fully controls the user's account
- Network exposure beyond loopback
- Multi-tenant authorization
- Arbitrary plugin code execution
- Process termination, source patching, and managed launch in MVP

Out of scope does not mean safe to expose. Any future change to these boundaries requires an ADR and threat-model revision.

## Security gate

A release is blocked by an unmitigated high-exposure threat, a secret canary leak, an authorization bypass, non-atomic lease behavior, unsafe symlink traversal, or optional AI failure that affects deterministic authoritative state.
