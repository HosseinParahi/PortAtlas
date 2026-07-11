# Security Policy

## Supported versions

There are no released or supported versions yet. This repository is a pre-implementation specification and documentation baseline.

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, tokens, private repository contents, personal paths, or sensitive diagnostic data.

Use GitHub private vulnerability reporting for this repository when that channel is available. If it is unavailable, open a minimal public coordination issue that contains no sensitive detail and asks a maintainer to establish a private channel. A maintainer will acknowledge a complete report, assess severity and scope, coordinate remediation, and publish an advisory when users need to act.

## Scope expectations

Future reports may cover host and Docker collection, project scanning, symlink handling, local HTTP authentication, MCP transports, subprocess boundaries, environment parsing, backups, logs, diagnostic bundles, and optional local-AI processing. The accepted security contracts are indexed under [docs/security](docs/security/threat-model.md).

The project does not promise a bounty or response-time service level. Good-faith research that avoids privacy violations, data destruction, persistence, and service disruption is welcome.
