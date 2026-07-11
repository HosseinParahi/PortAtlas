# ADR 0004: Docker

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Container and Compose observation

## Context

Developers need Docker container ports correlated with native host listeners and project declarations. Docker is common but cannot be a mandatory PortAtlas dependency. The Docker daemon exposes a privileged control surface, so an integration built for observation must not accidentally become a general container-control API.

## Decision

Implement Docker as an optional adapter using the Docker SDK for Python over the version-negotiated Docker Engine API:

- The MVP requests only inspection and event capabilities needed for containers, port bindings, networks, health, image metadata, timestamps, and Compose labels.
- Published host bindings, exposed container ports, and Dockerfile declarations remain distinct.
- Compose project and service labels are the primary project-association evidence when present.
- Docker events accelerate updates; periodic full reconciliation repairs missed events and restart gaps.
- Docker absence, Docker Desktop shutdown, permission denial, and unsupported API versions produce explicit degraded status while core host collection continues.
- The browser UI and remote clients never receive access to the Docker socket.
- PortAtlas does not open an unauthenticated TCP proxy to the daemon.
- Container start, stop, removal, image pull, and arbitrary Engine operations are outside the MVP adapter.
- A containerized PortAtlas mode may inspect only what it can truthfully observe and must disclose host-visibility limits.

## Alternatives considered

### Invoke the Docker CLI

The CLI is useful for manual diagnostics but adds output parsing and subprocess lifecycle concerns when a typed, version-aware API is available.

### Read Compose files only

Static declarations cannot establish running container identity, actual published bindings, health, or event state.

### Mount the Docker socket into a PortAtlas container

This is convenient but grants broad daemon control and still does not solve macOS native-host process visibility.

### Make Docker a required deployment foundation

This conflicts with zero-setup local use and the requirement to remain useful without Docker.

## Consequences

### Positive

- Runtime container mappings use authoritative daemon data.
- Event latency improves without sacrificing reconciliation.
- Compose evidence supports project and service association.
- Docker failure does not take down native inventory.

### Costs and risks

- Access to the Docker socket is highly privileged even for read-oriented code.
- API versions and Docker Desktop behavior require compatibility tests.
- Host-network and platform-specific networking can make apparent bindings subtle.
- A compromised core service could misuse its daemon access, so the adapter must stay narrow and auditable.

## Verification

- Test Docker unavailable, stopped, permission-denied, and API-version mismatch states.
- Reconcile running and stopped containers, TCP and UDP bindings, multiple interfaces, IPv4 and IPv6, health, networks, and Compose labels.
- Drop or reorder event fixtures and prove full reconciliation restores correct state.
- Verify the adapter surface cannot create, start, stop, remove, exec in, or pull for a container.
- Cross-check a native listener conflict with a published Docker host port.
- Inspect API, logs, MCP, and diagnostics to prove the socket path and daemon credentials are not leaked.

## Revisit triggers

- An approved managed-launch feature needs narrowly scoped Docker mutations.
- Docker changes its supported API or Compose-label conventions.
- Rootless or alternative container engines become an MVP requirement.
- A safer privilege-separated collector becomes practical.

## Sources

- [Docker Engine API](https://docs.docker.com/reference/api/engine/)
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
- [Docker Engine security](https://docs.docker.com/engine/security/)
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)
