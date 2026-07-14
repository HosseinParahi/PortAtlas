# Gate 3 Engineering Foundation Evidence

- **Status:** **OPEN** — local and hosted engineering evidence complete; exact-revision founder approval pending
- **Evidence date:** 2026-07-14
- **Gate 2 input:** [`e53f39916b2348e8626375bb33cac147e27bd217`](gate-2-approval.md)
- **Working branch:** `codex/gate3-engineering-foundation`
- **Immutable engineering candidate:** `4adf1fb500b651e425735595db528fd42fffba73`
- **Internal version authority:** `pyproject.toml` value `0.0.0.dev0`
- **Public release status:** None; PortAtlas remains a working title

## Disposition rule

This ledger records the bounded engineering foundation in the [Gate 3 sprint brief](gate-3-sprint-brief.md). Local and hosted passes do not close the gate. The immutable engineering candidate is `4adf1fb500b651e425735595db528fd42fffba73`; its push and pull-request workflow evidence is recorded below. Gate 3 remains **OPEN** until the founder explicitly approves that exact revision. The founder's 2026-07-13 direction authorized continuation toward Gate 3 closure; it was not exact-revision approval and waives no failed check, later-gate exclusion, name gate, or exact-revision requirement.

Any later commit that records this completed evidence is an administrative evidence successor. It is not the tested engineering candidate and does not replace the exact revision to which the hosted evidence and pending founder disposition apply.

The foundation includes contracts and test seams only. It does not claim working host or Docker inventory, project discovery, parsers, allocation, product REST resources, SSE, production MCP, optional AI behavior, package lifecycle, or release readiness.

## Evidence environment

| Evidence input | Observed value |
| --- | --- |
| Host profile | macOS 26.5.2, arm64 |
| Project Python | CPython 3.13.14 |
| Compatibility Python | CPython 3.14.6 |
| Documentation command driver | CPython 3.14.6 |
| uv | 0.11.28 |
| Node.js | 24.18.0 |
| pnpm | 11.10.0 through Corepack |
| Default database | Temporary SQLite; no live service |
| Default Docker/Ollama/Rust/packaging use | None |

These are contributor and evidence inputs, not end-user runtime promises. Exact toolchain pins live in `.python-version`, `.node-version`, `package.json`, and `scripts/check.py`.

## Locked and generated inputs

| File | SHA-256 | Disposition |
| --- | --- | --- |
| `uv.lock` | `7a2188940c6a1cc795b927eefbc5ab916c14a20d2341b059ec75d02d0873c893` | Locked Python runtime, development, build-backend, optional-integration, PostgreSQL, and packaging research graph |
| `pnpm-lock.yaml` | `dfd2d33f46a2cab944430e91358ba8401e137653a38de01eee33dee8bfdfd944` | Locked private browser/client workspace graph |
| `contracts/openapi/v1.json` | `fe1ff9203de5b8895fcc20d46de19dce747ee75f4a1b640a16b690f5a6bfcf91` | Generated minimal REST foundation contract |
| `packages/api-client/src/generated/openapi.ts` | `f8d3d044fc53a10199c03ee35cc77bfe90246a8de21f7302c45f54ca47fa9de6` | Generated private client types |

Both workspace manifests are private, the Python classifier says `Private :: Do Not Upload`, no publication configuration exists, and CI contains no artifact upload or publication step.

## Local verification results

| Command or profile | Result | Measured evidence |
| --- | --- | --- |
| `python3 scripts/check.py toolchains` | Passed | Selected Python 3.13.14 was executed; uv, Node, and pnpm matched exact pins |
| `python3 scripts/check.py all` | Passed | Complete default aggregate in 25.49 seconds; no Docker, PostgreSQL, Ollama, Rust, or packaging-research dependency used |
| `python3 scripts/check.py test-core` | Passed | 101 passed, 1 PostgreSQL test deselected, 87.63% branch-aware coverage; pytest 2.40 seconds |
| `python3 scripts/check.py test-web` | Passed | API client 4 tests in 233 ms; browser 7 tests in 1.72 seconds |
| `python3 scripts/check.py contracts` | Passed | OpenAPI and generated-client drift checks both current |
| Python format, lint/import architecture, and strict type commands | Passed | Ruff, two import-linter contracts, and mypy over 46 source files |
| Web format, peer, lint, and strict type commands | Passed | Both private workspaces clean |
| `python3 scripts/check.py build-web` | Passed | 130 modules; JavaScript 316.64 kB and 96.45 kB gzip; Vite build 147 ms |
| Frozen offline install profile | Passed | Clean external Python environment and rebuilt pnpm workspace installed only from committed locks and existing local stores |
| Python 3.14.6 compatibility profile | Passed | Format/lint architecture, strict typing, isolation, 101 core tests in 4.89 seconds, loopback smoke, and no-isolation private build |
| PostgreSQL 18.3 compatibility profile | Passed | One Alembic migration plus shared repository/UoW round trip passed; 99 non-PostgreSQL tests deselected |
| Disposable packaging repeat | Passed | 24,251,708-byte arm64 tree, SHA-256 `281329a5456e0acd101705b50fb1e11195a1b17f6e4fe4cac99f53b166c82b4e`; version/help passed and no artifact retained |
| Local hooks | Passed | Bootstrap installed pre-commit and commit-message hooks; all-file pre-commit execution passed |
| `python3 scripts/check.py audit` | Passed | Every locked Python group/extra, including the build backend, and all Node production/development dependencies; no known advisories |
| `python3 scripts/check.py licenses` | Passed after full-profile hydration | Complete Python inventory and 394 Node packages across 12 license expressions; automated AGPL/SSPL policy found no violation |
| `python3 scripts/check.py isolation` after restoring the default environment | Passed | Optional Python modules absent; production source has no process/network integration import; no Rust artifact |

