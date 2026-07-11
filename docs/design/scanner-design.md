# PortAtlas Scanner Design

## Objective

The scanner discovers projects and exact or high-value port declarations inside user-approved roots. It favors focused deterministic parsers with evidence over broad source scanning. It never executes project code, imports project modules, expands scan scope from repository instructions, or persists unrelated environment values.

## Pipeline

~~~mermaid
flowchart LR
    ROOT[Approved ProjectRoot]
    TRAV[Bounded traversal]
    ID[Project and ProjectInstance identification]
    CAND[Candidate selection]
    PARSE[Focused parser]
    VALID[Validation and redaction]
    EVID[DiscoveryEvidence]
    RECON[Declaration reconciliation]
    CONFLICT[Conflict recomputation]

    ROOT --> TRAV
    TRAV --> ID
    ID --> CAND
    CAND --> PARSE
    PARSE --> VALID
    VALID --> EVID
    EVID --> RECON
    RECON --> CONFLICT
~~~

## Approved-root enforcement

Before file access:

1. Load the active ProjectRoot and its revision.
2. Canonicalize the root through platform path APIs.
3. Apply configured symlink policy.
4. Canonicalize each candidate.
5. Verify containment under the approved root.
6. Reject traversal, device files, sockets, and unsupported file types.
7. Enforce sensitive-path and hidden-directory rules.

Symlinks are rejected by default. When enabled, the resolved target must still remain within the approved root unless a separately approved root covers it.

## Traversal budgets

Each root policy sets:

- maximum recursion depth;
- maximum directories and files;
- maximum candidate file size;
- maximum total bytes parsed per run;
- maximum scan duration;
- include patterns;
- exclude patterns;
- hidden-file handling;
- symlink handling;
- filesystem-watcher behavior.

Built-in excludes include .git, node_modules, Python environments, build outputs, dependency caches, package stores, generated artifacts, and common binary directories. The preview endpoint shows effective scope and exclusions before registration.

## Project discovery

Detectors identify:

- Git repository and worktree markers without requiring network access;
- workspace roots from supported package manifests;
- nested services;
- Docker Compose projects;
- Tauri projects;
- framework markers;
- manually registered non-Git directories.

Project is the logical family. ProjectInstance is the concrete checkout or worktree. Monorepo services remain under the instance unless explicit evidence supports a nested separately runnable ProjectInstance.

Identity evidence can include:

- user or project manifest identity;
- Git common-directory relationship;
- local repository fingerprint;
- worktree metadata;
- filesystem identity;
- canonical path;
- user-confirmed relationship.

Remote URL is optional evidence and does not require GitHub access.

## Parser contract

~~~python
class ProjectParser(Protocol):
    descriptor: ParserDescriptor

    def supports(self, candidate: CandidateFile) -> bool: ...

    async def parse(
        self,
        source: SafeSource,
        context: ParseContext,
    ) -> ParseResult: ...
~~~

ParserDescriptor contains ID, version, exact filenames or bounded patterns, supported syntax versions, maximum input size, and evidence capabilities.

ParseResult contains:

- declarations;
- service candidates;
- database or infrastructure dependency hints;
- DiscoveryEvidence;
- confidence;
- safe warnings;
- completeness;
- references to unresolved variables by name only.

Unknown fields and unsupported syntax remain explicit. A parser never guesses by scanning every numeric literal.

## Focused MVP parser catalog

### Tier 1: exact deployment and environment declarations

- compose.yaml, compose.yml, docker-compose.yaml, docker-compose.yml, and conventional override files;
- Dockerfile EXPOSE;
- .env variants using a strict allowlist of port-related keys and service context;
- Tauri configuration fields containing development URLs.

Compose parsing distinguishes host publications, container ports, protocol, interface, variable substitution, ranges, and short or long syntax. Unresolved substitutions produce partial declarations with evidence, not fabricated values.

### Tier 2: recognized launch and framework configuration

- package.json scripts using a shell lexer and recognized server command flags, plus workspace boundaries;
- Vite server.port and preview.port through a focused syntax strategy;
- Next, Nuxt, and SvelteKit known CLI and configuration fields;
- pyproject.toml script metadata;
- recognized Uvicorn, FastAPI, Flask, and Django launch flags;
- Procfile, Makefile, Taskfile, and justfile commands only when a recognized server command is present.

