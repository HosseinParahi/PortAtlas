# Security Policy

## Supported versions

There are no released or supported versions yet. The repository contains a private engineering foundation, but no installable product, public package, or supported runtime inventory exists.

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, tokens, private repository contents, personal paths, or sensitive diagnostic data.

Use GitHub private vulnerability reporting for this repository when that channel is available. If it is unavailable, open a minimal public coordination issue that contains no sensitive detail and asks a maintainer to establish a private channel. A maintainer will acknowledge a complete report, assess severity and scope, coordinate remediation, and publish an advisory when users need to act.

## Scope expectations

Current reports may cover the foundation's local HTTP shell, strict configuration, token primitives, persistence seam, dependency workflow, fixtures, and build tooling. Later reports may cover host and Docker collection, project scanning, symlink handling, complete authentication flows, MCP transports, subprocess boundaries, environment parsing, backups, logs, diagnostic bundles, and optional local-AI processing. The accepted security contracts are indexed under [docs/security](docs/security/threat-model.md).

The project does not promise a bounty or response-time service level. Good-faith research that avoids privacy violations, data destruction, persistence, and service disruption is welcome.

## Foundation dependency policy

The foundation accepted with Gate 3 at exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](docs/project/gate-3-evidence.md) uses committed uv and pnpm locks. CI rejects metadata/lock drift, reviews pull-request dependency changes, audits the complete Python lock including development, build-backend, optional-integration, PostgreSQL, and packaging profiles, and audits Node production and development dependencies. The Gate 3 disposition accepted these bounded foundation controls; it did not approve a release security review, runtime inventory, or later-gate behavior. A known advisory from either audit blocks a future candidate unless an explicit security disposition is recorded; no silent ignore list is permitted.

License inventory covers the same complete dependency scope. AGPL and SSPL findings fail the automated Python and Node reviews pending explicit compatibility review. PyInstaller reports GPLv2 with its bootloader exception; it is retained only in the non-default research group and receives a separate Gate 9 review if packaging work selects it. Every license remains subject to human review before a release; a Gate 3 inventory is not a release SBOM or NOTICE file.

Dependabot monitors the supported uv and GitHub Actions ecosystems. The current GitHub support table does not yet list pnpm 11, so Node upgrades remain deliberate locked changes with dependency review and full checks rather than an unverified automated updater.
