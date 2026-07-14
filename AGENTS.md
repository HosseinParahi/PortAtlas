# Agent Working Agreement

This file governs the entire repository. More specific `AGENTS.md` files may narrow these rules in future subdirectories.

## Current gate

Gate 2 was founder-approved on 2026-07-11 at exact revision `e53f39916b2348e8626375bb33cac147e27bd217`. Gate 3 [passed on 2026-07-14](docs/project/gate-3-evidence.md) at exact engineering candidate `4adf1fb500b651e425735595db528fd42fffba73`, then was integrated into `main` through administrative closure successor `461243541d6b63ddebf54598c6860ba73abcd012`. Gate 4 planning is isolated on `codex/gate4-runtime-inventory` from that exact planning base. The [Gate 4 sprint brief](docs/project/gate-4-sprint-brief.md) is **Proposed**; Gate 4 behavior must not begin until the founder accepts the brief.

- Keep `codex/gate4-runtime-inventory` planning-only. Do not add runtime-inventory or other Gate 4 behavior before the founder accepts the proposed [Gate 4 sprint brief](docs/project/gate-4-sprint-brief.md).
- Treat [the Gate 3 sprint brief](docs/project/gate-3-sprint-brief.md) and [evidence ledger](docs/project/gate-3-evidence.md) as the historical accepted boundary. Administrative evidence successors do not replace the approved engineering candidate.
- Do not publish packages, images, manifests, domains, or namespace claims.
- Treat every operational command as a proposed contract unless it has been implemented and verified.
- Keep `PortAtlas` labeled as a working title.
- Treat Gate 3 packaging as accepted research evidence only. Distributable artifacts, signing, notarization, service lifecycle, and packaging acceptance belong to Gate 9.

## Product invariants

- Preserve the distinction between managed allocation assurance and unmanaged discovery evidence in requirements, UI copy, APIs, CLI help, MCP instructions, tests, and release notes.
- Keep MVP mutation limited to reservations and atomic leases. Source editing, managed launch, and process termination are deferred.
- Model a logical `Project` separately from each worktree-aware `ProjectInstance`.
- Keep core operation independent of Docker and Ollama. Either integration must be able to degrade without corrupting authoritative state.
- Never add telemetry.
- Keep secrets out of source, fixtures, logs, examples, responses, screenshots, and diagnostic bundles.

## Documentation and traceability

- Use the stable requirement and test namespaces documented under `docs/requirements/` and `docs/testing/`.
- Link product objectives, requirements, architecture components, tests, and release gates when changing scope.
- Record material architectural changes as numbered ADRs rather than silently rewriting accepted decisions.
- Use explicit statuses such as Proposed, Accepted, Deferred, Superseded, or Open.
- Avoid unresolved placeholder markers in committed material.

## Engineering expectations

- Prefer standard-library tooling for repository checks where practical.
- Add a failing test before implementation for behavior changes.
- Keep collectors, parsers, storage, and external integrations behind interfaces that can be tested with fixtures.
- Preserve accessibility: keyboard access, focus management, semantic structure, and non-color state indicators are release criteria.
- Run `python3 scripts/validate_docs.py`, relevant tests, and `git diff --check` before declaring work complete.

## Contribution safety

Follow [CONTRIBUTING.md](CONTRIBUTING.md), sign commits with the Developer Certificate of Origin, and route suspected vulnerabilities through [SECURITY.md](SECURITY.md). Do not post secrets or exploit details in public issues.

The accepted root commit predates sign-off enforcement. Its explicit, non-rewriting provenance disposition is recorded in [Gate 2 founder approval](docs/project/gate-2-approval.md#provenance-attestation-for-the-root-commit); it is not a waiver for later commits.
