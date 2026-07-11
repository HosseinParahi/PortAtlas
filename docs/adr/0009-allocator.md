# ADR 0009: Allocator

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Port suggestion, reservation, and lease concurrency

## Context

A safe suggestion must respect active listeners, declarations, reservations, leases, service policy, excluded and ephemeral ranges, protocol, bind scope, and stable preferences. Two PortAtlas clients may allocate concurrently. An unmanaged process can still bind a port after any check, so the allocator must state exactly which races it controls.

## Decision

Use deterministic policy-aware probing backed by atomic database leases:

1. Accept a typed request containing ProjectInstance, service key, protocol, bind scope, requested stability, and applicable policy.
2. Preserve an existing assignment when it remains valid.
3. Construct allowed candidate ranges after removing privileged, forbidden, administrator-reserved, and configured ephemeral ranges.
4. Use a stable hash of opaque project-instance identity, service key, protocol, bind scope, and policy version as the preference seed. The hash is a placement hint, not a security mechanism.
5. Probe candidates deterministically from that seed.
6. Reject candidates conflicting with current observations, reservations, leases, policy, or higher-confidence declarations.
7. Treat TCP and UDP independently. For the MVP, treat the same protocol and port on different interfaces conservatively as conflicting unless an explicit policy and platform test prove the binding combination safe; wildcard binds conflict with every address of that family.
8. In one repository transaction, expire eligible leases, re-evaluate persistent conflicts, and insert a unique short-lived lease. SQLite uses an immediate write transaction; other repositories provide equivalent serialization.
9. Return the lease ID, expiry, selected port, evaluated policy, rejected candidates, evidence timestamp, and explanation.
10. Recheck runtime state immediately before an integrated launch, then verify the actual listener after launch.

Lease acquisition is atomic among cooperating PortAtlas clients. It is not an operating-system socket reservation and does not guarantee prevention for unmanaged external launches.

Renewal and release are idempotent, scoped to the owning credential and ProjectInstance, and audited. Expired leases never silently become persistent reservations.

## Alternatives considered

### First available port

Linear first-fit is simple but causes unrelated projects to converge on the same low ports and provides poor assignment stability.

### Random selection

Random choice spreads allocations but is hard to explain, reproduce, and keep stable.

### Hash directly to one port

A single hash target is stable but fails poorly when occupied and still needs deterministic collision handling.

### Bind a placeholder socket

Holding a socket can close part of the OS race, but transferring it to arbitrary child frameworks is not portable. It may be evaluated for managed launch profiles without replacing database leases.

### In-memory locking

An in-process mutex does not coordinate separate CLI, HTTP, or MCP processes and loses state on restart.

## Consequences

### Positive

- Cooperating clients receive distinct atomic leases.
- Stable services tend to retain predictable ports.
- Every choice has a deterministic explanation.
- Policies and runtime evidence remain authoritative over the hash preference.

### Costs and risks

- Conservative interface handling can reject technically compatible bindings.
- SQLite transactions must remain short under contention.
- Observation freshness affects unmanaged-race risk.
- Expiry depends on careful clock and restart handling.

## Verification

- Run concurrent property-based tests that request from overlapping ranges and prove no active lease key duplicates.
- Test policy precedence, stable repeatability, range exhaustion, expired leases, renewal, idempotent release, and database restart.
- Cover TCP versus UDP, IPv4 versus IPv6, loopback, wildcard, and specific-interface cases on real macOS.
- Start an unmanaged process during allocation and verify PortAtlas reports the race rather than claiming prevention.
- For managed launches, recheck before start and verify the child listened on the assigned port.
- Compare SQLite and PostgreSQL repository behavior under the same allocation contract.

## Revisit triggers

- Managed launch needs a portable socket-handoff mechanism.
- Platform testing supports less conservative interface coexistence.
- Measured transaction contention violates latency targets.
- Team/server mode requires distributed coordination.
- Operating-system ephemeral-range behavior changes on a supported platform.

## Sources

- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)
- [SQLite isolation](https://www.sqlite.org/isolation.html)
- [IANA service-name and port-number procedures, RFC 6335](https://www.rfc-editor.org/rfc/rfc6335)
