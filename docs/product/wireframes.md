# PortAtlas Initial Wireframes

## Purpose and status

These low-fidelity wireframes define information hierarchy, states, and primary actions for Gate 1. They are not final visual design or evidence that UI implementation exists. Interaction requirements come from [User journeys](user-journeys.md), [Information architecture](information-architecture.md), and the [SRS](../requirements/srs.md).

## 1. First-run setup: privacy and capabilities

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ PortAtlas setup                                                Step 1 of 5 │
├────────────────────────────────────────────────────────────────────────────┤
│ Local port intelligence, private by default                                │
│                                                                            │
│ ✓ Core data stays on this machine                                          │
│ ✓ Scans only roots you approve                                             │
│ ✓ Observation is read-only by default                                      │
│ ! Docker access is privileged and optional                                 │
│ ! Unmanaged processes can race with an availability check                  │
│                                                                            │
│ [View data-handling details]                           [Cancel] [Continue] │
└────────────────────────────────────────────────────────────────────────────┘
```

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Host capabilities                                              Step 2 of 5 │
├────────────────────────────────────────────────────────────────────────────┤
│ Host collector       Healthy     TCP/UDP · IPv4/IPv6                       │
│ Process metadata     Limited     Working directory unavailable for 3 PIDs  │
│ Docker               Stopped     Core features remain available            │
│ File watcher         Healthy                                                 │
│                                                                            │
│ PortAtlas will not request sudo automatically.                             │
│ [Learn about limitations]                              [Back] [Continue]   │
└────────────────────────────────────────────────────────────────────────────┘
```

## 2. Add and preview a project root

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Project roots                                                  Step 3 of 5 │
├────────────────────────────────────────────────────────────────────────────┤
│ Root label: Personal projects · selected folder        [Choose directory] │
│ Tag:  Personal      Depth: 4      Symlinks: Do not follow                 │
│                                                                            │
│ Default exclusions: .git · node_modules · .venv · build · caches          │
│ [Edit exclusions] [Preview scan]                                           │
│                                                                            │
│ Preview: 39 projects · 42 instances · 11 services · 2 warnings            │
│ ▸ Projects and checkout/worktree instances (39 / 42)                      │
│ ▸ Excluded paths (918)                                                     │
│ ▸ Permission warnings (2)                                                  │
│                                                                            │
│ Nothing is scanned until you approve.                  [Back] [Approve]   │
└────────────────────────────────────────────────────────────────────────────┘
```

## 3. Overview

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ PortAtlas       Search ports, projects, services…          [⌘K] [Refresh]  │
├───────────────┬──────────────────────────────────────────────────────────────┤
│ Overview      │ System status                                                │
│ Ports         │ [Host healthy] [Docker stopped—optional] [Scan 8s ago]       │
│ Projects      │                                                              │
│ Conflicts  4  │ [63 observed] [112 declared] [18 reserved] [2 leased]        │
│ Reservations  │ [4 conflicts] [1 public exposure] [47 projects]              │
│ Activity      │                                                              │
│ Integrations  │ Critical conflicts                                           │
│ Settings      │ ┌──────┬────────────┬────────────┬──────────┬──────────────┐ │
│ Help          │ │ Port │ Current    │ Other      │ Severity │ Action       │ │
│               │ ├──────┼────────────┼────────────┼──────────┼──────────────┤ │
│               │ │ 3000 │ app-one    │ app-two    │ High     │ Diagnose     │ │
│               │ │ 5432 │ postgres   │ public bind│ High     │ Review       │ │
│               │ └──────┴────────────┴────────────┴──────────┴──────────────┘ │
│               │                                                              │
│               │ Recent changes · Quick actions · Collector degradation       │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

## 4. Ports inventory

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Ports                    [Filter 3] [Group] [Columns] [Reserve] [Preflight] │
├──────────────────────────────────────────────────────────────────────────────┤
│ Search [3000____________________________________________________________]    │
│ Chips: [TCP ×] [Observed + Declared ×] [All projects]                       │
│                                                                              │
│ Port Proto Bind       State      Project       Service  Owner       Status  │
│ 3000 TCP   127.0.0.1  Observed   visual-labs   web      node/4812   OK      │
│      TCP   —           Declared   visual-labs   web      .env:PORT   Exact   │
│ 5432 TCP   0.0.0.0    Observed   infra-local   postgres Docker      Exposed │
│ 6379 TCP   —           Reserved   campaign-app  redis    user        Ready   │
│ 8080 TCP   —           Declared   old-project   api      compose:24  Conflict│
│                                                                              │
│ Showing 1–50 of 193                                      [Previous] [Next] │
└──────────────────────────────────────────────────────────────────────────────┘
```

