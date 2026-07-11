# PortAtlas Personas

## How to use these personas

Personas guide priorities, journeys, UX language, security defaults, and UAT. They describe needs and behavior, not demographic assumptions. Each persona maps to the [PRD](prd.md), [User journeys](user-journeys.md), and [Acceptance criteria](../requirements/acceptance-criteria.md).

## Persona P-01: Multi-project local developer

### Context

Runs many frontends, APIs, databases, containers, automation tools, and desktop applications across personal, work, experiment, archived, monorepo, and worktree directories. One logical repository project may have several concrete checkout/worktree `ProjectInstance` records. Starts services externally from terminals, IDEs, scripts, Docker Compose, and project launchers.

### Goals

- Know what owns a port and how it maps to a project/service.
- See conflicts before starting an inactive project.
- Reuse stable project ports and avoid system/ephemeral ranges.
- Distinguish a Docker internal port from a published host binding.
- Spot services exposed beyond loopback.
- Configure roots and policies without editing application source.

### Pain points

- Familiar defaults collide across unrelated projects.
- PID-only answers are unreliable and process commands can contain secrets.
- Configuration may declare ports in multiple files and environments.
- A stale listener remains after the visible project session ends.
- Generic dashboards show containers but miss native services or inactive declarations.

### Behaviors and constraints

- Needs high-density, keyboard-friendly inventory and fuzzy search.
- May not have Docker running and should not need elevated permissions for baseline value.
- Expects explicit uncertainty when ownership or permissions are incomplete.
- Will accept confirmation for mutation but not for ordinary observation.

### Success signals

- Finds process, PID/start time, project, service, address, Docker state, source, and timestamp for an active port in no more than two interactions.
- Adds and previews a root from the UI, scans it, and sees evidence/confidence.
- Resolves a conflict with a reviewed reservation or manual plan.

## Persona P-02: Agent-assisted developer

### Context

Uses Codex, Claude-compatible clients, or another MCP host to scaffold services, change configuration, or launch development commands. Wants automation without granting unrestricted machine authority.

### Goals

- Make the agent check the entire approved PortAtlas state before choosing a port.
- Receive a deterministic, explained suggestion and atomic lease.
- Receive an instance-scoped reservation/lease without exposing source-edit or launch tools.
- Re-query runtime evidence after an external launch while understanding that MVP did not supervise it.

### Pain points

- Agents select familiar defaults from training patterns.
- Tool-specific instruction files duplicate business rules and drift.
- Repository text can contain malicious or accidental instructions.
- A model may claim a port is free without checking current state.

### Behaviors and constraints

- Prefers typed MCP tools and stable machine-readable errors.
- Expects read-only access by default and a narrow project scope for mutation.
- Treats suggestions as advisory until leased/reserved.
- Does not authorize process killing, arbitrary shell, or silent global-client edits.

### Success signals

- Completes resolve → preflight → diagnose → suggest → lease in one workflow.
- MVP agent workflow exposes no source-edit, managed-launch, process-control, Docker-lifecycle, or launch-verification tool.
- Repository prompt injection cannot expand tools, paths, or permission policy.

## Persona P-03: Open-source maintainer

### Context

Maintains a project with multiple contributors and wants stable local development conventions without operating hosted infrastructure or exposing contributor machine state.

### Goals

- Eventually publish a documented optional project manifest after its name and schema gates, while using safe policy examples in MVP.
- Give contributors a quick installation and synthetic demo.
- Add parsers or service catalog entries through isolated, fixture-tested extensions.
- Release verifiable artifacts with predictable upgrade and rollback.

### Pain points

- Contributor instructions drift across operating systems and local toolchains.
- Security reports can accidentally include paths, environment values, or process arguments.
- Large dependency graphs and unclear architecture deter contribution.

### Behaviors and constraints

- Values small contracts, ADRs, semantic versioning, CI, license clarity, and reproducible fixtures.
- Needs a clear compatibility policy and no mandatory GitHub API.
- Requires bug-report redaction warnings and a responsible disclosure path.

### Success signals

- A contributor explores demo mode without system permissions.
- A scanner contribution has documented evidence semantics, fixtures, and targeted tests.
- Release and contributor documentation match verified commands.

## Persona P-04: Future small-team developer

### Context

Works in a small team that may share recommended ranges, service categories, or project manifests while every developer retains a separate local runtime inventory.

### Goals

- Reuse team policy without synchronizing sensitive host/process state.
- Preserve local overrides and machine-specific reservations.
- Understand portability and migration of manifests and policies.

### Constraints

- This persona does not expand the MVP into a multi-user server.
- PostgreSQL team mode, remote agents, shared registry, and cloud sync remain later capabilities requiring new threat and product review.

### Success signals

- MVP schemas are versioned and exportable without secrets.
- Domain logic does not assume SQLite-specific behavior or macOS-specific paths.

## Anti-personas and intentionally unsupported expectations

- A platform operator seeking full Docker/Kubernetes orchestration.
- A database administrator seeking query or credential management.
- A security administrator seeking firewall enforcement or packet inspection.
- A remote user seeking a cloud-access gateway.
- A user expecting PortAtlas to kill processes, rewrite arbitrary files, or guarantee control over unmanaged launches.
- An AI user expecting a model to be authoritative or receive unrestricted tools.

These needs are outside [MVP scope](scope-and-non-goals.md).
