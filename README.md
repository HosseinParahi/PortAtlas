# PortAtlas

> **Working title and pre-implementation project.** No package, container image, domain, manifest namespace, or public release may use the PortAtlas name until the naming decision in [ADR-0023](docs/adr/0023-working-name-collision-and-trademark-clearance.md) is resolved.

PortAtlas is a planned local-first control plane for understanding which development services use which ports, where those claims came from, and where conflicts or capacity risks exist. This repository is at **Gate 2: product and architecture foundation**. It contains documentation, governance, and a documentation validator only; it does not yet contain an installable application.

## Product promise

PortAtlas will combine host-socket evidence, Docker metadata, deterministic project scanning, reservations, and leases into a single inventory. It is designed for one local macOS user first, with Linux and Windows kept behind explicit adapter contracts.

The assurance boundary is deliberately strict:

- **Managed state** means a reservation or atomic lease was created through PortAtlas. PortAtlas can strongly guarantee uniqueness only inside this managed allocation boundary.
- **Unmanaged state** means a process, container, or configuration was discovered outside PortAtlas. It is evidence that can become stale, incomplete, or race with other tools; it is never described as a guarantee.

MVP mutation is limited to creating, renewing, and releasing reservations and leases. PortAtlas will not patch source files, launch projects, or terminate processes in the MVP.

## Planned foundation

- A native Python modular monolith serving a React browser UI
- Embedded SQLite through SQLAlchemy repositories, plus an optional PostgreSQL profile with compatibility tests
- Multiple worktree-aware `ProjectInstance` records beneath one logical `Project`
- Versioned REST commands under `/api/v1` and Server-Sent Events for browser updates
- CLI, REST, and MCP adapters calling the same application services
- MCP over STDIO and authenticated loopback Streamable HTTP
- No telemetry
- Conditional local Ollama assistance only after every privacy, redaction, prompt-injection, schema-validation, and failure-isolation gate passes

The proposed `.portatlas.yaml` manifest is a design contract only and must not be published as a namespace before the working-name gate closes.

## Documentation map

- [Product charter](docs/product/product-charter.md)
- [Business requirements](docs/product/brd.md) and [product requirements](docs/product/prd.md)
- [Software requirements specification](docs/requirements/srs.md) and [traceability matrix](docs/requirements/traceability-matrix.md)
- [Architecture](docs/architecture/system-context.md) and [architecture decisions](docs/adr/README.md)
- [Security model](docs/security/threat-model.md)
- [Test strategy](docs/testing/test-strategy.md)
- [Delivery roadmap](ROADMAP.md)
- [Checkpoint record](docs/project/first-checkpoint-plan.md)

## Current status

Installation, launch, recovery, and API examples are not operational yet. Any such material in `docs/operations/` or `docs/design/` is explicitly a proposed contract for later implementation and verification.

Run the documentation quality gate with:

```bash
python3 scripts/validate_docs.py
```

## License and commercial use

PortAtlas is intended to be released under the [Apache License 2.0](LICENSE). Companies and individuals may use it commercially without paying for permission, subject to that license. Sponsorship is voluntary and does not purchase usage rights. The project name and marks are separate from the copyright license; see [GOVERNANCE.md](GOVERNANCE.md) and ADR-0023.
