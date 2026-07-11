# PortAtlas Allocator Design

## Scope

The allocator selects explainable candidates and performs concurrency-safe registry reservations and leases. The MVP is registry-only:

- it does not bind an operating-system socket;
- it does not patch project files;
- it does not inject environment variables;
- it does not launch or supervise services;
- it does not prevent unmanaged processes from ignoring PortAtlas.

Atomicity is guaranteed among cooperating PortAtlas operations, not across every process on the workstation.

## Inputs

AllocationRequest contains:

- ProjectInstance ID;
- Service ID or stable service key;
- protocol;
- requested bind scope;
- preferred port or ranges;
- service category;
- stable or temporary intent;
- reservation or lease mode;
- lease duration when applicable;
- fresh-preflight requirement;
- idempotency key;
- Principal and scopes.

EffectivePortPolicy adds:

- global and scoped allowed ranges;
- forbidden and reserved-system ranges;
- configured ephemeral ranges;
- project and service-category ranges;
- preferred ports;
- interface exposure rules;
- worktree behavior;
- reuse and stability policy;
- lease duration bounds.

OccupancyView contains current observations, reservations, unexpired leases, relevant declarations, and policy exclusions with freshness.

## Port identity and overlap

Allocation evaluates protocol and bind scope, not port number alone.

- TCP and UDP are independent unless policy intentionally couples them.
- Container-internal ports do not occupy host ports.
- A host wildcard binding can overlap loopback or interface-specific bindings.
- IPv4 and IPv6 wildcard overlap depends on platform behavior and socket options.
- Unknown dual-stack semantics are evaluated conservatively.

The allocator delegates overlap rules to the same BindOverlap service used by the conflict engine.

## Candidate ordering

Candidate order is deterministic:

1. preserve an existing valid reservation for the same ProjectInstance and Service;
2. use an explicit preferred port when policy permits;
3. consider ProjectInstance and project-specific preferred ranges;
4. consider service-category ranges;
5. consider global allowed ranges;
6. within each range, choose a stable preference seed;
7. probe candidates deterministically with wraparound;
8. exclude occupied, forbidden, ephemeral, exposure-invalid, or policy-invalid candidates.

The preference seed is a versioned hash of stable project identity, ProjectInstance identity according to worktree policy, service key, protocol, and allocator strategy version. The hash is a preference, not a security mechanism.

Changing allocator strategy requires a versioned policy and migration behavior so existing valid reservations remain stable.

## Availability classification

| Classification | Meaning |
| --- | --- |
| unavailable | Active observation, reservation, or lease blocks the candidate |
| policy_forbidden | Effective policy excludes the candidate |
| declared_conflict | Another ProjectInstance declares the candidate and policy treats it as blocking |
| uncertain | Collector freshness or bind semantics are insufficient |
| available_unreserved | No current registry blocker; external race remains |
| reserved | Persistent assignment committed |
| leased | Expiring atomic assignment committed |

A suggestion returns available_unreserved. It does not occupy the port.

## Transaction algorithm

~~~mermaid
flowchart TD
    V[Validate request and scopes]
    F{Fresh preflight required?}
    R[Request bounded reconciliation]
    B[Begin database write transaction]
    I[Resolve effective policy and occupancy]
    C[Build deterministic candidate order]
    N{Candidate available?}
    X[Insert reservation or lease]
    A[Append audit and outbox]
    K[Commit]
    E[Return allocation and rationale]
    Z[Return typed exhaustion or conflict]

    V --> F
    F -->|yes| R
    F -->|no| B
    R --> B
    B --> I
    I --> C
    C --> N
    N -->|yes| X
    X --> A
    A --> K
    K --> E
    N -->|no candidates| Z
    N -->|next| N
~~~

Final occupancy and insertion occur inside one transaction. A preflight outside the transaction improves freshness but does not eliminate an external bind race.

### SQLite

The repository begins a short write transaction before final candidate evaluation. BEGIN IMMEDIATE or an equivalent adapter mechanism serializes competing writers. A unique active-allocation key prevents duplicate cooperative occupancy. Busy handling is bounded; on exhaustion the command returns a retryable persistence error without a partial reservation.

### PostgreSQL

The repository uses a transaction with row, advisory, or allocation-domain locking plus an active-allocation uniqueness constraint. Lock ordering is stable to avoid deadlocks. The same concurrency contract is verified against both adapters.

## Reservation behavior

A PortReservation is persistent until release or configured expiry. Creation response includes:

- reservation ID and revision;
- ProjectInstance and Service;
- PortKey and bind scope;
- effective policy provenance;
- selection rationale;
- current relevant evidence;
- request ID;
- explicit unmanaged-process warning.

An external observation on a reserved port creates a conflict; it does not silently delete or move the reservation.

## Lease behavior

A PortLease has:

- lease ID and owner Principal;
- creation and expiration;
- policy-bounded renewal;
- status;
- idempotency identity;
- revision.

Lease expiry is evaluated transactionally. Cleanup changes status and emits events; it does not assume that a service stopped. Renew requires ownership or administrative scope and cannot exceed policy maximum.

## Idempotency

Acquire and reserve require an idempotency key for API and MCP automation. Replaying the same normalized request returns the original allocation. Reusing a key with different content fails. A client timeout after commit therefore cannot cause a second allocation.

## Exhaustion response

When no candidate exists, return:

- searched ranges and counts;
- exclusion counts by reason;
- blocking conflict IDs and safe resource IDs;
- policy provenance;
- freshness;
- whether widening range or refreshing evidence could help;
- no fabricated suggestion.

The response does not list secret-bearing process arguments or paths outside caller scope.

## Selection explanation

An explanation is deterministic structured data:

~~~json
{
  "strategy_version": 1,
  "selected_port": 4310,
  "reasons": [
    "inside service-category range",
    "stable preference for this ProjectInstance and Service",
    "no blocking registry record"
  ],
  "freshness": {
    "host_observations_at": "2026-07-11T00:00:00Z"
  },
  "assurance": "cooperative_registry_only"
}
~~~

AI may paraphrase this response but cannot alter it.

## Worktree policy

ProjectInstances are separate allocation owners. Effective policy decides whether worktrees:

- receive independent stable ports;
- share a project reservation only when they cannot run concurrently;
- draw from a dedicated worktree range.

The default favors independent ProjectInstance allocations because worktrees can run simultaneously.

## Preflight

Preflight checks:

- collector freshness and limitations;
- current observations;
- declarations in the ProjectInstance;
- reservations and leases;
- effective policies;
- bind exposure;
- current conflicts.

It returns a point-in-time assessment. It never claims that a later unmanaged launch is safe without a fresh recheck and cooperative lease.

## Future managed-run contract

A future managed runner may:

1. acquire a lease;
2. inject an approved environment key;
3. launch a requested command;
4. verify the actual listener;
5. convert the assignment;
6. release on exit.

This requires a separate process-control threat model, signal-handling design, command allowlist, and approval gate. The MVP allocator exposes no launch hook.

## Tests

- deterministic candidate order;
- preservation of valid prior assignment;
- protocol separation;
- wildcard and dual-stack overlap;
- container namespace separation;
- range boundaries and exclusions;
- ephemeral-range avoidance;
- worktree isolation;
- concurrent lease uniqueness on SQLite and PostgreSQL;
- idempotent retry;
- lease expiry and renewal;
- stale observation uncertainty;
- external observation violating a reservation;
- exhaustion explanation;
- property tests over ranges and concurrent requests.
