# ADR 0007: Packaging

- **Status:** Proposed
- **Date:** 2026-07-11
- **Scope:** macOS MVP installation and native-service lifecycle

## Context

Normal users must not need to clone the repository, install Python, or manage a development environment. The package must install, start, stop, upgrade, roll back, back up, and uninstall the native service and built browser UI. macOS code signing, notarization, Apple Silicon and Intel artifacts, LaunchAgent behavior, data preservation, and release naming all affect the final choice.

PyInstaller is the leading way to bundle the Python service, but an architecture choice is not enough evidence for a release package. ADR 0023 also blocks publishing artifacts under the working title.

## Decision

Use a PyInstaller-packaged native service as the primary packaging research path:

- Prototype one-folder bundles first because their contents and import failures are easier to inspect.
- Bundle the compiled React assets with the service and ship the CLI against the same application.
- Evaluate a user LaunchAgent as an explicit setup option, not an invisible privileged daemon.
- Keep application data, configuration, credentials, logs, and backups outside the replaceable application bundle in platform-appropriate user directories.
- Build separately on each supported macOS architecture or produce a validated universal distribution.
- Research signing, notarization, reproducible builds, SBOM generation, upgrade, rollback, backup, uninstall, and stale-process recovery before accepting a release mechanism.
- Evaluate Homebrew distribution only after the standalone artifact and service lifecycle are reliable.
- Defer the Tauri shell to Version 1; it is not part of MVP packaging acceptance.
- Do not publish package names, bundle identifiers, formulae, casks, or installer branding until ADR 0023 is accepted.

This is a research direction. A later ADR must accept the exact artifact layout, installer, service manager, signing identity, update channel, and rollback mechanism.

## Alternatives considered

### Tauri shell with a Python sidecar

This offers a native application surface but adds a second lifecycle, sidecar signing, update coordination, and desktop-shell security work.

### Python wheel only

A wheel suits developers but requires a Python runtime and does not solve service lifecycle or ordinary-user installation.

### Container image

A container is useful for development and limited inspection but cannot be the primary package because host visibility and Docker-optional operation are requirements.

### PyInstaller one-file bundle immediately

One file appears simple, but extraction, startup, crash cleanup, diagnostics, and code-signing behavior should be evaluated only after a one-folder package works.

## Consequences

### Positive

- The leading path preserves the accepted native-service architecture.
- Users need not install Python.
- Tauri complexity does not block core delivery.
- Explicit research gates prevent an untested installer from becoming an irreversible commitment.

### Costs and risks

- PyInstaller output is platform-specific and can miss dynamic imports or data files.
- macOS signing, notarization, LaunchAgent installation, and upgrades remain unresolved.
- Supporting two CPU architectures expands build and release testing.
- Homebrew policy may constrain service and dependency layout.

## Verification

The packaging ADR can move to Accepted only after evidence demonstrates:

- Installation on clean supported macOS virtual machines for each target architecture.
- Signed and notarized artifacts that pass Gatekeeper.
- Start, stop, restart, status, logs, login behavior, crash recovery, and stale PID handling.
- Upgrade and rollback with database migration recovery and preserved user data.
- Complete uninstall with an explicit choice to retain or remove data.
- No dependency on a system Python, Node, Docker, or a repository checkout.
- SBOM, checksums, provenance, license notices, and redacted diagnostics.
- A measured comparison of one-folder, one-file, LaunchAgent, and Homebrew delivery paths.

## Revisit triggers

- PyInstaller cannot meet signing, lifecycle, size, startup, or supportability requirements.
- Tauri becomes an approved MVP requirement.
- Homebrew rejects the required package or service design.
- Apple platform policy changes affect unsigned local services or LaunchAgents.
- The working title changes, requiring artifact and bundle-identifier updates.

## Sources

- [PyInstaller operating model](https://pyinstaller.org/en/stable/operating-mode.html)
- [PyInstaller usage and platform notes](https://pyinstaller.org/en/stable/usage.html)
- [Apple launchd documentation](https://developer.apple.com/documentation/xpc/launchd)
- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Tauri sidecar documentation](https://v2.tauri.app/develop/sidecar/)
