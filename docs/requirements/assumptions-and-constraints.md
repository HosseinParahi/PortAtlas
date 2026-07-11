# PortAtlas Assumptions, Constraints, and Open Decisions

## Purpose

This register prevents planning defaults from becoming hidden architectural facts. Accepted Gate 2 decisions are labeled as constraints rather than left open. The remaining assumptions require measured implementation evidence, while unresolved release inputs stay blocked rather than being guessed.

## Assumption register

| ID | Planning assumption | Basis | Validation or decision point |
| --- | --- | --- | --- |
| AS-001 | macOS is the only fully implemented MVP host platform. | Founder environment and macOS-first principle | Gate 2 platform ADR and Gate 4 real-machine validation |
| AS-002 | MVP serves one local OS user. | Lowest-risk local-first mode | Gate 2 auth/data model review |
| AS-003 | Embedded SQLite is default local persistence behind SQLAlchemy; PostgreSQL is an optional compatibility profile. | Accepted persistence decision | Repository contract tests and performance evidence at Gates 3–5 |
| AS-004 | A native Python service serving a React browser UI is the accepted MVP runtime architecture. | Accepted runtime decision | Clean-machine and packaging evidence at Gates 3 and 9 |
| AS-005 | Tauri/menu-bar packaging is Version 1. | Accepted scope decision | Revisit only through a later ADR |
| AS-006 | Codex receives the first polished client integration; Claude-compatible docs follow the client-neutral MCP contract. | Master brief default | Gate 1 product review and current client-doc research |
| AS-007 | No telemetry is included. | Accepted privacy decision | A later proposal requires a new ADR and privacy review; no enable setting exists |
| AS-008 | Runtime history retention defaults to seven days and is configurable. | Master brief default | Gate 2 data/retention ADR and performance/storage review |
| AS-009 | Health checks and stale-service heuristics are minimal or Version 1; existing deterministic Docker/provider status may be displayed. | Avoids expansion into monitoring/process management | Gate 1 scope and Gate 2 domain review |
| AS-010 | Managed `portatlas run`, source patch application, process termination, and Docker lifecycle mutation are Version 1 or later. MVP mutation is limited to reservations and atomic leases. | Accepted mutation boundary | Revisit only through a later threat review and ADR |
| AS-011 | Optional Ollama may enter MVP only after all security/evaluation gates; it is disabled by default. | Optional-AI release criteria | Gate 2 scope and Gate 8 evidence |
| AS-012 | `qwen3:4b` is only a starting balanced-model candidate. | Master brief recommendation | Current availability/license/capability/resource benchmark before recommendation |
| AS-013 | AI receives read-only tools; raw prompts/conversations are not stored by default. | Authority and privacy boundary | Gate 2 AI ADRs and Gate 8 security tests |
| AS-014 | Embeddings/semantic search are Version 1, opt-in, local-only, and do not require PostgreSQL/pgvector. | Master brief default | Embedding-store/privacy ADR before implementation |
| AS-015 | No remote AI provider, cloud service, or automatic model download is configured. | Local-first and explicit-consent constraints | New founder approval and threat/privacy review |
| AS-016 | The initial repository had no project files beyond Git metadata when this documentation pass began. | Read-only repository inspection | Re-inspect before foundation work and preserve any later user changes |

## Mandatory constraints

| ID | Constraint | Consequence |
| --- | --- | --- |
| CON-001 | Local-first, private, offline-capable core | No mandatory network, cloud, telemetry, hosted database, GitHub API, Docker, or model dependency |
| CON-002 | Read-only by default | Mutation requires explicit policy, scope, preview/diff where relevant, confirmation, auth, and audit |
| CON-003 | Managed and unmanaged assurance remain distinct | No zero-conflict guarantee for external processes; suggestion is not reservation |
| CON-004 | Observed, declared, reserved, leased, desired, conflicted, stale, unknown, ignored, and AI-suggested state stay separate | No ambiguous mutable "port" row as sole source of truth |
| CON-005 | Every discovery claim has evidence/provenance and confidence where applicable | UI/API/MCP/model output links to source/timestamp; uncertainty is explicit |
| CON-006 | Native host visibility is required | Docker-only deployment cannot claim complete native process/socket inventory |
| CON-007 | Docker is optional and privileged | Core works without Docker; socket is not exposed remotely/unauthenticated |
| CON-008 | React/TypeScript UI and Python backend/system services | Technology ADRs choose supporting libraries without replacing these requested languages |
| CON-009 | macOS-first behind platform adapters | OS-specific code is isolated; domain logic has no macOS-only paths/assumptions |
| CON-010 | No secret leakage | Complete environment files/credentials/unsafe process args are absent from all outputs, persistence, model context, exports, tests, and reports |
| CON-011 | Scan only approved canonical roots | Preview, exclusions, symlink policy, size/time/concurrency limits, and no broad source scan by default |
| CON-012 | Safe subprocess execution | Argument arrays, timeouts and output bounds; no shell interpolation of untrusted values or automatic `sudo` |
| CON-013 | Loopback default and least privilege | Non-loopback requires explicit opt-in; mutating HTTP is authenticated and origin-protected |
| CON-014 | No automatic process termination or arbitrary source rewrite | No MVP kill tool; model never gets process control; file mutation remains narrowly governed |
| CON-015 | AI is optional, advisory, and subordinate | Model cannot determine authoritative availability/conflict, create leases, expand permissions, or corrupt core state |
| CON-016 | Repository/model text is untrusted | Fixed tool allowlists, delimited context, independent argument/path/evidence validation |
| CON-017 | Current primary specifications must be verified | Record date/version in ADRs; do not finalize from outdated secondary posts |
| CON-018 | Open-source quality is part of MVP | Tests, docs, accessibility, security, governance, packaging, release automation, and contributor experience are required work |
| CON-019 | No microservice or giant-monolith extremes for local MVP | Use focused modular boundaries inside a native service; adapters independently testable |
| CON-020 | Approval gates govern architecture, mutation, AI authority, telemetry/cloud, and release | Reversible documentation may proceed; dependent production decisions may not be silently assumed |

