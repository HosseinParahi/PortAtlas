# Versioning Policy

Status: **Proposed pre-implementation policy**

## Current truth

No PortAtlas product version, public tag, package version, compatibility promise, or released artifact exists at this checkpoint. PortAtlas is a working title and cannot be used for public namespace publication until [ADR 0023](../adr/0023-working-name-collision-trademark-clearance.md) is accepted.

This policy becomes operational only after Gate 3 establishes the version source and release tooling. It does not claim any version command, tag command, package command, or publication command works.

## Product version model

Use [Semantic Versioning 2.0.0](https://semver.org/) for the product release:

- **MAJOR** changes indicate incompatible supported public contracts after 1.0.
- **MINOR** changes add backward-compatible behavior after 1.0.
- **PATCH** changes contain backward-compatible fixes after 1.0.
- Before 1.0, use 0.MINOR.PATCH. A 0.MINOR release may include an intentional breaking contract change only with migration guidance, explicit release notes, and founder approval.
- A 0.PATCH release remains backward compatible with the corresponding 0.MINOR contract.

The first public version is chosen in the Gate 9 release record. Architecture approval does not assign it.

## Pre-release identifiers

Use Semantic Versioning pre-release identifiers to express evidence maturity:

| Identifier | Meaning |
| --- | --- |
| alpha | Incomplete implementation intended for controlled development evaluation |
| beta | Feature-complete candidate with unresolved verification or compatibility evidence |
| rc | Release candidate with frozen scope and artifacts undergoing final Gate 9 review |

Pre-release artifacts are not stable releases. No pre-release artifact may be publicly branded or published while the public-name gate is open.

Build metadata may identify a source revision or build attempt, but it does not change precedence and must not be used to replace immutable artifact hashes.

## Version authorities

Gate 3 selects one machine-readable product-version source. Generated surfaces must agree with it:

- native service and package metadata;
- CLI version output;
- browser About and diagnostic views;
- REST system metadata and OpenAPI information;
- MCP server implementation metadata;
- package and installer metadata;
- SBOM, provenance, release notes, and artifact names.

The release process compares every surface and blocks mismatches.

## Independently versioned contracts

Product version does not replace schema or protocol versions:

| Contract | Version rule |
| --- | --- |
| REST API | Major path such as /api/v1 changes only for an incompatible API contract; additive changes remain documented |
| SSE events | Explicit event-schema version; clients refetch on unsupported or reset events |
| MCP | Report both product version and reviewed MCP protocol revision; the approved baseline is 2025-11-25 |
| Database | Alembic revision graph; every product release records supported upgrade and rollback boundaries |
| Local configuration | Explicit schema version with migration and backup |
| Project manifest | Explicit schema version; the working .portatlas.yaml filename is not public until name clearance |
| Import and export | Format version independent of product version and validated before state changes |
| AI structured results | Task-specific schema version plus provider, model, and evidence metadata |
| Plugin contract | No public plugin compatibility promise in the MVP |

## Compatibility rules

A change is breaking when a supported client, stored state, documented workflow, or automation must change to keep working. Examples include:

- removing or changing a REST, SSE, CLI, or MCP field or semantic;
- changing allocation, conflict, or managed/unmanaged assurance semantics;
- invalidating existing configuration, manifest, backup, or export without migration;
- changing credential scope or permission defaults;
- broadening network, telemetry, Docker, scan-root, mutation, or AI authority;
- dropping a supported platform, architecture, or package lifecycle;
- changing public names or identifiers after they are declared stable.

Security tightening that rejects unsafe prior behavior is documented prominently and may require a breaking release when clients must change.

## Database and configuration compatibility

- Every release records the oldest directly upgradable schema and the supported rollback boundary.
- Upgrade takes a verified backup before migration.
- A failed migration preserves the prior executable and data or produces a tested recovery path.
- Downgrade is never implied; it is supported only when the release evidence explicitly proves it.
- Imports from newer unsupported formats fail safely and do not partially mutate state.
- AI-derived data remains deletable and cannot block deterministic-state migration.

## Conditional AI and version identity

AI inclusion does not create a separate product version:

- A release states whether AI is absent, available but disabled by default, or included for explicit activation.
- Core compatibility never depends on Ollama, a model download, a model digest, or network access.
- Provider and recommended-model compatibility are recorded in a separate tested matrix.
- Changing a recommendation alone does not change deterministic core semantics.
- Expanding AI tools, persistence, remote providers, or mutation authority requires ADR and security review before release-version classification.

## Telemetry and version checks

The application does not contact a remote service merely to report or discover its version. No usage ping, automatic analytics event, or telemetry record is authorized. Any future update-check mechanism requires separate network, privacy, authenticity, and opt-in review.

## License, sponsorship, and version access

Every released version remains under Apache-2.0 unless a later governance decision lawfully changes future project-owned releases. Apache-2.0 permits commercial use without payment to the maintainers. Sponsorship is voluntary and does not unlock versions, updates, security fixes, commercial permission, support eligibility, or release evidence.

## Release immutability

- A published version identifies one exact source revision and one approved artifact set per platform.
- Artifacts are identified by cryptographic hash and are never silently replaced.
- A correction produces a new version.
- Withdrawn artifacts retain an advisory explaining the reason and safe replacement.
- Release notes record migrations, security impact, known limitations, AI state, managed/unmanaged assurance, and evidence links.

## Version evidence

Before Gate 9 approval, record:

- chosen product version and classification rationale;
- source revision and version-authority value;
- every generated version surface;
- database, configuration, API, SSE, MCP, manifest, import/export, and AI schema versions;
- supported upgrade and rollback boundaries;
- artifact, SBOM, and provenance hashes;
- compatibility and migration test IDs;
- public-name approval, license review, and founder disposition.

## Related documents

- [Release process](release-process.md)
- [MVP checklist](mvp-checklist.md)
- [API design](../design/api-design.md)
- [MCP design](../design/mcp-design.md)
- [Configuration schema](../design/configuration-schema.md)
- [Project manifest schema](../design/project-manifest-schema.md)