Expanded port detail keeps authoritative and non-authoritative records separate:

```text
┌─ TCP 3000 ──────────────────────────────────────────────────────────────────┐
│ OBSERVED   127.0.0.1 · node · PID 4812 (started 10:42) · seen 2s ago       │
│ DECLARED   visual-labs/.env · PORT · exact · scanned 12s ago                │
│ RESERVED   none                                                             │
│ CONFLICTS  none                                                             │
│ EVIDENCE   [Collector record] [Safe declaration location]                   │
│ ACTIONS    [Open project] [Preflight] [Reserve]                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 5. Project detail

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Project: VisualLabs                   3 concrete instances                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ Stack: React · FastAPI · PostgreSQL · Docker Compose                       │
│ Instance: main checkout · /…/VisualLabs · clean · scanned 12s ago [Rescan] │
│ Other instances: feature-auth worktree · release-test checkout             │
│                                                                              │
│ Services                                                                     │
│ web  TCP 3100  Observed + declared   Healthy evidence      [View]           │
│ api  TCP 8100  Declared              Conflict on 8100      [Preflight]      │
│ db   TCP 5432  Docker published       Bound 127.0.0.1      [View]           │
│                                                                              │
│ [Ports] [Conflicts] [Evidence] [Policy] [Activity]                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 6. Conflict detail

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Conflict: TCP 8080                                  High · DECLARED_ACTIVE │
├──────────────────────────────────────────────────────────────────────────────┤
│ Current owner                                                               │
│ Java · PID 8132 + start time · service-a · 0.0.0.0:8080                    │
│ [Runtime evidence]                                                          │
│                                                                              │
│ Conflicting declaration                                                     │
│ service-b/compose.yaml:24 · host 8080 → container 8080 · exact              │
│ [Declaration evidence]                                                      │
│                                                                              │
│ Why it matters                                                              │
│ Docker startup cannot claim this host binding while the listener remains.   │
│                                                                              │
│ Recommendation                                                              │
│ 8182 is policy-compliant and unused in current evidence. A suggestion is    │
│ not a reservation.                                                          │
│                                                                              │
│ [Reserve 8182] [Manual guidance] [Ignore with reason]                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 7. Reserve a port

```text
┌─ Reserve port ──────────────────────────────────────────────────────────────┐
│ Project*     [service-b____________________]                                │
│ Instance*    [main checkout________________]                               │
│ Service*     [api__________________________]                                │
│ Protocol*    [TCP]       Policy range [8000–8999]                          │
│ Port         [8182]      [Check again]                                     │
│ Ownership    Persistent reservation                                         │
│ Reason       [Resolve conflict on 8080_______________________________]      │
│                                                                            │
│ ✓ No observation, reservation, or lease currently conflicts                │
│ ! An unmanaged external process can still ignore this registry              │
│                                                   [Cancel] [Reserve]        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Integrations

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Integrations                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│ Codex · Project scope · STDIO · Read-only              Connected [Manage]  │
│ Claude-compatible · Not configured                               [Set up]  │
│ Generic MCP HTTP · Loopback · Token expires in 26d          [Rotate token] │
│                                                                              │
│ Setup flow: Client → Scope → Transport → Permissions → Preview → Apply       │
│ Every automatic configuration change creates a backup and supports rollback. │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 9. Optional AI Assistant settings and result

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Settings / AI Assistant                                  [Disabled    ○]    │
├──────────────────────────────────────────────────────────────────────────────┤
│ Provider  Ollama       Endpoint http://127.0.0.1:11434     [Test]           │
│ Model     qwen3:4b     Structured ✓  Tools: read-only ✓    [Benchmark]      │
│ Permissions [Inventory ✓] [Explanations ✓] [Summaries ✓] [Detection ○]      │
│ Privacy    [Context preview ✓] [Store prompts ○] [Store conversations ○]    │
│ Runtime    Timeout 30s · Concurrency 1 · Keep-alive 5m · Background off     │
│ [Clear AI-derived data]                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

