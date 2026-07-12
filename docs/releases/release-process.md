# Release Process

Status: **Proposed release contract; Gate 3 candidate-local evidence complete**

## Current checkpoint truth

This document defines the evidence a future release must produce. Gate 2 was founder-approved on 2026-07-11 at exact revision [`e53f399`](../project/gate-2-approval.md). Gate 3 contributor commands are implemented and candidate-local evidence is complete, while exact-revision hosted CI and founder binding remain open. This document does not claim an installable artifact, public release version, signing identity, publication namespace, or accepted package lifecycle.

The architecture decisions are recorded for review, but this document does not by itself mark a delivery gate complete. Gate disposition must be explicit and linked from the decision or work log.

PortAtlas is a working title. No public package, executable identity, domain, container image, MCP directory entry, application bundle identifier, Homebrew entry, or configuration convention may be published under that name while [ADR 0023](../adr/0023-working-name-collision-trademark-clearance.md) remains blocking.

## Gate separation

| Gate | Purpose | Evidence required | What the gate does not prove |
| --- | --- | --- | --- |
| Gate 2 — Requirements and architecture | Approve MVP scope, contracts, authority boundaries, risks, ADRs, and verification design | Founder disposition; consistent SRS, traceability, architecture, threat model, test strategy, deployment strategy, and ADR set | No source scaffold, dependency lock, executable command, CI run, package, or implemented behavior is implied |
| Gate 3 — Engineering foundation | Prove the implementation foundation is reproducible and green | Version-pinned toolchains, deterministic dependency locks, formatting, linting, typing, unit/contract test harnesses, CI, hooks, contributor commands, and recorded successful runs | No product feature, real-host accuracy, UAT, package lifecycle, or release readiness is implied |
| Gates 4–8 — Product evidence | Prove runtime, discovery, allocation, UI, MCP, security, and conditional AI behavior | Requirement-linked automated tests, real-machine evidence where required, security review, performance results, and UAT dispositions | No public release is authorized before Gate 9 |
| Gate 9 — Release | Approve a specific, immutable release candidate | Complete checklist, artifact hashes, lifecycle tests, signing and license evidence, name clearance, security review, UAT, and founder approval | Approval applies only to the reviewed candidate |

Gate 3 work started after the explicit Gate 2 disposition. Implemented contributor commands are supported only where [Development setup](../operations/development-setup.md) records successful evidence. The remaining exit proof is defined by [the Gate 3 sprint brief](../project/gate-3-sprint-brief.md).

## Release roles

- **Founder:** approves product scope, Gate 2, release exceptions, public name, and Gate 9.
- **Release manager:** freezes the candidate, assembles evidence, verifies provenance, and stops publication when a blocker appears.
- **QA reviewer:** confirms requirement, test, performance, accessibility, lifecycle, and UAT evidence.
- **Security reviewer:** confirms threat controls, auth, redaction, permissions, dependency findings, and conditional AI posture.
- **Maintainer reviewer:** confirms DCO sign-off, code ownership, documentation truth, license notices, and support readiness.

One person may hold multiple roles, but each required disposition remains explicit in the release record.

## Candidate preparation

### 1. Freeze scope and traceability

- Identify the exact source revision and candidate version.
- Link every included change to issue or work-item IDs and applicable BO, PF, US, SRS, AC, VT-SRS, UAT, ADR, and risk identifiers.
- Update the [traceability matrix](../requirements/traceability-matrix.md) without replacing stable requirement or test IDs.
- Classify every deferred item and user-visible limitation.
- Reject scope that changes authority, persistence, public networking, telemetry, AI permissions, or release identity without the required ADR and founder approval.

### 2. Clear public identity

- Close the evidence and legal-review conditions in [ADR 0023](../adr/0023-working-name-collision-trademark-clearance.md).
- Confirm repository, package, binary, service, bundle, domain, configuration-file, and MCP identities match the accepted public name.
- Repeat collision checks immediately before namespace publication.
- Stop if any relevant conflict or unreviewed name change appears.

### 3. Confirm license and contribution provenance

