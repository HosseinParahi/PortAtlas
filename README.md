# PortAtlas

> **Working title and engineering-foundation project.** No package, container image, domain, manifest namespace, or public release may use the PortAtlas name until the naming decision in [ADR-0023](docs/adr/0023-working-name-collision-trademark-clearance.md) is resolved.

PortAtlas is a planned local-first control plane for understanding which development services use which ports, where those claims came from, and where conflicts or capacity risks exist. The founder approved **Gate 2: product and architecture foundation** at exact revision [`e53f399`](docs/project/gate-2-approval.md). **Gate 3: engineering foundation has complete candidate-local evidence and awaits exact-revision hosted CI and founder binding**; an installable product, completed runtime inventory, and release candidate do not exist.

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

- [Product charter](docs/product/project-charter.md)
- [Business requirements](docs/product/brd.md) and [product requirements](docs/product/prd.md)
- [Software requirements specification](docs/requirements/srs.md) and [traceability matrix](docs/requirements/traceability-matrix.md)
- [Architecture](docs/architecture/system-context.md) and [architecture decisions](docs/adr/README.md)
- [Security model](docs/security/threat-model.md)
- [Test strategy](docs/testing/test-strategy.md)
- [Delivery roadmap](ROADMAP.md)
- [Checkpoint record](docs/project/first-checkpoint-plan.md)
- [Gate 2 approval and provenance](docs/project/gate-2-approval.md)
- [Gate 3 sprint brief and evidence boundaries](docs/project/gate-3-sprint-brief.md)
- [Gate 3 evidence ledger](docs/project/gate-3-evidence.md)

## Current status

The Gate 3 foundation includes a private, tested workspace and minimal foundation shells. These do not constitute an installable product or proof of later-gate features. Installation, service lifecycle, recovery, and release packaging remain proposed contracts until their owning gates produce evidence. A command is supported only when [Development setup](docs/operations/development-setup.md) identifies it as verified.

After the pinned bootstrap in [Development setup](docs/operations/development-setup.md), run the mandatory default foundation gate with:

```bash
python3 scripts/check.py all
```

Network advisory/license checks and opt-in PostgreSQL/packaging research are separate profiles documented in that guide. No default command requires Docker or Ollama.

## License and commercial use

This repository is licensed under the [Apache License 2.0](LICENSE). Companies and individuals may use it commercially without paying for permission, subject to that license. Sponsorship is voluntary and does not purchase usage rights. The project name and marks are separate from the copyright license; see [GOVERNANCE.md](GOVERNANCE.md) and ADR-0023.
