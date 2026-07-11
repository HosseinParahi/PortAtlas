# PortAtlas Project Manifest Schema

## Status and naming gate

.portatlas.yaml is the proposed working filename for design and internal fixtures. It is not a published compatibility promise until repository, package-registry, domain, and trademark or name-collision research is completed and the naming ADR is approved.

The central dashboard works without a manifest. A manifest is an optional, project-local declaration of stable project identity, services, preferred ports, and policy hints. It cannot grant scan scope, weaken host security, or authorize mutation.

## Design goals

- Human-readable YAML with a published strict schema.
- Versioned from the first release.
- Safe to parse without executing code.
- No credentials or environment values.
- ProjectInstance-aware behavior for worktrees.
- Clear distinction between preference, reservation, and runtime fact.
- Round-trip generation and validation through UI and CLI.

## Version 1 draft

~~~yaml
version: 1

project:
  id: visual-labs
  name: VisualLabs
  description: Local visual production workspace

instance:
  allocation_scope: independent

services:
  web:
    name: Web
    category: frontend
    protocol: tcp
    preferred_port: 3100
    bind: loopback
    environment_key: PORT
    stability: stable

  api:
    name: API
    category: api
    protocol: tcp
    preferred_range:
      start: 8100
      end: 8199
    bind: loopback
    environment_key: API_PORT
    stability: stable

  postgres:
    name: PostgreSQL
    category: database
    protocol: tcp
    preferred_port: 5432
    bind: loopback
    stability: stable

policy:
  forbidden_ports:
    - 3000
  require_loopback:
    - database
    - admin
~~~

## Root object

| Field | Required | Contract |
| --- | --- | --- |
| version | yes | Integer schema version; exactly 1 for this draft |
| project | yes | Stable logical project metadata |
| instance | no | Worktree and allocation behavior |
| services | yes | Map keyed by stable service key |
| policy | no | Project-scoped policy hints subject to central policy |
| metadata | no | Bounded extension metadata under published keys |

Unknown root fields are rejected. YAML duplicate keys, anchors exceeding limits, unsafe tags, and excessive nesting are rejected.

## project

### id

Required stable slug:

- 1 through 64 characters;
- lowercase ASCII letter or digit start and end;
- interior lowercase letters, digits, hyphens, and underscores;
- stable across path rename;
- unique only within the local PortAtlas registry unless a future namespace contract says otherwise.

The manifest ID is strong identity evidence but does not automatically merge an existing unrelated Project. A collision requires explicit user resolution.

### name

Required user-facing name, 1 through 120 Unicode characters after normalization. It is never an identity key.

### description

Optional safe project description, maximum 500 characters. It can be eligible for future local AI context only with project consent.

## instance

### allocation_scope

- independent: each ProjectInstance or worktree receives its own stable allocation;
- shared: instances express a preference to reuse the logical project assignment;
- policy: central effective policy decides.

The default is independent because worktrees may run simultaneously. Central policy can reject unsafe shared behavior.

An optional instance key may be supplied through local override, not committed shared manifest, when a developer needs a stable workstation-specific label.

## services

Service key follows the project ID slug character rules and is unique in the map.

| Field | Required | Allowed |
| --- | --- | --- |
| name | no | Safe display string |
| category | yes | frontend, api, database, cache, queue, worker, admin, proxy, storage, tooling, other |
| protocol | yes | tcp or udp |
| preferred_port | conditional | Integer 1 through 65535 |
| preferred_range | conditional | Inclusive start and end |
| bind | no | loopback, any, or policy; default policy |
| environment_key | no | Safe key name only, never value |
| stability | no | stable or temporary; default stable |
| container_port | no | Internal container port, explicitly not host occupancy |
| description | no | Safe bounded text |

Exactly one of preferred_port or preferred_range may be present for one protocol entry. A service requiring multiple ports uses a ports list form:

~~~yaml
services:
  minio:
    category: storage
    ports:
      - name: api
        protocol: tcp
        preferred_port: 9000
        bind: loopback
      - name: console
        protocol: tcp
        preferred_port: 9001
        bind: loopback
~~~

The single-port shorthand and ports list cannot be combined.

## policy

Project manifest policy is a constrained hint layer. It may define:

- allowed_ranges;
- preferred_ranges by service category;
- forbidden_ports;
- require_loopback categories;
- default_lease_seconds within central maximum;
- worktree allocation preference.

It cannot:

- widen a central forbidden range;
- enable non-loopback service binding;
- approve a filesystem root;
- change authentication or MCP scopes;
- enable process control or file patching;
- enable Docker mutation;
- enable AI, model download, or data retention;
- override secret handling.

Central policy wins on conflict and reports provenance.

## Environment keys

environment_key is an identifier telling a future managed workflow how a service normally receives a port. It contains no value and grants no permission to edit an environment file. The registry-only MVP uses it for explanation and plan generation only.

Valid keys use an uppercase environment identifier pattern and a bounded length. Secret-like keys are rejected even if syntactically valid.

## Semantics

- preferred_port is a declaration or allocation preference, not a reservation.
- A valid manifest does not prove a listener exists.
- The scanner emits PortDeclarations with user-authored exact evidence.
- The allocator considers preferences only after central policy.
- A committed PortReservation or PortLease remains central registry state.
- An external process can ignore the manifest and registry.

## Validation flow

1. Enforce approved-root path containment.
2. Enforce file size and YAML resource limits.
3. Parse with a safe YAML loader.
4. Reject duplicate and unknown fields.
5. Validate version and scalar types.
6. Validate service keys and mutually exclusive fields.
7. Validate port ranges and central security floors.
8. Emit safe diagnostics with structured pointers.
9. Produce Project, ProjectInstance, Service, PortDeclaration, and DiscoveryEvidence candidates.
10. Require user resolution for identity collisions.

Validation never interpolates environment values, executes tags, imports code, or follows manifest-specified paths.

## Error examples

| Condition | Code |
| --- | --- |
| Unsupported version | MANIFEST_VERSION_UNSUPPORTED |
| Duplicate YAML key | MANIFEST_DUPLICATE_KEY |
| Unknown field | MANIFEST_UNKNOWN_FIELD |
| Invalid service key | MANIFEST_SERVICE_KEY_INVALID |
| Port and range both supplied | MANIFEST_PORT_CHOICE_INVALID |
| Central policy conflict | MANIFEST_POLICY_REJECTED |
| Identity collision | MANIFEST_IDENTITY_CONFLICT |
| Secret-like field or value | MANIFEST_SECRET_FORBIDDEN |

Messages include a safe structured pointer and line when available, never the full source line.

## Schema publication

After the name gate, the selected filename and JSON Schema URI are recorded in an ADR. The schema is distributed in the manifest-schema package, published with checksums, and used by backend, CLI, editor integration, fixtures, and documentation. A version 1 file remains valid throughout the major-version compatibility window.

## Migration

Future schema versions require:

- explicit version discriminator;
- deterministic migration preview;
- no silent rewrite;
- preservation of comments only when the chosen YAML tooling proves it;
- backup before write;
- a user-approved apply step;
- downgrade or rollback guidance.

## Security

The manifest is untrusted repository content. It cannot contain executable hooks, shell commands, arbitrary file includes, remote URLs to fetch, plugin code, credentials, token scopes, or model instructions. Descriptions are data and are delimited as untrusted if sent to optional AI.
