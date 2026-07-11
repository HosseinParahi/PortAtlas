# Quality Assurance Plan

Status: **Proposed pre-implementation contract**

## Change workflow

1. Link the change to a requirement, ADR, risk, and test impact.
2. Add or update a failing automated test before behavior implementation.
3. Review deterministic behavior, managed/unmanaged language, privacy classification, accessibility, and degradation.
4. Run the smallest relevant suite during development and the full mandatory matrix before a release gate.
5. Record reproducible evidence and resolve all release-blocking findings.

## Review matrix

| Change area | Mandatory review | Mandatory suites |
|---|---|---|
| Domain or allocator | Architecture and data | UT-DOM-001, UT-ALC-001, IT-SQL-001, concurrency cases |
| Collector or scanner | Security and provenance | UT-COL-001 or UT-SCN-001, adversarial fixtures, E2E freshness |
| REST, SSE, CLI, MCP | Contract and security | CT-API-001 or CT-MCP-001, auth and redaction cases |
| UI | Product, accessibility, and copy | E2E-CORE-001, keyboard, focus, non-color state, compact layout |
| Storage or migration | Data and operations | IT-SQL-001, IT-PG-001, backup/restore drill |
| Optional AI | Security, privacy, and product | AI-EVAL-SAFE-001 plus full core regression without provider |
| Packaging or release | Operations and security | Clean install, upgrade, uninstall, permissions, signing checks |

## Defect severity

- **Critical:** secret disclosure, authentication bypass, destructive or forbidden mutation, authoritative-state corruption, unsafe public network exposure. Blocks all release work.
- **High:** incorrect allocation assurance, lease race, project-root escape, inaccessible core workflow, data-loss recovery failure. Blocks the affected gate.
- **Medium:** material parser miss, stale or misleading evidence, degraded-state failure, substantial performance regression. Requires disposition before release.
- **Low:** cosmetic or low-impact documentation issue with no truth, accessibility, privacy, or workflow effect. May be scheduled with written rationale.

Severity is based on impact and reproducibility, not on who reported the issue.

## Entry and exit

A release candidate enters QA only when requirements and migrations are frozen for the candidate, mandatory unit and contract suites pass, release notes are drafted, and known risks are recorded. It exits only when critical and high defects are zero, medium defects have founder-approved disposition, UAT passes, security and performance thresholds pass, and operational drills produce reproducible evidence.

## Exploratory charters

- Rapid process and container churn while browsing and filtering
- Multiple worktrees with identical repository remotes and different declarations
- Port exhaustion, lease expiry, concurrent retries, and stale browser revisions
- Docker unavailable, permissions denied, engine restart, and malformed metadata
- Renamed, deleted, nested, oversized, encoded, and symlinked project files
- Browser restart, service restart, expired bootstrap, and credential rotation
- Keyboard-only use, narrow layouts, zoom, reduced motion, and non-color conflict recognition
- Optional provider unavailable, slow, malicious, invalid, and disabled mid-request

## Documentation QA

The standard-library validator enforces required files, links, ADR sequence, stable IDs, traceability, unresolved markers, personal paths, and common secret patterns. Human review still checks meaning, contradictions, legal claims, and operational truth.