Commands outside the aggregate that can reach registries or optional services remain deliberately separate. Local evidence is complete for exact engineering candidate `4adf1fb500b651e425735595db528fd42fffba73`. Hosted push CI, pull-request CI, dependency review, the macOS packaging-research repeat, the aggregate, and the clean post-commit Git observation are recorded below. Gate 3 remains **OPEN** pending exact-revision founder approval, and Gate 4 product behavior remains blocked.

## License and vulnerability disposition

- No Python or Node advisory was reported on 2026-07-13.
- Python inventory includes runtime, development, Docker, host, MCP, PostgreSQL, and packaging-research dependencies. Node inventory includes production and development tooling.
- PyInstaller and its hook contribution package report GPLv2-related metadata. They remain non-default research tools; PyInstaller's bootloader exception and any selected packager receive Gate 9 review.
- psycopg reports LGPL-3.0-only and Hypothesis, certifi, pathspec, axe-core, and Lightning CSS report MPL-family licenses. These are recorded review inputs, not a release NOTICE or SBOM.
- Automated policy blocks AGPL and SSPL findings. Every dependency and asset is re-reviewed for the immutable release candidate.

## Work-item ledger

| Work item | Evidence | Candidate disposition |
| --- | --- | --- |
| G3-00 | Founder-approved Gate 2 revision, branch, exclusions, and forward root-commit provenance attestation | Accepted |
| G3-01 | Sprint brief plus this one complete bounded ledger | Candidate-local accepted |
| G3-02 | Exact machine-readable pins and executed toolchain validation | Candidate-local accepted |
| G3-03 | Private manifests, committed locks, uv lock check, clean offline Python sync, and pnpm frozen offline install | Candidate-local accepted |
| G3-04 | Typed modular-monolith packages, import-linter contracts, and sibling-adapter AST rule | Candidate-local accepted |
| G3-05 | Opaque IDs, clocks, revisions, `PortKey`, `Project`, and `ProjectInstance` unit tests | Candidate-local accepted |
| G3-06 | Reusable repository/UoW fakes, SQLite adapter, migration/metadata drift test, and PostgreSQL 18.3 migration/repository compatibility pass | Candidate-local accepted |
| G3-07 | Required configuration schema version, strict keys, loopback host/origin bounds, platform paths, no telemetry, and secret exclusion tests | Candidate-local accepted |
| G3-08 | Token entropy/hash/expiry/revocation, scopes, user-only files, immutable secret-safe error values, and authenticated readiness primitives | Candidate-local accepted |
| G3-09 | Inward CLI/MCP/host/Docker/scanner/provider interfaces, protocol revision constant, and optional-import isolation | Candidate-local accepted |
| G3-10 | Minimal liveness and authenticated readiness, canonical errors, safe request IDs, versioned OpenAPI, and correct degraded-response schema | Candidate-local accepted |
| G3-11 | Strict React shell, Query/Table/Radix wrappers, managed/unmanaged copy, axe, keyboard/focus, core-unavailable, compact-layout, and reduced-motion tests | Candidate-local accepted |
| G3-12 | `pyproject.toml` authority drives service import metadata, CLI, REST/OpenAPI, and generated contract checks | Candidate-local accepted |
| G3-13 | Unit, contract, integration, architecture, security, and web harnesses execute with deterministic local inputs | Candidate-local accepted |
| G3-14 | Eight versioned synthetic fixture-family catalogs with benign, degraded, adversarial, sensitivity, seed, and defined test-ID metadata; behavioral payloads remain in owning gates | Candidate-local accepted |
| G3-15 | One documented command dispatcher covers bootstrap, quality, contracts, security, isolation, service smoke, and builds | Candidate-local accepted |
| G3-16 | Installed pre-commit and commit-message hooks, successful all-file hook run, SHA-pinned least-privilege CI, and PR-head-safe exact-history DCO job | Engineering evidence complete; hosted CI, exact-history DCO, and aggregate successful |
| G3-17 | Default optional-module absence, static process/network/Rust exclusion, and failing Docker/AI adapters leaving authoritative SQLite state unchanged | Candidate-local accepted |
| G3-18 | Expanded secret scan, lock checks, digest/action pins, locked build backend, full advisory/license inventory, dependency-review workflow, and Dependabot for supported ecosystems | Engineering evidence complete; hosted dependency review successful on PR attempt 2 |
| G3-19 | Dated toolchain, dependency-review, update-tooling, packaging, and later-gate research dispositions | Candidate-local accepted |
| G3-20 | Repeated disposable native bundle feasibility and Gate 9 experiment plan in the packaging memo | Engineering evidence complete; hosted macOS packaging-research repeat successful on PR attempt 2 |
| G3-21 | Exact candidate revision, complete final command durations, hosted CI URLs, clean Git state, and founder binding | **OPEN** — engineering evidence complete; exact-revision founder approval pending |