## Remaining decision and release-input register

| ID | Input | Current safe state | Approval point |
| --- | --- | --- | --- |
| OD-001 | Public product name and trademark clearance | `PortAtlas` is a working title; publish no namespace | Before any public artifact |
| OD-002 | Package, image, MCP, Homebrew, manifest, and domain namespaces | None is approved or reserved by this checkpoint | After OD-001 |
| OD-003 | Signing identity and public release contact | No identity is invented | Before packaging/release |
| OD-004 | Sponsorship platform and active handle | Sponsorship is voluntary; omit funding metadata | When founder supplies a verified handle |
| OD-005 | Native packaging implementation | Research PyInstaller/native service lifecycle, signing, notarization, update, rollback, and uninstall | Gate 3 prototype and packaging ADR acceptance |
| OD-006 | Exact dependency patch versions | Reverify and lock from primary sources | Gate 3 foundation |
| OD-007 | Founder parser corpus and representative capacity hardware | Use synthetic labeled fixtures until approved samples are available | Gates 4–5 |
| OD-008 | Exact bounded retention durations | Prefer the shorter privacy-preserving behavior; no raw AI history by default | Data/privacy implementation review |
| OD-009 | Ollama inclusion, provider version, model digest, and resource profile | Excluded unless every conditional gate passes in one recorded run | Gate 8 |
| OD-010 | Final project-manifest filename and publication | `.portatlas.yaml` is a design-only working name and not in the locked MVP parser set | After OD-001 and explicit schema approval |

## Scope tensions and documented treatment

### PostgreSQL request versus zero-setup local storage

The accepted design preserves Python/React, uses embedded SQLite by default behind SQLAlchemy repositories, and retains PostgreSQL as an optional compatibility profile. PostgreSQL is not a required local service, and shared repository contract tests prevent silent drift.

### Strong prevention versus managed-run timing

The product truth describes strong prevention only for a future complete managed-launch workflow. The registry-only MVP provides atomic reservations and leases to cooperating PortAtlas clients but does not bind an OS socket, patch, launch, terminate, or verify a child process. It must not market a future runner as present capability or extend registry atomicity to unmanaged processes.

### Change plans versus patch application

Conflict/UI/MCP design may name safe evidence and recommendations. MVP exposes no source-patch tool or endpoint. Deterministic patch planning and application are deferred to a separately approved Version 1 contract; arbitrary source editing is always outside scope.

### Worktree discovery versus worktree-aware identity

One logical `Project` owns multiple concrete checkout/worktree `ProjectInstance` records. The instance is the accepted boundary for scanning, runtime association, policy, reservations, and leases; absolute path alone is not identity.

### Health/stale fields versus monitoring scope

Docker/provider status already available from deterministic sources can be displayed. Active HTTP/TCP/command health probes and stale-process heuristics remain later work unless explicitly promoted. A future-compatible model or UI column is not evidence that monitoring is implemented.

### Optional AI listed in MVP versus conditional release

All AI requirements and acceptance scenarios are documented now, but only core-independent, default-off functionality that passes strict security/evaluation gates may enter MVP. Failing the AI gate removes or defers AI without delaying core release.

### CLI and Version 1 candidates

The MVP CLI set is normative in `SRS-CLI-001`. Managed run, plan application, doctor, shell-completion command, and CLI import/export are Version 1 candidates; MVP import/export may be delivered through UI/API/config service without promising those CLI commands.

## Approval checklist by gate

### Gate 1 product direction

- Accept personas, product value, scope/non-goals, MoSCoW, assurance wording, metrics, journeys, and roadmap.
- Confirm the locked parser catalog, registry-only mutation boundary, and conditional-AI policy reflected in the product source of truth.

### Gate 2 architecture and MVP

- Approve the accepted ADR outcomes for runtime, persistence, `ProjectInstance`, allocator, SSE, auth, MCP, no telemetry, Apache-2.0, and AI boundaries.
- Approve threat, data, API/MCP, mutation, packaging-research, and test strategies; authorize no production implementation until this gate is explicit.

### Gate 8 optional AI

- Decide `OD-009` from measured model/provider/license/resource results and every applicable `AC-010` through `AC-015` outcome.

### Gate 9 release

- Close `OD-001` through `OD-006` and `OD-010`; approve signing/artifacts, lifecycle/UAT, security review, dependency licenses, SBOM, and the release checklist.

## Change discipline

When an assumption becomes a decision, record its ADR/decision-register reference and update [PRD](../product/prd.md), [SRS](srs.md), [Traceability](traceability-matrix.md), [Backlog](../product/backlog.md), and [Roadmap](../product/roadmap.md) in the same coherent change. If a non-blocking detail remains unclear, use the documented reversible default and surface it at the named gate rather than inventing machine or founder facts.
