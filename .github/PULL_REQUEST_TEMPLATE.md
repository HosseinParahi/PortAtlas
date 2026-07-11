# Pull request

Do not include secrets, credentials, environment files, private project content, personal paths, raw AI prompts, complete process arguments, unredacted diagnostics, or vulnerability exploit details. Security-sensitive work must use the repository's private disclosure and review path.

## Summary

- User or maintainer outcome:
- Scope included:
- Scope intentionally excluded:
- Risk and rollback summary:

## Gate and change classification

Select the applicable stage. Gate 2 approves contracts; Gate 3 separately proves executable toolchains and green CI. Documentation approval is not evidence that implementation commands work.

- [ ] Gate 2 documentation or architecture
- [ ] Gate 3 engineering foundation
- [ ] Gate 4–8 product implementation or verification
- [ ] Gate 9 packaging or release
- [ ] Non-product repository governance

Change areas:

- [ ] Requirements, product, or UX
- [ ] Architecture, ADR, domain, or data
- [ ] Collector, scanner, allocator, or conflict engine
- [ ] REST, SSE, CLI, MCP, or UI
- [ ] Authentication, security, privacy, or redaction
- [ ] Persistence, migration, backup, or restore
- [ ] Conditional AI
- [ ] Packaging, release, or open-source governance

## Traceability

- Issue or work-item IDs:
- BO, PF, and US IDs:
- SRS IDs:
- AC, VT-SRS, UAT, and test-suite IDs:
- ADR and risk IDs:
- Traceability-matrix rows changed:

If this introduces new behavior without stable IDs, update the requirement and traceability sources in this pull request before requesting approval.

## Product truth

- [ ] Observed, declared, reserved, leased, desired, conflicted, stale, unknown, and ignored meanings remain distinct where relevant.
- [ ] Reservations and leases are described as coordination among PortAtlas-aware clients.
- [ ] The MVP exposes no source-patching, managed-launch, process-termination, or Docker-lifecycle tool, endpoint, or command.
- [ ] Any proposal for managed launch is explicitly Version 1 scope and has a separate approved contract.
- [ ] Unmanaged processes are described as able to ignore or race the registry; no surface promises zero conflicts for unmanaged launches.
- [ ] Evidence, confidence, freshness, and permission limits are preserved.

If these checks are not applicable, explain why:

## Security and privacy review

- [ ] No secret, credential, token, cookie, private key, database URL, personal path, private source, raw prompt, or unredacted diagnostic was added.
- [ ] Filesystem, symlink, subprocess, process, Docker, network, auth, MCP, and mutation authority were reviewed where applicable.
- [ ] Inputs, outputs, timeouts, concurrency, retries, errors, logs, and audit records are bounded and redacted.
- [ ] Local HTTP and MCP remain loopback-only by default with the required auth and Origin protections.
- [ ] No telemetry, analytics, crash upload, or automatic remote data flow was introduced.
- [ ] Security tests or documented threat-model analysis cover the change.

Security-review evidence:

## Conditional AI

Select one:

- [ ] No AI impact
- [ ] AI excluded from this candidate; core behavior and tests require no provider
- [ ] Optional AI included but disabled by default; complete AI release gate attached

For an included AI change:

- [ ] Deterministic core behavior remains authoritative and works with Ollama absent.
- [ ] AI has only the fixed read-only capability set and cannot mutate state, run shell commands, read arbitrary files, control processes, or broaden roots.
- [ ] Context minimization, redaction, prompt-injection defense, strict structured output, evidence validation, retention, deletion, failure isolation, and resource bounds are verified.
- [ ] Provider version and model digest are recorded; no provider or model is installed, downloaded, activated, or contacted automatically.

AI evidence or exclusion rationale:

## Public name, license, and sponsorship

- [ ] The change treats PortAtlas as a working title and creates no public namespace or trademark claim while ADR 0023 is blocking.
- [ ] Any package, executable, service, bundle identifier, manifest filename, domain, or registry impact is listed.
- [ ] Apache-2.0 notices and dependency or asset license obligations were reviewed where applicable.
- [ ] Copy states that Apache-2.0 permits commercial use without payment when licensing is discussed.
- [ ] Sponsorship is voluntary and is not tied to use, features, commercial permission, updates, support, security handling, or telemetry.

Identity and license impact:

## Verification evidence

Record only invocations actually executed. Do not copy a planned command from documentation and present it as passing evidence.

| Exact executed invocation or manual procedure | Requirement or test IDs | Environment profile | Result and counts | Redacted evidence |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Also record:

- Source revision:
- Started and completed timestamps:
- Artifact or report hashes:
- Skipped profiles and reason:
- Failure, flake, warning, and exception disposition:

## Data, migration, and lifecycle

- [ ] No stored-data or configuration impact
- [ ] Migration and compatibility impact documented and tested
- [ ] Backup, restore, upgrade, rollback, and uninstall behavior reviewed where applicable
- [ ] User-owned project sources and external Docker or Ollama resources remain untouched unless separately and explicitly authorized

Details:

## Accessibility and documentation

- [ ] No user-interface impact
- [ ] Keyboard, focus, screen-reader, non-color state, contrast, motion, and responsive behavior reviewed where applicable
- [ ] Requirements, architecture, security, testing, operations, and release documentation match the change
- [ ] Every user or contributor invocation described as working was executed in the stated environment

Evidence and document links:

## Reviewer prompts

- Which requirement or risk remains least directly evidenced?
- Could any copy overstate managed assurance or hide an unmanaged race?
- Could any input, log, diagnostic, screenshot, AI context, or fixture disclose sensitive data?
- Does this change add network, Docker, process, filesystem, mutation, telemetry, or AI authority?
- Does Gate 2 documentation get mistaken for Gate 3 implementation evidence?
- Does the working-title gate or Apache-2.0/sponsorship policy need another review?

## DCO certification

- [ ] Every commit in this pull request carries a Developer Certificate of Origin Signed-off-by trailer matching its contributor.
- [ ] I have the right to submit these changes under the project's Apache-2.0 contribution terms.

See the [Developer Certificate of Origin](https://developercertificate.org/) for the attestation represented by Signed-off-by.
