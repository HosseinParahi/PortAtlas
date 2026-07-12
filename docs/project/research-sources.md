# Research Sources and Baseline

Core stack research was checked on **2026-07-11** and Gate 3 supply-chain tooling was rechecked on **2026-07-13**. Machine-readable pins and frozen locks are now the contributor authority recorded by `G3-02` and `G3-03`; observations that are not adopted by those files remain planning inputs rather than product requirements.

## Verified machine snapshot

The checkpoint machine reported:

| Capability | Observed state |
|---|---|
| Operating system | macOS 26.5.2 on arm64 |
| Python | 3.14.6 |
| uv | 0.11.25 |
| Node.js | 24.18.0 |
| pnpm | 11.9.0 |
| Docker Engine client | 29.5.3 |
| Docker Compose | 5.1.4 |
| Ollama | Client 0.30.11 present; runtime service unavailable during verification |
| Rust | No `rustc` or `cargo` toolchain found |

This snapshot proves only what was present on one development machine. It must not become a hard-coded compatibility floor, installation promise, or assumption that Docker or Ollama is running.

## Gate 3 toolchain selection

The Gate 3 research pass selected and the evidence run adopted these foundation pins:

| Tool | Gate 3 candidate | Reason and authority |
| --- | --- | --- |
| Python | 3.13.14 | Matches the Accepted Python 3.13 runtime line in ADR 0001; [official Python release](https://www.python.org/downloads/release/python-31314/) |
| Node.js | 24.18.0 LTS | LTS contributor line compatible with the Vite 8 floor; [official Node release](https://nodejs.org/en/blog/release/v24.18.0) |
| uv | 0.11.28 | Exact project/lock manager candidate; [PyPI project record](https://pypi.org/project/uv/0.11.28/) |
| pnpm | 11.10.0 | Exact private-workspace package manager candidate; [npm package record](https://www.npmjs.com/package/pnpm/v/11.10.0) |

These pins do not overwrite the earlier machine snapshot or promise end-user toolchain requirements. The pin/lock files and [Gate 3 evidence](gate-3-evidence.md) take precedence. Gate 9 revalidates the immutable release candidate and its bundled/runtime requirements.

## Gate 3 supply-chain tooling

| Control | Selected baseline and implication | Primary source |
| --- | --- | --- |
| Dependency review | Official Dependency Review Action v5.0.0, pinned to its immutable release commit; pull requests fail for newly introduced High/Critical advisories | [Official v5.0.0 release](https://github.com/actions/dependency-review-action/releases/tag/v5.0.0) |
| Automated updates | Dependabot monitors uv and GitHub Actions weekly. Current official ecosystem support lists uv but lists pnpm only through v10, so the pinned pnpm 11 graph remains a deliberate manual locked update until official support catches up. | [Dependabot ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#package-ecosystem) |
| Python advisory coverage | A hash-locked uv export includes every development group and optional extra before pip-audit checks it. | [pip-audit](https://github.com/pypa/pip-audit) and [uv export](https://docs.astral.sh/uv/reference/cli/#uv-export) |
| Node advisory/license coverage | pnpm audits and inventories production plus development dependencies; the production-only filter is deliberately not used. | [pnpm audit](https://pnpm.io/cli/audit) and [pnpm licenses](https://pnpm.io/cli/licenses) |

## Official stack baseline

| Area | Baseline and implication | Primary source |
|---|---|---|
| Python | 3.14.6 was the current Python 3 release displayed during research. Reverify before locking runtime support. | [Python downloads](https://www.python.org/downloads/) |
| React | 19.2 is the documented current version line. | [React versions](https://react.dev/versions) |
| Vite | Vite 8 is current and documents Node.js 20.19+ or 22.12+ as its supported runtime floor; the machine's Node 24 is a development observation. | [Announcing Vite 8](https://vite.dev/blog/announcing-vite8) |
| Docker | Integrate through the versioned Engine API and negotiated client compatibility, never by scraping Docker Desktop UI. | [Docker Engine API](https://docs.docker.com/reference/api/engine/) and [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/) |
| Host processes | `psutil` is the recommended primary portability layer, with tested `lsof -nP` fallback and cross-validation on macOS. | [psutil documentation](https://psutil.readthedocs.io/en/latest/) |
| MCP | The current protocol revision is 2025-11-25. Streamable HTTP servers must validate Origin, bind locally for local use, and authenticate. | [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25) and [transport security](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) |
| MCP Python SDK | Stable v1 is the implementation baseline and dependency should remain below v2 until v2 is stable and reviewed. | [MCP on PyPI](https://pypi.org/project/mcp/) |
| UI accessibility | Radix primitives provide accessible patterns while retaining styling control; TanStack Table is recommended for inventory scale and keyboard-aware composition. | [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) and [TanStack Table](https://tanstack.com/table/latest) |
| Server state | React Query is recommended for cache invalidation, refetch, and SSE-triggered synchronization rather than duplicating server state in a custom store. | [TanStack Query](https://tanstack.com/query/latest) |
| Packaging | PyInstaller is a research candidate for a native Python service bundle; signing, service lifecycle, and browser bootstrap still require prototypes. | [PyInstaller documentation](https://pyinstaller.org/en/stable/usage.html) |
| Local AI | Ollama can constrain structured output, but PortAtlas must independently validate schemas and treat model output as untrusted. | [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) and [tool calling](https://docs.ollama.com/capabilities/tool-calling) |

## Product comparison

| Product or utility | Primary strength | Gap PortAtlas proposes to address | Positioning lesson |
|---|---|---|---|
| `lsof` and Activity Monitor | Point-in-time operating-system process and socket evidence | No project intent, reservation registry, provenance graph, or conflict workflow | Preserve raw evidence and timestamps; do not pretend a snapshot is ownership |
| Docker Desktop | Rich container-specific runtime visibility and lifecycle | Does not unify host processes, source declarations, worktrees, and local reservations | Use the Engine API as one collector, not Docker as the product's authority |
| [Portless](https://github.com/vercel-labs/portless) | Proxy-first stable local names and automatic routing | Different center of gravity from inventory, evidence, worktree identity, and cross-source conflict analysis | Clearly distinguish PortAtlas from proxy-first products; proxying is not MVP scope |
| [LocalCan](https://www.localcan.com/docs/cli/overview) | Polished local domains, reverse proxy, HTTPS, and service workflows | Focuses on routing and local domains rather than a read-mostly evidence registry | Avoid claiming routing or launch capabilities in MVP |
| portm, portman, and similar small utilities | Quick port lookup, selection, or process actions | Often lack durable provenance, multi-source reconciliation, security boundaries, and worktree modeling | Keep CLI workflows fast while retaining auditable domain semantics |
| Adjacent launchers and development proxies | Convenient process start and friendly URLs | Launch authority creates stronger mutation and security obligations | Defer managed launch, patching, and termination until separately designed |

PortAtlas therefore positions itself as an **inventory, provenance, conflict, reservation, and capacity control plane**. It may report unmanaged evidence, but its strong allocation assurance applies only to PortAtlas-managed reservations and leases.

## Preliminary name and namespace checks

These checks are discovery signals, not legal clearance, availability guarantees, or permission to register anything. Searches used the exact working title and close spacing variants on 2026-07-11.

| Surface | Preliminary result | Interpretation |
|---|---|---|
| Repository search | Exact-title searches found existing user identities and unrelated uses; this repository's remote also already uses the working title. | Identity overlap exists; repository existence does not grant trademark rights. |
| npm | Exact-package web search returned no indexed package result. | Inconclusive until an authenticated registry availability check immediately before release. |
| PyPI | Exact-project web search returned no indexed project result. | Inconclusive; do not reserve or publish. |
| Homebrew | Exact formula and cask search returned no indexed result. | Inconclusive; formula naming policy and live index require later verification. |
| crates.io | Exact-crate web search returned no indexed result. | Rust is not MVP, and the result grants no reservation. |
| Docker Hub | Exact official-image search returned no indexed result. | Organization and image namespaces remain unapproved and unpublished. |
| MCP Registry | Exact indexed search returned no result. | Registry format and naming must be rechecked at release time. |
| Domains | `portatlas.com` resolves to an existing personal site; adjacent domain-intelligence naming also exists. | A matching primary domain is already in use and confusion risk is material. |
| USPTO | Search surfaced `PORT ATLAS`, serial 88346783, for downloadable GIS software and related services, plus official TTAB proceedings. | Software-class overlap is a release blocker requiring professional review. See the [USPTO TTAB inquiry](https://ttabvue.uspto.gov/ttabvue/v?pnam=City+of+Long+Beach++). |
| EUIPO | Public exact-title web indexing produced no reliable official record. | Inconclusive; a professional similarity and class search is still required. |
| WIPO | Public exact-title web indexing produced no reliable Global Brand Database record. | Inconclusive; a professional international search is still required. |

The result is not “name available.” The result is **collision risk confirmed and clearance incomplete**. [ADR-0023](../adr/0023-working-name-collision-trademark-clearance.md) blocks public namespaces until the founder receives adequate clearance or selects a replacement.

## Licensing sources

- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- [Open Source Definition](https://opensource.org/osd)
- [Developer Certificate of Origin 1.1](https://developercertificate.org/)

Apache-2.0 permits commercial use without a usage fee. Voluntary sponsorship is compatible with that model but cannot be represented as a condition of business use.
