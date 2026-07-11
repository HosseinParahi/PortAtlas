# PortAtlas Business Requirements Document

## 1. Executive summary

PortAtlas addresses the operational cost and safety risk of inconsistent local development ports. It combines runtime observation, static configuration discovery, explicit reservations, concurrency-safe leases, conflict analysis, and permissioned agent access in an open-source, local-first product. The business case is developer time saved, safer local networking, more predictable onboarding, and a durable open-source coordination standard rather than a hosted data product.

This BRD defines why the product should exist and what outcomes matter. Feature behavior is specified in the [PRD](prd.md) and [SRS](../requirements/srs.md).

## 2. Business problem

Developers operating many web applications, services, databases, containers, worktrees, and agent workflows lack a machine-wide source of truth for ports. Conflicts emerge at startup, ownership requires manual command-line investigation, inactive declarations are invisible, and source changes are often inconsistent or undocumented. Agents amplify the problem when they select familiar defaults without consulting other projects.

The absence of coordinated state causes:

- Failed or misdirected development launches.
- Time spent tracing processes, containers, and configuration.
- Unintended bindings to public or LAN interfaces.
- Fragile onboarding instructions and contributor-specific port conventions.
- Race-prone automated changes without reservation or verification.
- Secret leakage risk when broad project/environment inspection is used as a shortcut.

## 3. Product opportunity

A native, local-first control center can reconcile what is running with what projects declare and what users reserve. MCP offers a client-neutral integration boundary for coding agents, while an optional local model can improve explanation without owning safety-critical decisions. An open-source implementation can become shared development infrastructure without requiring users to upload repository or process metadata.

## 4. Stakeholders

| Stakeholder | Need | Success signal |
| --- | --- | --- |
| Founder/product owner | A dependable daily control center with controlled scope | Primary UAT workflows pass and architecture/release gates are reviewable |
| Multi-project developer | Fast machine-wide ownership and conflict answers | Owner/source found within two interactions; conflicts found before launch |
| Agent-assisted developer | Safe, typed preflight and reservation | One MCP workflow checks and reserves without unapproved edits |
| Open-source maintainer | Sustainable contribution and release process | Clean setup, green CI, useful fixtures, policy and governance docs |
| Security/privacy reviewer | Least privilege and no secret leakage | Threat controls and adversarial tests pass |
| Future team administrator | Portable policy without centralizing local runtime data | Versioned policy/export design supports later team mode |

## 5. Business objectives

| ID | Objective | Measure |
| --- | --- | --- |
| BO-01 | Establish trusted local port intelligence | Runtime and declaration evidence is visible, current, and attributable |
| BO-02 | Reduce conflict discovery time | Current and future conflicts are surfaced before supported launch workflows |
| BO-03 | Make safe allocation automatable | Concurrent clients receive unique atomic leases with explained choices |
| BO-04 | Improve developer and contributor onboarding | A first-time user reaches the dashboard in under five minutes and adds roots through UI |
| BO-05 | Preserve local privacy and user control | Core works offline; no secret value appears in default logs, API, MCP, exports, or model context |
| BO-06 | Enable client-neutral agent coordination | Codex and other MCP clients use the same service-owned rules and contracts |
| BO-07 | Create an open-source-quality foundation | Documentation, CI, security, packaging, governance, and release processes ship with the product |
| BO-08 | Add optional intelligence without authority drift | AI can explain evidence but cannot mutate authoritative state or become a core dependency |

Measurement details live in [Success metrics](success-metrics.md).

## 6. Scope

### In business scope for MVP

- macOS-first host and Docker port intelligence.
- Configurable approved roots, one logical `Project` with concrete checkout/worktree `ProjectInstance` records, and the locked MVP deterministic parser set.
- Distinct state, evidence, confidence, conflict, policy, reservation, and lease models.
- Browser dashboard, local API/events, CLI, MCP, integrations, audit, import/export, and demo mode.
- Safe macOS installation lifecycle and open-source contributor/release foundation.
- Optional Ollama assistance only when disabled by default and all defined safety/evaluation gates pass.

### Outside business scope for MVP

- Hosted SaaS, cloud sync, remote access, credential management, database administration, firewall management, Kubernetes, full observability, full process supervision, arbitrary source rewriting, automatic process termination, autonomous AI actions, and guarantees for unmanaged launches.

The normative boundary is [Scope and non-goals](scope-and-non-goals.md).

## 7. Constraints

- Local-first and offline-capable core; no cloud service or telemetry in the accepted product baseline.
- Read-only by default; mutation is scoped, previewed, confirmed, authenticated, and audited.
- Native host collector required; Docker-only deployment cannot claim full host visibility.
- macOS-first implementation behind platform adapters.
- Native Python backend/system service serving a React/TypeScript browser UI.
- Embedded SQLite is the local default and PostgreSQL is a supported optional profile behind the same repository boundary.
- A logical `Project` owns one or more `ProjectInstance` records; the instance is the scan, runtime-association, policy, reservation, and allocation boundary.
- UI updates use Server-Sent Events; MCP uses STDIO and loopback streamable HTTP.
- Current official specifications and dependency status must be verified before architecture finalization.
- Public release requires working-name/package-namespace clearance, signing identity, exact dependency patch locks, and artifact evidence; the project license is Apache-2.0.