- Include the official Apache License 2.0 text and every required NOTICE or third-party notice.
- Generate and review dependency and asset license evidence for the candidate.
- Preserve copyright and modification notices required by Apache-2.0.
- Confirm documentation states that Apache-2.0 permits commercial use without payment to the maintainers.
- Confirm sponsorship is voluntary and is not tied to installation, features, commercial use, support eligibility, security handling, or telemetry.
- Verify every contribution after the initial baseline satisfies the Developer Certificate of Origin through a matching `Signed-off-by` trailer.
- Include the founder-approved [forward provenance attestation](../project/gate-2-approval.md#provenance-attestation-for-the-root-commit) for root commit `8081f409f54f088d61f9a36433b7e56f2410e66f`. Do not rewrite the accepted Gate 2 history or report that commit as carrying a trailer it lacks.

### 4. Build the immutable candidate

- Build only from the reviewed source revision and locked inputs.
- Record the exact invocation actually executed, environment profile, tool versions, start and end times, exit status, artifact names, sizes, and cryptographic hashes.
- Produce a software bill of materials and provenance record.
- Sign and notarize only the final candidate artifacts.
- Rebuilding a changed source revision creates a new candidate and invalidates prior approval.

No build or release invocation is specified here. Gate 3 may establish supported contributor quality commands, but only [Development setup](../operations/development-setup.md) may promote them after execution evidence. Release build, package, signing, and publication commands remain Gate 9 concerns.

### 5. Run quality and acceptance evidence

- Execute every mandatory suite in the [test strategy](../testing/test-strategy.md).
- Record the associated VT, AC, and UAT identifiers rather than reporting a generic test pass.
- Run the default core matrix without Docker and without Ollama.
- Run opt-in PostgreSQL, Docker, live macOS, packaging, and AI profiles only when applicable; absence is reported as not executed, never as passing.
- Complete performance, accessibility, compatibility, migration, backup, restore, upgrade, rollback, uninstall, and residue inspections.
- Preserve exact counts, failures, duration, environment, artifact hashes, reviewer disposition, and redacted evidence.

### 6. Complete security and privacy review

- Resolve every Critical and High defect; founder-approved disposition is required for remaining Medium defects.
- Verify loopback binding, local auth, scoped credentials, Origin and CSRF defenses, approved-root enforcement, symlink and traversal defenses, safe subprocess arguments, Docker-socket isolation, and audit integrity.
- Run secret canaries through collection, scanning, persistence, REST, SSE, CLI, MCP, logs, backup, export, diagnostics, and any included AI path.
- Perform an outbound-network audit proving that core operation sends no telemetry, crash report, analytics event, project data, process data, or AI context.
- Inspect the candidate for private keys, tokens, credentials, personal paths, environment values, and unsafe diagnostic samples.
- Handle suspected vulnerabilities privately; do not attach exploit details or secrets to public issues or pull requests.

### 7. Review managed and unmanaged claims

- Describe reservations and atomic leases as coordination among PortAtlas-aware clients.
- Confirm the MVP exposes no source-patching, managed-launch, process-termination, or Docker-lifecycle tool, endpoint, or command.
- Label any future managed-launch assurance as Version 1 scope. It requires its own approved contract and cannot be presented as current MVP behavior.
- State that unmanaged terminals, IDEs, scripts, containers, and applications can ignore the registry or race after a check.
- Reject any UI, API, CLI, MCP, README, release note, marketing, or issue copy that promises zero conflicts for unmanaged launches.

### 8. Decide conditional AI inclusion

If AI is excluded:

- The release notes and UI state that AI is unavailable or not included.
- The core suite passes with Ollama absent, stopped, invalid, and disabled.
- No model is installed, downloaded, activated, or contacted.

If AI is included:

- [ADR 0016](../adr/0016-conditional-ai.md) release gates and AI-EVAL-SAFE-001 pass.
- Read-only permission, prompt-injection, redaction, strict structured output, retention, deletion, local-only provider, timeout, cancellation, and core-isolation evidence pass.
- Generated output remains advisory and cannot mutate authoritative state.
- The exact provider version and model digest are recorded; a model recommendation is not a hidden dependency.

### 9. Validate package lifecycle

The bounded Gate 3 packaging research spike does not satisfy any lifecycle item below. Package implementation, selection, signing, notarization, and lifecycle acceptance begin only in Gate 9 after the spike's hypotheses are reviewed.

- Perform timed clean installation on each supported macOS architecture.
- Verify authentication bootstrap, user-only credential permissions, loopback binding, offline core, start, stop, restart, logs, crash recovery, and degraded integrations.
- Verify upgrade, migration failure recovery, rollback, backup, restore, credential rotation, diagnostic export, uninstall, user-data choice, and residue inspection.
- Confirm uninstall never deletes registered project sources, Docker resources, Ollama models, or global toolchains.

### 10. Approve and publish

- Assemble a release record containing every checklist item, evidence reference, exception, reviewer, and founder disposition.
- Confirm the candidate hashes match the signed artifacts.
- Draft release notes that state supported platforms, known limitations, managed/unmanaged assurance, telemetry policy, AI inclusion state, migration and rollback facts, security contact, license, and voluntary sponsorship.
- Obtain explicit Gate 9 approval for the exact candidate.
- Publish only after approval; any artifact or metadata change restarts the affected review.

## Evidence record

Every release claim must point to reproducible evidence containing:

- candidate version and source revision;
- artifact and SBOM hashes;
- operating-system, architecture, hardware, and dependency profile;
- exact invocation actually executed and exit status;
- requirement, test, AC, VT, and UAT identifiers;
- test counts, failures, duration, and skipped-profile reasons;
- timestamp and accountable reviewer;
- redacted logs, reports, screenshots, or machine-readable artifacts;
- deviations, risk acceptance, rollback decision, and founder disposition.

Screenshots supplement assertions but do not replace them. Secret-bearing logs, full environment files, raw credentials, private paths, complete process arguments, Docker credentials, raw AI prompts, and unredacted repository content are forbidden evidence.

## Abort and rollback

Stop publication for:

- unresolved Critical or High findings;
- missing Must-requirement evidence;
- a failed mandatory test or UAT case;
- name clearance or license uncertainty;
- unsigned, mismatched, or unreproducible artifacts;
- secret exposure or unauthorized network activity;
- incorrect managed/unmanaged claims;
- conditional AI included without its complete gate;
- failed install, migration, rollback, backup, restore, or uninstall evidence.

After publication, a security or data-integrity defect triggers private triage, artifact withdrawal when necessary, user guidance, and a new candidate. Never silently replace a published artifact under the same version.

## Related documents

- [Roadmap and gate map](../product/roadmap.md)
- [MVP checklist](mvp-checklist.md)
- [Versioning policy](versioning.md)
- [QA plan](../testing/qa-plan.md)
- [UAT plan](../testing/uat-plan.md)
- [Threat model](../security/threat-model.md)
- [Local installation contract](../operations/local-installation.md)
- [Backup and restore](../operations/backup-and-restore.md)
