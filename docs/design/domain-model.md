# PortAtlas Domain Model

## Modeling principles

- Observed, declared, reserved, leased, desired, conflicted, stale, ignored, and unknown are distinct states.
- Runtime evidence is authoritative only for its collection time and permission scope.
- AI output is advisory and never promotes itself into authoritative state.
- ProjectInstance, not an absolute path and not a logical Project alone, is the operational ownership boundary.
- Protocol, address family, bind address, and host/container namespace are part of port meaning.
- Every inferred association carries evidence and confidence.

## Aggregate map

~~~mermaid
classDiagram
    class ProjectRoot {
      root_id
      canonical_path
      scan_policy
      state
      revision
    }
    class Project {
      project_id
      display_name
      repository_identity
      manifest_identity
    }
    class ProjectInstance {
      instance_id
      project_id
      root_id
      canonical_path
      worktree_identity
      lifecycle_state
      revision
    }
    class Service {
      service_id
      instance_id
      key
      category
    }
    class PortObservation {
      observation_id
      port_key
      process_identity_id
      container_identity_id
      observed_at
      freshness
    }
    class PortDeclaration {
      declaration_id
      service_id
      port_key
      role
      confidence
      evidence_id
    }
    class PortReservation {
      reservation_id
      service_id
      port_key
      status
      revision
    }
    class PortLease {
      lease_id
      service_id
      port_key
      expires_at
      status
      revision
    }
    class Conflict {
      conflict_id
      code
      severity
      fingerprint
      status
      revision
    }
    ProjectRoot "1" --> "*" ProjectInstance
    Project "1" --> "*" ProjectInstance
    ProjectInstance "1" --> "*" Service
    Service "1" --> "*" PortDeclaration
    Service "1" --> "*" PortReservation
    Service "1" --> "*" PortLease
    Conflict "*" --> "*" PortObservation
    Conflict "*" --> "*" PortDeclaration
    Conflict "*" --> "*" PortReservation
    Conflict "*" --> "*" PortLease
~~~

## Identity model

### ProjectRoot

A user-approved scanning boundary. It owns traversal policy, include and exclude rules, symlink handling, tags, pause state, and revision. Removal stops future scanning; retention policy determines whether discovered ProjectInstances are archived or removed.

Invariants:

- canonical path is absolute;
- canonical path is accessible to the current user at approval time;
- every scanned path resolves inside the boundary under the selected symlink policy;
- changing scope requires explicit user action and an audit event.

### Project

A logical project family. It may represent a repository, monorepo, or manually grouped application. Project identity can use a user manifest ID, local generated identity, Git common repository evidence, and configured remote hints. A network lookup is never required.

Invariants:

- absolute path is not the sole identity;
- remote URL is evidence, not a mandatory key;
- multiple ProjectInstances may refer to one Project;
- logical-project metadata cannot silently merge two user-separated projects.

### ProjectInstance

A concrete checkout, Git worktree, monorepo package boundary, or standalone directory. This is the unit that can be scanned, started externally, assigned ports, and associated with runtime evidence.

Invariants:

- belongs to one ProjectRoot while active;
- belongs to one Project;
- canonical path is unique among active instances on a host;
- worktrees of one Project have distinct instance IDs;
- path relocation updates evidence when identity reconciliation is strong enough; otherwise a user-confirmed link is required.

Lifecycle: discovered, active, paused, inaccessible, archived, removed.

### Service

A logical runnable component inside a ProjectInstance, such as web, api, postgres, worker, or storybook. A stable service key is unique within an instance.

## Runtime identities

### ProcessIdentity

ProcessIdentity is PID plus process start time and executable identity. PID alone is insufficient because operating systems reuse it. Optional fields include user, parent identity, redacted command metadata, and permitted current working directory evidence.

### ContainerIdentity

ContainerIdentity includes Docker container ID, name, image, compose project, compose service, networks, labels selected by allowlist, start time, health, restart policy, internal ports, and published bindings.

### PortObservation

A factual socket observation:

- PortKey;
- socket state;
- ProcessIdentity or ContainerIdentity reference when known;
- collector source and version;
- observed_at and last_seen_at;
- snapshot scope;
- permission limitations;
- association evidence to ProjectInstance and Service;
- freshness state.

Observations are not rewritten into declarations or reservations.

## Declared and desired state

### PortDeclaration

A supported configuration source references a port. Required fields:

- ProjectInstance and optional Service;
- PortKey or a partially known key;
- role: host_bind, container_internal, connect_target, framework_default, or unknown;
- value source and safe location;
- parser ID and version;
- confidence;
- DiscoveryEvidence;
- detected_at and source fingerprint;
- confirmation state.

Container-internal ports do not collide with host listeners unless a published host binding exists.

### DesiredPortAssignment

A proposal inside a reviewable change plan. Desired state can influence explanation but never occupies a registry slot. It becomes a reservation or declaration only through the corresponding deterministic command.

### DiscoveryEvidence

Evidence records parser or collector provenance without secret-bearing content:

- evidence ID and kind;
- source path relative to approved root where possible;
- safe line and column or structured pointer;
- parser or collector version;
- source fingerprint;
- confidence rationale;
- redaction indicators;
- observed or scanned time.