## 8. Assurance limitation

The MVP has no managed launcher. Reservations and atomic leases coordinate PortAtlas participants, but PortAtlas does not edit, launch, stop, or verify services, terminate processes, or control Docker lifecycle. Business and marketing materials therefore describe timely evidence, conflict detection, and race-safe allocation—not end-to-end launch prevention. A future Version 1 managed runner may make a stronger integrated-launch claim only after it implements preflight, injection, launch, listener verification, and cleanup.

## 9. Risks and responses

| Risk | Business impact | Response |
| --- | --- | --- |
| Collector accuracy varies by permissions or OS changes | Loss of trust | Show capability gaps, preserve evidence, test real machines, and avoid absolute claims |
| Large scanner scope delays value | Slow release and quality dilution | Prioritize exact high-value formats and corpus-measured detection |
| Local packaging is cumbersome | Adoption target missed | Validate the accepted native Python service plus React browser package on clean machines and retain Tauri as Version 1 |
| Mutating integrations create security incidents | Reputational harm | Read-only default, narrow scopes, dry-run, auth, backup, audit, and no kill tool |
| AI leaks data or hallucinates state | Trust and privacy harm | Minimum redacted context, strict schema/evidence validation, read-only allowlist, optional default-off feature |
| Project name or dependency license conflicts | Release delay/legal risk | Name and license ADRs plus automated license checks |
| Maintainer capacity is insufficient | Unsustainable community | Modular ownership, contribution guide, governance, issue templates, and bounded MVP |

## 10. Accepted baseline and remaining release inputs

The accepted baseline is a local single-user macOS MVP; native Python service plus React/TypeScript browser UI; embedded SQLite default plus PostgreSQL profile; `Project`/`ProjectInstance` identity; Server-Sent Events; MCP STDIO and loopback HTTP; Codex first; no telemetry; Apache-2.0; locked parser and mutation boundaries; and conditional default-off Ollama. [Assumptions and constraints](../requirements/assumptions-and-constraints.md) distinguishes these decisions from the remaining release inputs.

## 11. Adoption strategy

1. Provide a sub-five-minute local quick start and synthetic demo mode.
2. Make the first value visible immediately: current listeners, owners, Docker bindings, and exposures.
3. Let users add one real project root with a preview and measure exact declarations.
4. Offer copy-ready, reversible Codex MCP setup before broader client integrations.
5. Publish fixture-driven scanner contribution guidance and a data-driven service catalog.
6. Release signed or otherwise integrity-verifiable artifacts with upgrade, backup, rollback, and uninstall documentation.

No GitHub API account, Docker installation, internet connection, model installation, or repository clone should be required for normal core use after public release.

## 12. Sustainability and community model

PortAtlas is licensed under Apache-2.0. Commercial use is permitted without payment, while sponsorship is voluntary and grants no product-control or licensing advantage. The sponsorship handle remains a release input. Sustainability may also come from contributions, support, or future team/server capabilities without moving local core data to a mandatory hosted service. Governance, support expectations, security disclosure, compatibility policy, and release cadence must be documented before public launch.

## 13. Competitive and prior-art frame

Phase 0 research must compare socket/process tools, Docker dashboards, local service launchers, port registries, reverse proxies, IDE tooling, and MCP coordination products. The evaluation should focus on PortAtlas's differentiator: reconciled observed/declared/reserved state with evidence and race-safe agent integration. The research must use current primary sources and must not claim competitive facts before verification.

## 14. Legal and release considerations

- "PortAtlas" remains a working title until repository, package, domain, and trademark/name checks are documented.
- Apache-2.0 is the accepted project license and permits commercial use without payment; sponsorship remains voluntary.
- Every dependency and bundled-model candidate still requires current license and exact-version review.
- Diagnostic and issue templates require redaction warnings.
- Releases should include provenance, changelog, security policy, and SBOM where practical.

## 15. Business acceptance

Gate 1 passes when the founder confirms that the product documents reflect the locked value proposition, personas, scope, assurance wording, metrics, and decisions. Gate 2 confirms detailed contracts and threat/test evidence for that baseline. The genuinely open release inputs are working-name and package-namespace clearance, signing identity, sponsorship handle, exact dependency patch versions, packaging implementation evidence, and optional AI inclusion only after its gates pass.

## Related documents

- [Project charter](project-charter.md)
- [PRD](prd.md)
- [Success metrics](success-metrics.md)
- [Roadmap](roadmap.md)
- [Traceability matrix](../requirements/traceability-matrix.md)
