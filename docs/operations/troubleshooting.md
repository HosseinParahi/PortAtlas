# Troubleshooting Contract

Status: **Proposed diagnostic taxonomy; commands are added only after implementation**

## Safety rules

Start with visible health, request IDs, freshness, and redacted diagnostics. Do not ask users to disable authentication, bind publicly, expose the Docker socket broadly, run the service as an administrator, post raw environment files, or delete a database as a first response.

| Symptom | Likely categories | Safe first checks | Escalation evidence |
|---|---|---|---|
| Dashboard cannot connect | Service stopped, bootstrap expired, port changed, session invalid | Confirm local service health and loopback address; restart through supported lifecycle; retry a fresh one-time bootstrap | Redacted health and request ID |
| Authentication rejected | Expired/reused bootstrap, rotated credential, wrong audience or scope | Use supported credential rotation or new bootstrap; verify user-only permissions | Outcome category, credential identifier only |
| Inventory empty | True empty state, collector denied, unsupported platform, stale scan | Inspect collector health and freshness; distinguish unavailable from zero results | Collector status, safe counts, timestamps |
| Runtime change not visible | Collector delay, event disconnect, revision gap | Check freshness and SSE reconnect state; request full resynchronization | Event IDs, revisions, timing, no payload secrets |
| Project scan incomplete | Unsupported syntax, budget exceeded, symlink policy, permission denial | Inspect per-parser findings and safe errors; compare labeled fixture | Parser type, relative evidence location, error code |
| Docker missing | Daemon absent, permission denied, incompatible API | Leave core running; verify Docker is optional and inspect negotiated health | Safe API version and error category |
| Reservation conflict | Existing managed lease, unmanaged listener, exclusion, stale revision | Open conflict provenance; refresh; retry with idempotency and current revision | Resource IDs and evidence types |
| Database problem | Integrity failure, disk full, migration interrupted, permissions | Stop writes through supported lifecycle; preserve files; run read-only integrity diagnosis | Schema version, integrity category, free-space range |
| High CPU or memory | Scan loop, event backlog, optional provider, oversized estate | Cancel bounded work; disable optional integration; inspect queue and capacity counters | Redacted local metrics and operation IDs |
| Optional AI unavailable | Disabled, provider absent, model missing, timeout, invalid output | Confirm feature gate and loopback provider health; keep deterministic workflow | Provider category, model identifier, timing, validation error |

## Error handling

All user-facing failures map to stable error codes, a request ID, safe explanation, and an action that does not weaken security. Repeated transient failure uses bounded backoff and a circuit breaker. An unavailable optional integration never masquerades as authoritative empty data.

## Support handoff

Before sharing a diagnostic bundle, inspect its manifest and preview. Remove project display paths if they are not necessary. Use the private path in [SECURITY.md](../../SECURITY.md) for suspected vulnerabilities.
