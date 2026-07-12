# Gate 2 Founder Approval and Initial-History Provenance

- **Status:** Approved
- **Approval date:** 2026-07-11
- **Approved revision:** `e53f39916b2348e8626375bb33cac147e27bd217`
- **Short revision:** `e53f399`
- **Next gate:** Gate 3 — Engineering foundation

## Founder disposition

The founder explicitly approved the Gate 2 baseline and authorized Gate 3 work on 2026-07-11. The approved object is the exact source revision above, which contains the product, requirements, architecture, security, testing, operations, release, governance, and traceability baseline produced by the [first-checkpoint plan](first-checkpoint-plan.md).

The approval accepts the locked Gate 2 scope and the Accepted ADR outcomes at that revision. It does not:

- declare Gate 3 complete;
- verify any application behavior, dependency lock, build, or contributor command;
- authorize a package, image, manifest, domain, or public namespace publication;
- clear the `PortAtlas` working title for public use;
- accept the Proposed packaging ADR or move packaging lifecycle evidence into Gate 3; or
- approve any later release candidate.

Gate 3 may establish the private engineering workspace and quality foundation. Each Gate 3 claim still needs the evidence in the [Gate 3 sprint brief](gate-3-sprint-brief.md), and the gate closes only through a separate disposition against an exact revision.

## Approved initial history

The approved Gate 2 revision consists of these four ordered commits:

1. `8081f409f54f088d61f9a36433b7e56f2410e66f` — `chore: establish project governance and research baseline`
2. `a970095976592eb870ff745312463e234666e67c` — `docs: define PortAtlas product and requirements`
3. `5ba6889a72795ee39cb86b9d06f01fb4c6f5cd73` — `docs: record architecture security and test strategy`
4. `e53f39916b2348e8626375bb33cac147e27bd217` — `docs: add delivery roadmap and release gates`

Commits two through four carry `Signed-off-by` trailers. The root commit predates enforcement of the repository contribution instructions and has no `Signed-off-by` trailer.

## Provenance attestation for the root commit

The founder approved a forward provenance record for commit `8081f409f54f088d61f9a36433b7e56f2410e66f` instead of rewriting the accepted initial history.

For project-governance purposes, this record attests that:

- the root commit is the founder-originated governance and research baseline accepted as part of the exact Gate 2 revision;
- the contribution is accepted under Apache-2.0 and the Developer Certificate of Origin 1.1 contribution policy;
- no third-party application code or dependency payload is represented as part of that documentation baseline;
- the missing trailer is a recorded initial-history exception, not a waiver for later commits; and
- the commit object is retained unchanged so its hash and the approved Gate 2 revision remain stable.

This attestation is a transparent governance record, not a retroactive Git trailer or cryptographic signature. All later commits remain subject to the sign-off rule in [CONTRIBUTING.md](../../CONTRIBUTING.md#developer-certificate-of-origin). A future release provenance review must include this record and must not report the root commit as having a trailer it does not have.

## Gate 3 authorization boundary

The approval permits implementation of the Gate 3 engineering foundation on `codex/gate3-engineering-foundation`. It does not relax the product invariants in [AGENTS.md](../../AGENTS.md), especially the managed-versus-unmanaged assurance boundary, reservation/lease-only MVP mutation, Docker and Ollama independence, no telemetry, secret safety, and the working-name publication block.
