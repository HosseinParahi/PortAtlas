# ADR 0010: Manifest

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Optional project-local port metadata

## Context

Projects need an optional, reviewable way to declare stable service names, preferred ports, protocols, environment keys, and policy intent. The dashboard must still discover and manage projects without a manifest. The repository is using PortAtlas only as a working title, so publishing a branded filename before name clearance would create migration and registry costs.

## Decision

Define a versioned YAML manifest with the working filename .portatlas.yaml:

- The file lives at a ProjectInstance root. Monorepo service entries use stable keys within that instance.
- A required top-level version field selects the schema. The initial schema version is integer 1.
- Project metadata is optional; service keys, protocol, preferred port, environment key, bind intent, and stable-or-temporary policy are declarative data.
- The schema never contains secret values, credentials, arbitrary commands, shell fragments, model prompts, or permission grants.
- YAML is parsed with a safe data-only loader.
- Publish a JSON Schema for editor and UI validation after the name gate.
- Unknown fields are rejected within a known schema version. A newer version receives a clear unsupported-version error and is not partially applied.
- The UI can preview, generate, validate, import, and export the manifest. Writing it requires an explicit user-approved diff.
- Central configuration and deterministic scanners remain fully functional when the file is absent.
- Manifest evidence is declared state, not proof that a service is listening.
- Worktree-specific files may intentionally differ; shared Project policy supplies inherited defaults.

The .portatlas.yaml filename is accepted only as an internal working filename. It must not be advertised, registered as an ecosystem convention, or promised as stable until ADR 0023 accepts the public name. A pre-release rename may change the filename without an alias.

## Alternatives considered

### .devports.yaml

The name is product-neutral and descriptive but could imply a broader external standard that does not yet exist.

### portatlas.yaml without a leading dot

This is more visible but adds a branded top-level file to every repository and is equally dependent on name clearance.

### Embed configuration in package manifests

pyproject.toml or package.json would be natural for some stacks but excludes other languages and creates multiple schema homes.

### Central database only

Central state avoids repository files but cannot be reviewed, shared, or versioned with project changes.

### Infer everything

Discovery is essential but cannot represent user policy, preferred assignments, or intentional stability reliably.

## Consequences

### Positive

- Teams can review non-secret port intent with code.
- The schema is stack-neutral and versioned.
- Worktrees can carry distinct desired state.
- The product remains useful without adding repository files.

### Costs and risks

- YAML parsing and schema evolution require security and compatibility tests.
- A working-title change can rename the file before release.
- Declared intent can become stale and must be reconciled with observations.
- Strict unknown-field handling requires coordinated schema upgrades.

## Verification

- Validate accepted, malformed, unknown-field, duplicate-key, unsupported-version, and oversized manifests.
- Prove the loader cannot construct arbitrary objects or execute tags.
- Round-trip UI generation through the published schema without changing meaning.
- Confirm no secret value, arbitrary command, or permission field is accepted.
- Show manifest provenance and confidence separately from runtime evidence.
- Verify the product completes core workflows with no manifest present.
- Block schema publication and branded documentation while ADR 0023 remains unresolved.

## Revisit triggers

- ADR 0023 selects a different public name.
- Schema version 2 needs behavior that cannot be represented compatibly.
- User research prefers an unbranded ecosystem-neutral filename.
- A major language ecosystem establishes a safer canonical configuration location.

## Sources

- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
