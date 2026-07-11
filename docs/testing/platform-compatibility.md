# Platform Compatibility Plan

Status: **Proposed pre-implementation contract**

## Support tiers

| Tier | Platform | MVP commitment |
|---|---|---|
| Supported | macOS on Apple silicon, one local OS user | Install, collect, scan, allocate, UI, CLI, MCP, backup, restore, and uninstall acceptance |
| Contract | Linux | Domain, collector, path, process, service, and packaging interfaces remain explicit; fixture contracts run where practical |
| Contract | Windows | Domain, path, process, socket, service, and packaging interfaces remain explicit; no MVP runtime support claim |
| Optional profile | PostgreSQL | Repository contract compatibility, not a required local service |
| Optional integration | Docker | Supported when reachable and authorized; absence must degrade cleanly |
| Conditional integration | Ollama | No core dependency; inclusion only after AI gates pass |

Exact supported macOS patch releases and CPU baselines are selected during Phase 3 and reverified before release. The checkpoint machine snapshot is research evidence, not the compatibility matrix.

## Adapter contracts

Platform-specific code must sit behind interfaces for listener enumeration, process identity, path canonicalization, user-only file permissions, service lifecycle, browser bootstrap, and packaging. Domain services accept normalized values and typed errors, not raw platform objects.

## Test matrix

- Supported macOS: clean install, standard and permission-restricted user cases, sleep/wake, service restart, IPv4/IPv6, TCP/UDP, process churn, filesystem variants, and uninstall.
- Filesystem: case sensitivity assumptions, unicode normalization, spaces, long paths, symlinks, deleted worktrees, and removable-volume loss.
- Browser: current stable Safari, Chrome, and Firefox lines chosen at release time; keyboard, zoom, reduced motion, narrow viewport, and session behavior.
- Contract platforms: serialize identical normalized fixtures and pass shared domain/repository/API contracts without claiming native collector completion.
- Optional profiles: clean absence, permission denial, version negotiation, restart, timeout, cancellation, and recovery.

## Compatibility rule

Unsupported environments receive clear messages and never trigger silent fallback to unsafe privileges or an unverified collector. Platform-specific deviations require an ADR or a documented compatibility exception with tests.