## Registry state

### PortReservation

A persistent cooperative assignment to a ProjectInstance and Service. It may be active, released, expired by policy, or stale. A reservation has an owner Principal, rationale, policy snapshot, creation time, optional expiration, and revision.

### PortLease

A short-lived atomic cooperative allocation. State transitions:

~~~mermaid
stateDiagram-v2
    [*] --> active
    active --> renewed: authorized renewal
    renewed --> renewed: authorized renewal
    active --> released: explicit release
    renewed --> released: explicit release
    active --> expired: expires_at reached
    renewed --> expired: expires_at reached
    active --> violated: conflicting observation
    renewed --> violated: conflicting observation
    violated --> released: explicit release
    violated --> expired: expires_at reached
    released --> [*]
    expired --> [*]
~~~

A violated lease remains evidence that a cooperating allocation lost a race to an unmanaged process.

### PortPolicy

Policy may be global, ProjectRoot, Project, ProjectInstance, Service, or category scoped. More specific policy overrides only fields declared overrideable. Effective policy contains:

- allowed and preferred ranges;
- forbidden and ephemeral ranges;
- protocol;
- bind exposure requirements;
- stability preference;
- conflict severities;
- lease duration and renewal bounds;
- reuse and worktree behavior.

Policy evaluation returns both value and provenance.

### ScanRule

A versioned built-in or user-defined focused discovery rule. It names eligible file patterns, parser identity, parser version, resource budgets, enabled scope, and confidence mapping. A ScanRule cannot execute a command, import project code, widen an approved ProjectRoot, or bypass the scanner security policy. Built-in rules are signed with the installed application version; user rules are limited to a reviewed declarative rule language.

### HealthCheck

A future-compatible descriptor for HTTP, TCP, command, or custom checks associated with a Service. The MVP may store a supported parser hint but does not execute arbitrary command checks. HealthCheck remains separate from PortObservation: a listening socket does not prove application health, and a failed health check does not prove the listener disappeared.

### IntegrationClient

A configured Codex, Claude, CLI, IDE, or generic MCP client. It owns client identity, transport, enabled state, scopes, ProjectRoot or ProjectInstance boundaries, token metadata, and last-use time. It never stores a raw bearer token and cannot derive permissions from repository content.

### AuditEvent

An append-only record of a meaningful configuration, scan, registry, integration, permission, or AI action. It contains Principal, action, target resource, outcome, request ID, revisions, timestamp, and bounded safe metadata. It excludes raw credentials, environment values, full source lines, complete process arguments, and model prompts.

## Conflict aggregate

Conflict is a normalized finding with:

- stable fingerprint;
- machine-readable code;
- severity;
- status: open, acknowledged, ignored, resolved, or reopened;
- affected record references;
- evidence references;
- human explanation template data;
- recommended action descriptors;
- automated-safety classification;
- suppression reason and expiry;
- first_seen_at, last_seen_at, resolved_at;
- revision and audit history.

A conflict is derived from deterministic records and policy. It cannot be authored by AI.

## Optional AI domain records

### AIProviderProfile

Provider type, loopback endpoint, selected model names, enabled capabilities, privacy controls, request deadline, maximum concurrency, keep-alive, retention, and revision. Provider credentials, if ever required, live in secret storage.

### AIContextRecord

Metadata describing task type, project scope, evidence IDs, category counts, redaction counts, byte and token estimates, provider profile, creation time, and retention decision. Raw prompt and source snippets are absent by default.

### AIAssistanceResult

Contains task type, provider and model identity, schema version, evidence references, generated indicator, confidence where defined, validation status, user-confirmation state, created time, expiration, and redacted structured result.

Status is always advisory, AI suggested, or user confirmed. User confirmation can create a separate deterministic domain command; it never mutates this record into a runtime fact.

## State classification rules

| UI state | Source | Meaning |
| --- | --- | --- |
| Observed | PortObservation | Listener seen in a successful collector snapshot |
| Declared | PortDeclaration | Supported configuration references a port |
| Reserved | PortReservation | PortAtlas registry assignment exists |
| Leased | PortLease | Unexpired atomic cooperative allocation exists |
| Desired | DesiredPortAssignment | Reviewable proposal exists |
| Conflicted | Conflict | Deterministic incompatibility exists |
| Stale | Freshness or conflict lifecycle | Evidence no longer current under retention policy |
| Unknown | Explicit uncertainty | Permission or evidence is insufficient |
| Ignored | Suppression | User suppressed a finding with reason and expiry |

These labels always include text or an icon and never rely only on color.

## Cross-aggregate invariants

- An active reservation or lease references an active ProjectInstance and valid Service.
- A lease expiration is greater than creation and within policy maximum.
- A PortKey is valid before persistence.
- One active allocation cannot overlap another blocking allocation in the same allocation domain.
- Source reconciliation cannot delete records outside its completed scope.
- A conflict fingerprint is deterministic for the same rule and affected record identities.
- An audit event and outbox event accompany every meaningful mutation.
- Secret material is not a domain field.
- AI-derived output cannot satisfy evidence required by runtime, allocation, or conflict invariants.
