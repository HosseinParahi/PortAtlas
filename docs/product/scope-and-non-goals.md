# PortAtlas Scope and Non-goals

## Scope rule

The MVP focuses on local development port intelligence and coordination. A capability belongs in the MVP only when it improves trustworthy observation, project declaration discovery, conflict reasoning, safe allocation/reservation, local human use, or permissioned agent use without turning PortAtlas into a broader system-management platform.

## MVP scope

### Runtime and state

- macOS-first TCP and UDP listener inventory with IPv4/IPv6 and interface awareness.
- Process identity using PID plus start time, executable, safely redacted command metadata, user, and project association where permitted.
- Docker running/stopped containers, Compose identity, internal/exposed/published ports, interface bindings, and status.
- Periodic and event-driven reconciliation, manual refresh, file watchers, debounce, last-known-good snapshots, and visible degradation.
- Independent observed, declared, reserved, leased, desired, conflicted, stale, unknown, and ignored state.

### Projects and configuration discovery

- UI-managed approved roots with preview, tags, recursion, inclusion/exclusion, symlink policy, pause/rescan, progress, and permission errors.
- One logical `Project` for repository identity and one or more concrete `ProjectInstance` records for each checkout/worktree; the instance is the scan, runtime-association, policy, reservation, and allocation boundary. Monorepo services remain children of the relevant instance.
- Exactly these isolated, fixture-tested MVP parsers: Compose; Dockerfile `EXPOSE`; safe `.env*` port keys; `package.json` scripts/workspaces; Vite, Next, Nuxt, and SvelteKit; Python launcher commands and `pyproject.toml`; Tauri configuration; Makefile, Taskfile, Procfile, and justfile.
- Data-driven service defaults as hints, never authoritative listeners.
- Evidence, source location, parser, timestamp, and exact/high/medium/low/user-confirmed confidence.

### Coordination

- Configurable global/project/service port policies and ranges.
- Deterministic explained suggestions, persistent manual reservations, release, and atomic short-lived leases.
- Current and future conflict types across observations, declarations, reservations, leases, protocols, interfaces, Docker/native state, exposure, policy, and staleness.
- Severity, machine code, human explanation, evidence, safe recommendations, audit, and reasoned suppression.
- Central operation without a manifest. The proposed `.portatlas.yaml` schema remains a design-only future contract, outside the locked MVP parser catalog and unpublished until the working-name gate closes.

### Interfaces and operations

- Accessible setup wizard, dashboard, ports, projects, conflicts, reservations, activity, integrations, settings, help, fuzzy search, and command palette.
- Local versioned REST API and Server-Sent Events.
- MVP CLI command contract.
- MCP STDIO and authenticated loopback streamable HTTP, typed tools/resources/prompts, Codex-first setup, and client-neutral guidance.
- Read-only default plus explicitly scoped reservation/lease and PortAtlas-configuration mutations; audit trail, non-secret import/export, backup/restore/migration/reset, and synthetic demo mode.
- Automated unit, property, fixture, integration, E2E, security, accessibility, performance, and UAT coverage.
- macOS packaging plus install/start/stop/status/log/upgrade/rollback/backup/uninstall documentation and verification.
- Open-source README, contribution, security, governance, support, release, issue/PR, changelog, and dependency foundations.

### Conditional MVP scope: local AI

Ollama may ship in MVP only if disabled by default and every AI release gate passes. Allowed scope is provider/model discovery, capability test, read-only natural-language inventory, grounded conflict explanations, project summaries, strict redaction/structured validation, bounded execution, generated labels, local audit metadata, and full failure isolation. Core behavior and release readiness cannot depend on it.

## Version 1 planning scope

- Linux and Windows implementations.
- Tauri shell, menu bar/tray experience, or alternative desktop packaging.
- Managed launch profiles and `portatlas run` with environment injection and post-launch verification.
- Source-change planning, patch generation, and narrowly allowlisted patch application.
- Health checks, stale-service heuristics, notifications, history/trends, one-click open, and launcher/tmux hooks.
- Richer Git metadata for the accepted `Project`/`ProjectInstance` model.
- Shell completions, templates/presets, pluggable collectors/scanners, development proxy adapters, devcontainer scanning, VS Code task/launch scanning, generic shell/proxy adapters, stable `.localhost` aliases, and PostgreSQL team/server profile.
- Opt-in local embeddings/semantic search, AI fallback scanning, manifest proposals, correction memory, and model benchmarking profiles.

These boundaries are locked outside MVP; later promotion requires a new post-MVP scope and security review.

## Future scope

- Kubernetes and local clusters.
- Remote machine agents and multi-machine dashboards.
- Team-shared registry or cloud synchronization.
- IDE extensions and mobile clients.
- Full process supervisor.
- Automatic proxy, DNS, and certificate management.
- Network packet inspection.
- Remote AI providers or repository fine-tuning.

## Explicit MVP non-goals

PortAtlas is not:

- A Portainer replacement, Docker orchestrator, or Kubernetes dashboard.
- A database administration client or credential manager.
- A general monitoring/APM suite, firewall manager, packet analyzer, or remote gateway.
- A secrets manager or hosted SaaS.
- A full process manager or tool that automatically kills processes.
- A source-change plan, patch-generation, or patch-application service/tool/endpoint.
- A managed launcher or an autonomous agent that edits files, executes commands, launches services, changes global client configuration, or terminates processes.
- A Docker start, stop, restart, create, remove, or other lifecycle controller.
- An AI-first application or a system that treats model output as authoritative runtime evidence.
- A guarantee that an external unmanaged process cannot race with an availability check.
- A requirement to install Docker, PostgreSQL, Ollama, a model, Tauri, or a GitHub client for baseline local use.
- A broad numeric source-code scanner in the MVP.

## Boundary clarifications

### SQLite

PortAtlas may identify a project as SQLite-backed metadata. SQLite is not represented as a network listener unless another process actually exposes it through a network service.

### Docker

A Docker image may support development or limited Docker-only inspection, but only the native host collector can claim full native visibility. Docker socket access is treated as highly privileged.

### Port suggestions

A suggestion is a policy-aware point-in-time recommendation. Only a reservation or atomic lease coordinates other PortAtlas participants. Even a lease cannot control an external process that ignores the registry.

### File changes and managed actions

The MVP has no source-change planning, patch generation/application, managed launch, process termination, or Docker lifecycle tool/endpoint. It may show the declaration file/location as evidence and provide non-executable manual guidance. Version 1 may design managed/change capabilities behind a new permission and threat review.

### Health and process status

Existing deterministic container/service status can be displayed, but broad health monitoring and stale-process heuristics remain Version 1. PortAtlas never terminates a suspected stale process automatically.

### Worktrees

One logical `Project` owns multiple concrete checkout/worktree `ProjectInstance` records. Each instance has its own canonical path and is the boundary for scanning, runtime association, policy evaluation, reservation, and lease allocation; identity is not path-only.

## Change control

Scope changes require:

1. A stated user/business outcome.
2. MoSCoW priority and displaced work.
3. Security, privacy, performance, accessibility, packaging, and test impact.
4. Updated PRD, SRS, traceability, backlog, and roadmap.
5. Founder approval when the change affects architecture, mutation authority, AI authority, cloud/telemetry, or release scope.

## Related documents

- [PRD](prd.md)
- [Backlog](backlog.md)
- [Roadmap](roadmap.md)
- [Assumptions and constraints](../requirements/assumptions-and-constraints.md)
