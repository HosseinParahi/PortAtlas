# Test Data Strategy

Status: **Proposed pre-implementation contract**

Gate 3 establishes only versioned synthetic fixture-family catalogs with deterministic seeds, sensitivity labels, and owning test IDs. Scenario payloads, labeled golden outputs, and corpus thresholds are implemented and accepted in their owning Gates 4–8; the catalogs alone do not claim collector, parser, allocator, UI, or AI behavior.

## Principles

- Synthetic by default, deterministic from a recorded seed, and safe to publish
- No copied founder repositories, home paths, real tokens, or proprietary process arguments
- Labeled ground truth for every expected declaration and non-declaration
- Adversarial cases separated from benign controls
- Versioned fixtures with explicit parser and schema ownership

## Fixture families

| Family | Contents | Labels |
|---|---|---|
| Host observations | TCP/UDP, IPv4/IPv6, wildcard/loopback, PID reuse, permission loss, process exit races | Expected normalized endpoint, identity confidence, freshness |
| Docker | Published/bound ports, multiple networks, stopped/running states, API versions, permission and daemon errors | Expected container evidence and degraded state |
| Project identity | Git roots, monorepos, nested roots, clones, detached heads, two or more worktrees | Expected `Project` and `ProjectInstance` relationships |
| Scanner corpus | Compose, Dockerfile, safe environment keys, package scripts/workspaces, Vite/Next/Nuxt/SvelteKit, Python commands and `pyproject.toml`, Tauri, Makefile, Taskfile, Procfile, justfile | Exact declaration positions, protocols, confidence, unsupported variants |
| Filesystem attacks | Symlink escapes/cycles, large and sparse files, deep trees, invalid encodings, special files, renamed files | Expected skip or safe typed error |
| Allocator | Boundaries, exclusions, exhaustion, concurrent claims, expiry, renew, release, retries, stale revisions | Expected deterministic candidate or typed conflict |
| Security canaries | Synthetic provider tokens, private-key markers, credential URLs, sensitive paths, misleading names | Expected zero output and redaction category |
| UI and capacity | 500 projects, 2,000 declarations, 1,000 observations, conflicts, degraded collectors, empty states | Expected row counts, filters, states, provenance paths |
| AI evaluation | Grounded questions, malicious instructions, invalid schemas, fabricated IDs, slow/disconnected provider | Expected rejection or validated structured result |

## Corpus governance

Each fixture has a manifest containing format version, purpose, generated seed, expected outputs, sensitive-data classification, and owning test IDs. A parser change that updates a golden result must explain whether the specification, parser, or prior expectation changed. Reviewers inspect semantic diffs rather than mechanically accepting regenerated output.

## Real-project validation

Founder-selected projects may be used only in a local, non-committed acceptance profile. The harness records aggregate counts and anonymized miss categories, not source contents or absolute paths. Any example promoted to the repository is recreated synthetically.

## Time and concurrency

Unit tests use an injected clock and deterministic scheduler where possible. Integration tests include real transaction and cancellation races with repeated seeds. A failure must print the safe seed and operation schedule needed to reproduce it.
