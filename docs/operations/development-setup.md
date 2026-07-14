# Development Setup

Status: **Verified contributor guide accepted with Gate 3 on 2026-07-14 at exact engineering candidate [`4adf1fb500b651e425735595db528fd42fffba73`](../project/gate-3-evidence.md); Gate 4 planning only, with behavior gated on founder acceptance of its proposed sprint brief**

This guide covers the accepted private engineering foundation only. It is not an end-user installation, runtime-inventory, service-lifecycle, or release-packaging guide. The exact-revision evidence is recorded in the [Gate 3 ledger](../project/gate-3-evidence.md).

## Pinned contributor tools

| Tool | Required Gate 3 value | Authority |
| --- | --- | --- |
| CPython | 3.13.14 default; 3.14.6 compatibility matrix | `.python-version` and CI matrix |
| uv | 0.11.28 | `scripts/check.py` and CI setup |
| Node.js | 24.18.0 | `.node-version` and root `package.json` |
| pnpm | 11.10.0 | Corepack `packageManager` and root `package.json` |

These are contributor inputs, not product-runtime promises. Do not modify system Python, global shell profiles, Docker settings, or user-wide package configuration for this repository.

## First bootstrap

Install the pinned uv and Node/Corepack prerequisites through their official mechanisms, then run from the repository root:

```bash
uv python install 3.13.14
corepack enable
python3 scripts/check.py toolchains
python3 scripts/check.py bootstrap
```

`toolchains` executes the selected Python and compares every tool to the exact pin. `bootstrap` rejects Python lock drift, performs locked Python and frozen pnpm synchronization, and installs both the pre-commit and commit-message hooks. It requires registry access only when locked content is not already cached.

The default Python environment includes the `dev` group and excludes Docker, host-collector, MCP, PostgreSQL, and packaging extras. Default tests use temporary SQLite and synthetic fixtures.

## Offline locked repeat

After the locked content has been cached, the dependency repeat is:

```bash
uv sync --locked --offline --group dev --python 3.13.14
corepack pnpm install --frozen-lockfile --offline
```

Both commands fail rather than resolve a changed manifest. `uv lock --check` is also executed by bootstrap and hosted Python jobs.

## Supported command surface

Every command below is implemented by `scripts/check.py` and propagates the first non-zero exit status.

| Command | Scope |
| --- | --- |
| `python3 scripts/check.py fast` | Documentation, foundation metadata, Python/TypeScript formatting |
| `python3 scripts/check.py docs` | Documentation validator and its standard-library regression suite |
| `python3 scripts/check.py foundation` | Private metadata, locks, fixtures, workflow pins, test IDs, no telemetry/publication |
| `python3 scripts/check.py dco` | Matching DCO trailers for commits after the accepted Gate 2 revision |
| `python3 scripts/check.py format-check` | Ruff and Prettier check mode |
| `python3 scripts/check.py lint` | Ruff, import architecture, peer validation, and ESLint |
| `python3 scripts/check.py typecheck` | Strict mypy and TypeScript checks |
| `python3 scripts/check.py test-core` | Default Python suites and minimum 85% coverage; no live optional service |
| `python3 scripts/check.py test-web` | API-client and React unit/component/accessibility tests |
| `python3 scripts/check.py contracts` | OpenAPI authority and generated-client drift |
| `python3 scripts/check.py security` | Repository secret, personal-path, workflow, dependency-policy, and telemetry checks |
| `python3 scripts/check.py isolation` | Optional-module, process/network-import, and Rust-artifact exclusion |
| `python3 scripts/check.py service-smoke` | Ephemeral loopback liveness/request-ID smoke with automatic shutdown |
| `python3 scripts/check.py build` | Private Python metadata build plus browser/client build; publishes nothing |
| `python3 scripts/check.py all` | Mandatory default aggregate in the order documented above |

The aggregate intentionally excludes network advisory queries, license inventory, live PostgreSQL, and the packaging research group. Those profiles are separate so everyday core work stays deterministic without Docker, PostgreSQL, Ollama, Rust, or packaging tools.

The Python build synchronizes the committed `build` dependency group, then creates ignored wheel/source-distribution metadata with build isolation disabled so the exact locked Hatchling backend is used. It proves packaging metadata and imports are coherent; it is not the native packaging spike, an installable product, or a publishable artifact.

## Network-dependent supply-chain checks

Run these after the default aggregate:

```bash
python3 scripts/check.py audit
python3 scripts/check.py licenses
```

`audit` checks all locked Python runtime, development, build, optional, PostgreSQL, and packaging dependencies plus all Node production/development dependencies. `licenses` temporarily synchronizes every locked Python group/extra and inventories the same Python and Node scope; both inventories reject AGPL/SSPL findings and remain mandatory human-review inputs. Restore and prove the default path afterward:

```bash
uv sync --locked --group dev --python 3.13.14
python3 scripts/check.py isolation
```

Registry or advisory-service failure is a failed or not-executed profile, never a clean audit result. See [SECURITY.md](../../SECURITY.md) for the vulnerability and license policy.

## Python compatibility profile

CI executes the Python quality, test, isolation, service-smoke, and private-build path on both supported contributor interpreters. A local compatibility run selects the second interpreter without changing the default pin:

```bash
PORTATLAS_PYTHON_VERSION=3.14.6 python3 scripts/check.py typecheck-python
PORTATLAS_PYTHON_VERSION=3.14.6 python3 scripts/check.py test-core
PORTATLAS_PYTHON_VERSION=3.14.6 python3 scripts/check.py service-smoke
```

Restore the default environment with the locked synchronization command before continuing ordinary work.

## Optional PostgreSQL compatibility profile

The PostgreSQL test requires an explicitly supplied, disposable, credential-free test URL through `TEST_POSTGRES_URL`. It runs the same Alembic head migration and repository/UoW seam in an isolated schema. CI provides PostgreSQL 18.3 from a digest-pinned service image.

```bash
uv sync --locked --group dev --extra postgres --python 3.13.14
uv run --locked --python 3.13.14 pytest -m postgres
uv sync --locked --group dev --python 3.13.14
```

The middle command reports a skip when `TEST_POSTGRES_URL` is absent. A skip is not a compatibility pass. The profile does not make PostgreSQL a supported end-user mode and never silently falls back from PostgreSQL to SQLite.

## Bounded packaging research profile

Gate 3 permits only the disposable experiment documented in [Gate 3 native packaging research](../project/gate-3-packaging-research.md):

```bash
uv sync --locked --group dev --group packaging --python 3.13.14
python3 scripts/packaging_spike.py
uv sync --locked --group dev --python 3.13.14
python3 scripts/check.py isolation
```

The script builds inside an automatically deleted temporary directory and may print a local measurement. It does not retain, sign, notarize, install, upload, or publish an artifact. Packaging selection and lifecycle acceptance remain Gate 9.

## Failure behavior and local outputs

- A missing executable returns 127 with bootstrap guidance.
- A stale Python lock, frozen pnpm mismatch, generated-contract change, failing test, or validator finding returns non-zero.
- Tests isolate filesystem and SQLite state in temporary directories.
- Service smoke binds only an ephemeral loopback port and always terminates its child process.
- Ignored local outputs include `.venv`, `node_modules`, coverage data, private build metadata under `dist`, and browser output under `apps/web/dist`.
- No supported contributor command publishes a package, reserves a namespace, sends telemetry, installs a model, or changes Docker resources.

End-user installation, authentication bootstrap, background service lifecycle, upgrade, rollback, backup, restore, and uninstall remain proposed contracts until Gate 9 evidence exists.