## Optional and deferred profiles

- **PostgreSQL:** An explicit disposable PostgreSQL 18.3 profile tests the same Alembic migration and repository/UoW seam. It is never part of default bootstrap and does not make PostgreSQL a product mode.
- **Docker:** No Docker SDK or daemon call occurs in default checks. Only the interface, synthetic fixtures, and failure isolation exist; runtime collection belongs to Gate 4.
- **Ollama/local AI:** No provider is installed or called by default. Only a failure-isolated protocol exists; AI inclusion remains conditional Gate 8 scope.
- **Rust/Tauri:** No Rust source, manifest, compiler call, or Tauri shell exists. Tauri remains Version 1.
- **Packaging:** PyInstaller is in a non-default group used only by the automatically deleted research spike. No retained, signed, notarized, installed, or published artifact exists.

## Residual risks and exclusions

- Real macOS process/socket fidelity, permissions, and `psutil`/`lsof` cross-validation are Gate 4 evidence.
- Real Docker Engine negotiation and degradation are Gate 4 evidence.
- Scanner safety and parser accuracy are Gate 5 evidence.
- Reservation/lease concurrency and conflict behavior are Gate 6 evidence.
- Primary browser workflows and full accessibility/UAT are Gate 7 evidence.
- Production MCP and conditional local AI are Gate 8 evidence.
- Packaging selection, clean-machine lifecycle, signing, notarization, SBOM, provenance, upgrade, recovery, and uninstall are Gate 9 evidence.
- The public-name gate remains blocking. No package, image, domain, manifest, Homebrew, MCP Registry, or other namespace was published by this checkpoint.

## Exact-revision closure

The immutable engineering candidate is `4adf1fb500b651e425735595db528fd42fffba73`. It is the revision evaluated by the hosted runs associated with [pull request 1](https://github.com/HosseinParahi/PortAtlas/pull/1).

| Closure input | Recorded evidence | Disposition |
| --- | --- | --- |
| Hosted push CI | [Run 29315789627](https://github.com/HosseinParahi/PortAtlas/actions/runs/29315789627) | `success` for the exact engineering candidate |
| Hosted pull-request CI | [Run 29315801647, attempt 2](https://github.com/HosseinParahi/PortAtlas/actions/runs/29315801647/attempts/2) | `pull_request` event for head SHA `4adf1fb500b651e425735595db528fd42fffba73`; started `2026-07-14T07:50:12Z`, completed `2026-07-14T07:51:26Z`; all 11 jobs succeeded, including dependency review and the Gate 3 aggregate |
| Clean Git state | Observation at `2026-07-14T07:52:53Z` | `HEAD`, local branch `codex/gate3-engineering-foundation`, and upstream `origin/codex/gate3-engineering-foundation` all resolved to `4adf1fb500b651e425735595db528fd42fffba73`; ahead/behind was `0/0`; no worktree path records were present |
| Founder exact-revision approval | No approval bound to `4adf1fb500b651e425735595db528fd42fffba73` is recorded as of the evidence date | **OPEN** |

These records complete the hosted engineering evidence; they do not constitute founder approval, a passed or closed gate, or authorization for Gate 4 behavior. Gate 3 remains **OPEN** pending founder approval explicitly bound to `4adf1fb500b651e425735595db528fd42fffba73`, and Gate 4 product behavior remains blocked. Any later documentation commit containing this record is an administrative evidence successor, not the tested engineering candidate. PortAtlas remains a working title, and no package, image, manifest, domain, release artifact, or public namespace was published.
