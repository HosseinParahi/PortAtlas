# PortAtlas Conflict Engine

## Purpose

The conflict engine converts normalized registry records and effective policy into deterministic, first-class findings. It is the only authority for conflict classification. AI-generated prose may explain an existing finding but cannot create, change severity, suppress, or resolve one.

## Inputs

- current and stale PortObservations;
- PortDeclarations;
- PortReservations;
- PortLeases;
- DesiredPortAssignments for advisory plan checks;
- ProjectInstance and Service identity;
- effective PortPolicy;
- collector and scanner freshness;
- platform bind-semantics profile;
- prior Conflict state and suppression.

## Evaluation key

Rules index records by:

- host identity;
- namespace;
- protocol;
- port;
- address family;
- bind address and normalized bind scope.

Candidate pairs are reduced through this key before bind-overlap evaluation. The engine does not compare every record to every other record.

## Bind-overlap semantics

~~~mermaid
flowchart TD
    P{Same protocol?}
    N{Same namespace and host?}
    O{Same port?}
    A[Evaluate address and wildcard overlap]
    D{Platform semantics known?}
    C[Conflict candidate]
    U[Uncertain overlap finding]
    X[No socket collision]

    P -->|no| X
    P -->|yes| N
    N -->|no| X
    N -->|yes| O
    O -->|no| X
    O -->|yes| A
    A --> D
    D -->|known overlap| C
    D -->|unknown or permission limited| U
    D -->|disjoint| X
~~~

Rules preserve:

- TCP versus UDP;
- host versus container namespace;
- wildcard versus loopback or interface-specific binds;
- IPv4 versus IPv6 and dual-stack platform behavior;
- Docker published host binding versus container-internal port.

Conservative uncertainty is not mislabeled as a confirmed collision.

## Required rule catalog

| Code | Condition | Default severity |
| --- | --- | --- |
| ACTIVE_DECLARATION_COLLISION | Observation overlaps a declaration owned by another intended service | high |
| ACTIVE_RESERVATION_COLLISION | Observation overlaps a reservation without matching ownership evidence | high |
| DECLARATION_DECLARATION_COLLISION | Two runnable ProjectInstances declare overlapping host ports | medium |
| RESERVATION_RESERVATION_COLLISION | Two persistent reservations overlap | high |
| LEASE_OBSERVATION_COLLISION | New observation overlaps active lease without matching launch evidence | critical |
| DOCKER_NATIVE_COLLISION | Docker host publication overlaps native process | high |
| BIND_SCOPE_AMBIGUOUS | Address or dual-stack facts make apparent collision uncertain | low |
| WILDCARD_SHADOWS_SPECIFIC | Wildcard bind overlaps loopback or interface-specific intent | high |
| IPV4_IPV6_DUAL_STACK_COLLISION | Platform dual-stack behavior produces overlap | high |
| POLICY_VIOLATION | Assignment violates effective policy | configured |
| FORBIDDEN_OR_EPHEMERAL_PORT | Port is forbidden or in avoided ephemeral range | medium |
| UNEXPECTED_NETWORK_EXPOSURE | Service binds beyond allowed loopback scope | high; critical for protected categories |
| CONTAINER_PORT_NOT_HOST_PORT | Apparent conflict incorrectly compares only internal container namespace | informational correction |
| STALE_RESERVATION | Reservation lacks current project evidence under retention policy | low |
| STALE_DECLARATION | Declaration source is stale or inaccessible | low |
| UNKNOWN_OWNER | Active observation lacks process or container owner | medium |
| PERMISSION_LIMITED_OBSERVATION | Permissions prevent reliable ownership or absence conclusion | low |

Severity can be increased by service category, exposure, policy, and active impact. It cannot be reduced below a configured security floor without explicit policy.

## Ownership-aware matching

An observation can satisfy an expected declaration or reservation when evidence strongly connects:

