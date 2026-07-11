# ADR 0013: Plugin boundary

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Extension contracts and third-party code loading

## Context

Collectors, project scanners, service catalogs, health checks, port policies, and agent integrations are natural extension points. Loading arbitrary Python packages inside a host-observing service would give third-party code the service's filesystem, process, database, Docker, and credential access. The MVP needs replaceable modules for testing and future growth, but not a public plugin marketplace.

## Decision

Separate internal extension contracts from public plugin execution:

- Define versioned typed protocols for runtime collectors, project scanners, service-catalog providers, health checks, port-policy providers, and client integrations.
- Register built-in implementations explicitly at startup. Their capabilities, configuration schema, version, and evidence source are visible in local diagnostics.
- Test every built-in implementation through its contract without starting the full application.
- Do not discover or execute arbitrary third-party Python entry points, shared libraries, downloaded code, or UI contributions in the MVP.
- Reserve a versioned plugin manifest format describing identity, API version, capabilities, permissions, configuration schema, provenance, and compatibility, but do not treat a manifest as a security boundary.
- A future public plugin system must receive a separate threat model and ADR. The preferred research direction is an out-of-process protocol with explicit capability grants, resource limits, canonical path scope, authenticated messages, and revocation.
- UI contribution plugins remain deferred until a dedicated browser-content and supply-chain security review.
- Unknown plugin configuration is rejected safely; disabling an extension cannot corrupt core state.

## Alternatives considered

### Python entry-point plugins in the MVP

Entry points are conventional and easy to develop, but they execute with full process authority and provide no meaningful isolation.

### Out-of-process plugins immediately

This offers a better permission boundary but requires protocol versioning, lifecycle, distribution, sandboxing, and support work before real external plugin demand exists.

### No extension contracts

This is smaller initially but would couple platform collectors and scanners to the application and make cross-platform work harder.

### Web UI plugins

UI extensibility is powerful but introduces script execution, dependency collision, content-security-policy, accessibility, and data-access risks.

## Consequences

### Positive

- Core modules are replaceable and testable without exposing a public code-loading surface.
- The MVP supply chain and privilege boundary stay smaller.
- Future plugins have named capability and manifest concepts to build on.
- Built-ins and future extensions can share evidence contracts.

### Costs and risks

- External contributors cannot ship drop-in plugins during the MVP.
- Explicit registration adds small amounts of wiring.
- Internal protocols can still evolve before a public compatibility promise.
- Out-of-process isolation remains future research rather than an implemented guarantee.

## Verification

- Run a shared contract suite for each built-in extension type.
- Verify startup loads only the explicit built-in registry.
- Place an installed package with matching Python entry points in the environment and prove PortAtlas does not execute it.
- Fuzz extension results and configuration at the normalization boundary.
- Ensure disabled or failing built-ins report degraded status without crashing unrelated capabilities.
- Review every added extension point for least privilege and data provenance.

## Revisit triggers

- At least two independently maintained third-party extensions need a stable distribution contract.
- Linux or Windows support demonstrates a contract missing from built-in adapters.
- A practical OS sandbox and signed distribution model is selected.
- An approved feature requires UI contributions.

## Sources

- [Python packaging entry-points specification](https://packaging.python.org/en/latest/specifications/entry-points/)
- [Python importlib.metadata entry points](https://docs.python.org/3/library/importlib.metadata.html#entry-points)
- [OWASP Third Party JavaScript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)