The scanner tokenizes command text but never executes it, performs shell expansion, or evaluates command substitution.

### Tier 3: planned focused adapters

Nginx, Caddy, Traefik development configuration, devcontainer, VS Code launch and task files, and additional framework parsers use the same contract after fixtures demonstrate exact value. They are not replaced by generic text or number scanning.

The proposed project-manifest schema has a design contract but is not part of the locked MVP parser catalog and is not a published namespace. A future scope decision may add a manifest parser only after the working-name gate resolves and its filename and schema are accepted.

## Environment safety

Environment scanning:

- is local and can be disabled per root;
- reads only eligible files inside approved roots;
- uses a key allowlist and context-aware service mapping;
- persists a recognized port and safe key name only;
- discards unrelated values immediately;
- rejects credential-bearing URLs as port declarations unless a dedicated safe parser extracts only a non-secret endpoint port;
- never logs full lines;
- never returns environment contents through API or MCP;
- never sends an environment file to AI.

Examples of eligible keys include PORT and recognized service-specific port keys. Secret-like key names are never persisted as evidence text even if their values look numeric.

## Evidence and confidence

| Confidence | Meaning | Example |
| --- | --- | --- |
| exact | Syntax unambiguously defines the port and namespace | Compose published host port |
| high | Recognized key or command in supported context | PORT in an eligible service environment |
| medium | Supported framework default with stack evidence but no explicit value | Vite default port |
| low | Weak heuristic | Excluded from default MVP results |
| user_confirmed | User explicitly confirmed a finding | Confirmed custom declaration |

Framework defaults are declarations with role framework_default and medium confidence. They are not reservations and do not prove the service will use that value.

DiscoveryEvidence records:

- parser ID and version;
- safe relative path;
- line and column or structured pointer;
- source fingerprint;
- confidence and rationale code;
- redaction flags;
- scan time.

Evidence does not store full source lines.

## Variable resolution

Only deterministic, local, non-secret substitutions within the same supported configuration scope are resolved. Resolution has:

- explicit source precedence;
- cycle detection;
- depth and byte limits;
- no shell execution;
- no ambient process environment unless a documented scanner setting allows selected non-secret keys;
- provenance for every resolved segment.

Unresolved port variables remain an unknown declaration candidate with key name and evidence. They do not become port zero or a framework default automatically.

## Reconciliation

A declaration source key includes ProjectInstance, parser ID, source file identity, structured pointer, declaration role, protocol, namespace, and port.

After a complete successful parse:

- matching declarations are refreshed;
- new declarations are inserted;
- absent prior declarations from that exact parser-source scope become stale;
- affected conflicts are recomputed.

After a partial or failed parse:

- verified new results may be added when independent;
- old declarations are not retired;
- a safe parser diagnostic is attached to the scan run.

## Caching and file watching

Cache key includes:

- canonical source identity;
- content fingerprint;
- parser ID and version;
- effective scan policy revision;
- manifest or configuration schema version.

Watcher events are debounced and treated as hints. Rename, overflow, or watcher restart triggers targeted or full reconciliation. Cache entries never bypass current path authorization.

## Malicious-input controls

- YAML safe loader with aliases and nesting limits.
- JSON, TOML, and syntax parsers with size and depth limits.
- Regex patterns bounded and reviewed against denial of service.
- No eval, import, dynamic module execution, template execution, or shell.
- Archives and binary files are not expanded by default.
- Parser crashes are isolated to one file.
- Repository text and comments cannot change scanner policy.

## Failure behavior

| Failure | Result |
| --- | --- |
| Root permission denied | Root or subtree limitation with no false deletion |
| Symlink escapes root | Candidate rejected and security diagnostic audited |
| Oversized file | File skipped with bounded warning |
| Malformed supported file | Existing source declarations retained as stale or uncertain |
| Parser timeout | File-scoped timeout; other files continue |
| Watcher overflow | Schedule reconciliation; mark freshness appropriately |
| Unsupported syntax | Explicit unsupported result, no heuristic guess |
| Secret detector uncertainty | Drop the value and keep only safe diagnostic metadata |

## Parser release requirements

Every parser has fixtures for:

- explicit port and protocol;
- absent port;
- host versus container distinction;
- variable substitution;
- malformed input;
- oversized and deeply nested input;
- comments and unrelated numeric values;
- secret-bearing neighboring values;
- path and encoding edge cases;
- parser-version cache invalidation.