- the same ProjectInstance and Service;
- matching process working directory or executable evidence;
- matching Docker compose project and service;
- matching managed-run correlation in a future version;
- explicit user confirmation.

Matching does not erase the individual records. It changes the relationship from conflict to fulfilled or associated.

## Finding fingerprint

A stable fingerprint is a versioned hash of:

- rule code and rule version;
- normalized PortKey or policy key;
- sorted affected resource types and IDs;
- relevant policy scope.

Timestamps, display names, paths, and evidence ordering are excluded so a continuing finding retains identity across refreshes. Rule-version changes may intentionally create a new fingerprint with migration handling.

## Evaluation output

ConflictProjection contains:

- fingerprint;
- code and rule version;
- severity;
- affected record references and roles;
- evidence IDs;
- explanation parameter map;
- recommended action descriptors;
- automated-safety classification;
- freshness and uncertainty;
- first-seen hint from prior finding.

Human text is rendered from versioned templates. It is not the machine contract.

## Lifecycle

~~~mermaid
stateDiagram-v2
    [*] --> open
    open --> acknowledged: user acknowledges
    open --> ignored: reason and expiry
    acknowledged --> ignored: reason and expiry
    ignored --> open: suppression expires
    ignored --> resolved: underlying conflict disappears
    open --> resolved: underlying conflict disappears
    acknowledged --> resolved: underlying conflict disappears
    resolved --> reopened: same fingerprint returns
    reopened --> ignored: reason and expiry
    reopened --> resolved: underlying conflict disappears
~~~

Resolution requires fresh enough evidence for every rule input. A collector failure or partial scan cannot resolve a finding that depends on absence.

## Incremental recomputation

Application services submit affected evaluation keys after:

- collector reconciliation;
- scan reconciliation;
- reservation or lease mutation;
- lease expiry;
- policy update;
- ProjectInstance lifecycle change;
- suppression change.

The engine loads current records for those keys, evaluates all applicable rules, and diffs projections against stored findings in the same transaction.

## Recommendations

Recommendations are deterministic descriptors, for example:

- refresh runtime evidence;
- inspect owner evidence;
- reserve an allocator suggestion;
- change bind scope to loopback;
- release a stale reservation;
- confirm or ignore a declaration;
- create a reviewable port-change plan;
- perform manual process action outside PortAtlas.

Each descriptor includes required permission, risk, whether a dry run exists, and affected resources. The MVP never marks process termination or arbitrary file edits safe for automatic execution.

## Suppression

Ignore requires:

- conflict ID and expected revision;
- reason from a safe bounded field;
- optional expiry, with policy maximum;
- Principal and audit record.

Suppression does not delete evidence. Critical security exposure may remain visible in system summaries even when acknowledged, according to policy.

## AI boundary

AI explanation receives the immutable conflict projection, safe evidence summaries, effective policy, and deterministic alternatives. Validation requires every referenced owner, port, project, and evidence ID to exist in supplied context. The generated result is separately labeled and may fail without affecting Conflict.

## Failure behavior

| Failure | Behavior |
| --- | --- |
| Rule evaluation exception | Roll back affected recomputation; preserve prior findings; mark engine degraded |
| Unknown platform bind behavior | Produce uncertainty finding, not confirmed collision |
| Stale collector or scanner scope | Preserve finding and expose staleness |
| Missing referenced evidence | Reject projection and report invariant error |
| Policy invalid | Do not apply policy; use last valid revision and surface configuration error |
| Suppression expired | Reopen on next deterministic evaluation |

## Test strategy

- table-driven tests for every rule;
- IPv4, IPv6, wildcard, loopback, and interface matrices;
- TCP and UDP separation;
- Docker internal versus published host ports;
- same-service fulfillment versus other-service collision;
- declaration confidence and stale evidence;
- deterministic fingerprints and member-order independence;
- severity policy floors;
- suppression expiry and reopening;
- incremental results equivalent to full recomputation;
- property test for conflict symmetry where applicable;
- proof that AI records cannot enter rule inputs.
