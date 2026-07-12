# Local Installation Contract

Status: **Proposed Gate 9 release workflow; no installable artifact exists**

## User outcome

A first-time user on supported macOS should reach an authenticated dashboard in under five minutes without editing code, supplying a cloud account, running Docker, installing Ollama, or granting persistent administrator access.

## Proposed stages

1. Verify platform, architecture, available disk, and supported browser.
2. Verify artifact signature, checksum, version, and public-name approval.
3. Install the native Python service bundle and browser assets into a user-scoped location.
4. Generate local authentication material with user-only permissions.
5. Start the loopback-only service and perform a one-time browser bootstrap exchange.
6. Show privacy, no-telemetry, project-scan consent, and optional-integration choices.
7. Confirm collector health, an empty or discovered inventory, and documentation access.

No step may publish a port beyond loopback, send telemetry, install a model, enable Docker access, register a project root, or change source files without explicit user action.

## Packaging research gate

Gate 3 performs only the bounded `G3-20` packaging feasibility/research spike described in the [Gate 3 sprint brief](../project/gate-3-sprint-brief.md#evidence-bound-work-items). It may refine hypotheses, risks, and the experiment plan; it does not produce a distributable bundle or accept a package mechanism.

Gate 9 owns PyInstaller or equivalent bundle implementation, background-service lifecycle, browser launch/bootstrap integration, signing, notarization, update/rollback safety, complete uninstall, clean-machine measurements, and packaging ADR acceptance. Tauri remains a Version 1 option rather than an MVP prerequisite.

## Upgrade and rollback contract

An upgrade verifies the artifact, takes a safe backup, checks schema compatibility, migrates transactionally, starts the new service, and validates health before declaring success. A failed migration preserves the prior data and executable. Rollback support and downgrade limits are versioned release facts, not implied.

## Uninstall contract

Uninstall stops the user service and removes installed application files. It asks separately before removing PortAtlas state, backups, or diagnostics and never deletes registered project sources, Docker resources, Ollama models, or global toolchains.

## Acceptance evidence

Release evidence includes three timed clean installs, signature verification, user-only credential permissions, loopback binding, offline operation, upgrade and failure rollback, backup/restore, and residue inspection after uninstall.
