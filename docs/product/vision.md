# PortAtlas Product Vision

## Vision statement

PortAtlas gives a developer one trustworthy, private map of the ports used and planned across their machine—and gives coding agents a safe way to consult that map before choosing or changing a port.

It should make the question "what owns this port, what else expects it, and what should I use instead?" answerable in seconds with evidence rather than guesswork.

## Why this matters

Modern local development spans frontends, APIs, databases, Docker Compose stacks, desktop applications, monorepos, worktrees, manually launched services, and automated coding agents. Each tool sees only part of the machine. Familiar defaults such as 3000, 5432, 6379, and 8080 collide across projects, while wildcard bindings can expose development services unexpectedly.

PortAtlas treats local port coordination as a state-reconciliation problem rather than a prettier wrapper around one socket command. It joins:

- **Observed state:** what is listening now.
- **Declared state:** what project configuration says may listen.
- **Reserved state:** what a user or policy has assigned.
- **Leased state:** what is atomically held for a participating client before an external launch.
- **Desired state:** what a reviewed plan proposes.
- **Evidence:** where each association came from and how certain it is.

## Value proposition

### For multi-project developers

- Find the process, service, project, container, declaration, address, and evidence behind a port.
- See conflicts before starting inactive projects.
- Reserve predictable ports without maintaining a private spreadsheet.
- Detect unexpected LAN or wildcard exposure.

### For agent-assisted developers

- Require an agent to preflight the machine before selecting a default.
- Return typed, explained suggestions and acquire atomic leases.
- Receive an instance-scoped reservation or lease without source-edit or launch authority.
- Recheck current evidence after an external launch while preserving the unmanaged limitation.

### For open-source maintainers

- In Version 1, after the name gate, publish project-local port intent through an optional versioned manifest.
- Give contributors consistent onboarding and conflict diagnostics.
- Keep core behavior deterministic, offline, and independent of an LLM.

## Assurance promise

The MVP coordinates PortAtlas participants with reservations and atomic leases but does not edit configuration, launch/stop services, control Docker lifecycle, terminate processes, or verify a launched listener. Every actual launch is unmanaged and can race with external processes that ignore the registry. A future Version 1 managed runner may provide stronger prevention only after it owns assignment injection, launch, verification, and cleanup.

The product will always label which boundary applies. It will not imply that a suggestion reserves a port, that an MVP lease supervises a launch, or that a dashboard controls arbitrary processes.

## Experience principles

1. **Evidence before assertion:** every port fact exposes source, timestamp, collector/parser, and confidence.
2. **Safe first action:** inspection is the default; allowed registry/configuration mutations are explicit and scoped.
3. **One map, distinct states:** do not flatten observations, declarations, reservations, and plans into one ambiguous status.
4. **Fast path to cause:** ownership and source are no more than two interactions away under normal use.
5. **Configuration without code edits:** roots, policies, exclusions, integrations, and preferences are managed through UI, CLI, or versioned files.
6. **Degraded, not broken:** missing Docker, limited permissions, or unavailable Ollama produces visible partial capability, not a failed core service.
7. **Local means minimized:** running a model locally does not justify sending secrets or entire source trees to it.
8. **Accessible density:** a high-information table remains keyboard navigable, readable without color, responsive, and screen-reader compatible.

## Product horizon

### MVP

Deliver reliable macOS inventory, Docker mapping, logical `Project` plus concrete checkout/worktree `ProjectInstance` discovery, the locked parser set, evidence, policies, conflict detection, manual reservations, atomic leases, safe suggestions, React browser UI, API with Server-Sent Events, CLI, MCP integrations, audit, demo mode, non-secret configuration portability, macOS packaging, and optional AI only if its security/evaluation gates pass.

### Version 1

Extend to Linux and Windows, managed launch profiles and `portatlas run`, source-change planning/patching, health and stale-service signals, richer `ProjectInstance` Git metadata, shell completion, Tauri/tray options, deferred scanner/proxy adapters, reverse-proxy aliases, notifications, pluggable scanners/collectors, PostgreSQL team mode, and opt-in local embeddings.

### Later

Consider remote agents, team-shared policy, multi-machine dashboards, IDE extensions, Kubernetes/local clusters, proxy/certificate automation, and cloud synchronization only after the local registry and permission model are proven. PortAtlas does not aspire to become a database administrator, firewall, general observability suite, secrets manager, full process supervisor, or autonomous coding agent.

## Product identity

"PortAtlas" is a working title. A public release requires an ADR documenting repository, package-registry, domain, and trademark/name-collision checks. Until then, the name communicates the concept but does not represent a final brand decision.

## Related documents

- [Project charter](project-charter.md)
- [Business requirements](brd.md)
- [Product requirements](prd.md)
- [Personas](personas.md)
- [User journeys](user-journeys.md)
- [Success metrics](success-metrics.md)
- [System requirements](../requirements/srs.md)