```text
┌─ Generated explanation · non-authoritative ─────────────────────────────────┐
│ service-b cannot publish TCP 8080 because service-a currently owns a        │
│ wildcard binding. Port 8182 is policy-compliant in current evidence.         │
│                                                                            │
│ Evidence: runtime-7a2 · declaration-1cf · policy-03                         │
│ Model: qwen3:4b · schema valid · generated 14:02 · current as of 14:02      │
│ [View deterministic records] [Discard]                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 10. Degraded state

```text
┌─ Local AI unavailable ──────────────────────────────────────────────────────┐
│ Ollama is not responding. Core scanning, conflict detection, allocation,   │
│ reservations, MCP tools, and project management remain operational.         │
│ [Retry once] [Disable AI] [Troubleshoot]                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

Collector, Docker, watcher, and permission degradation use the same pattern: named subsystem, last successful evidence, affected capability, unaffected capability, and safe recovery action.

## 11. Narrow-screen adaptation

The persistent sidebar becomes a labeled navigation drawer. Summary cards stack. Port tables offer a column chooser and semantic list rows showing port/protocol, state, project/service, owner, and conflict before secondary fields. Row actions remain keyboard accessible and no essential relationship depends on horizontal scrolling alone.

## 12. Activity and audit

```text
┌─ Activity ──────────────────────────────────────────────────────────────────┐
│ [Search request/resource] [Actor ▾] [Action ▾] [Result ▾] [Time range ▾]   │
│ 14:22  ✓ Lease created     agent:codex   instance:api   TCP 4310 [View]    │
│ 14:19  ! Docker degraded   collector     last good 14:18          [View]    │
│ 14:17  ○ Project rescanned user          instance:web  12 findings [View]  │
│                                                                              │
│ ✓ success   ! degraded   ○ informational — text/icon states, not color-only │
│ [Previous]                                              [Next]              │
└──────────────────────────────────────────────────────────────────────────────┘
```

Activity detail shows request ID, safe actor identity, action, resource/revision, outcome, timestamp, and redacted metadata. It never shows bearer values, cookies, raw environment data, full process arguments, project contents, or raw AI prompts.

## 13. Empty, keyboard, and compact states

```text
┌─ Ports — empty ─────────────────────────────────────────────────────────────┐
│ No current evidence matches this view.                                     │
│ Collector status: Host ✓  Docker unavailable !  Scans not configured ○     │
│ [Add project root] [Refresh host evidence] [Clear filters] [Learn why]      │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ Command palette (⌘K / Ctrl+K) ─────────────────────────────────────────────┐
│ > inspect tcp 4310                                                          │
│ → Open port TCP 4310               owner/source and freshness               │
│ → Reserve a port                   opens explicit scoped form               │
│ → Collector health                opens degraded-capability detail          │
└──────────────────────────────────────────────────────────────────────────────┘
```

Empty states distinguish true zero results, active filters, collector unavailability, permission limits, and scans not yet configured. Compact density preserves semantic labels and focus order; it may hide secondary columns behind an accessible disclosure but never hides managed status, conflict, freshness, or degraded state. All row actions, filters, tabs, dialogs, pagination, and the command palette have a documented keyboard path with visible focus and an equivalent non-shortcut control.

## Interaction and accessibility annotations

- All dialogs have a visible title, initial focus, focus trap, Escape behavior, and non-destructive default action.
- Status changes use live-region announcements without excessive repetition.
- State and severity use text/icon plus color.
- Filters are removable controls with announced result counts.
- Evidence opens without losing inventory filters or scroll position.
- Generated content is never visually indistinguishable from authoritative evidence.
- Demo mode uses a persistent banner and source labels.
- Reduced-motion preference disables nonessential transitions.
