# Agent Working Agreement

This file governs the entire repository. More specific `AGENTS.md` files may narrow these rules in future subdirectories.

## Current gate

The repository is at the founder approval gate after the product and architecture foundation. Until Gate 2 is explicitly approved:

- Do not add production application code or dependencies.
- Do not publish packages, images, manifests, domains, or namespace claims.
- Treat every operational command as a proposed contract unless it has been implemented and verified.
- Keep `PortAtlas` labeled as a working title.

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

## Engineering expectations after approval

- Prefer standard-library tooling for repository checks where practical.
- Add a failing test before implementation for behavior changes.
- Keep collectors, parsers, storage, and external integrations behind interfaces that can be tested with fixtures.
- Preserve accessibility: keyboard access, focus management, semantic structure, and non-color state indicators are release criteria.
- Run `python3 scripts/validate_docs.py`, relevant tests, and `git diff --check` before declaring work complete.

## Contribution safety

Follow [CONTRIBUTING.md](CONTRIBUTING.md), sign commits with the Developer Certificate of Origin, and route suspected vulnerabilities through [SECURITY.md](SECURITY.md). Do not post secrets or exploit details in public issues.
