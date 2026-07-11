# Privacy Model

Status: **Proposed pre-implementation contract**

## Principles

- Local-first and offline-capable by default
- No telemetry, analytics beacon, crash upload, or background cloud call
- Collect the least data needed to explain a port claim
- Preserve provenance and freshness without retaining unnecessary contents
- Give the user a preview before diagnostic or AI context leaves its source component
- Make deletion and retention behavior explicit

## Data inventory

| Class | Examples | Default persistence | Default disclosure |
|---|---|---|---|
| Authoritative allocation | Reservation, lease owner identity, port, protocol, scope, revision, expiry | Required until released plus bounded audit history | Authenticated local UI, CLI, MCP by scope |
| Runtime evidence | Listening address, port, PID-derived stable identity, executable label, collector time | Current and limited recent observations | Authenticated local surfaces; raw arguments excluded |
| Container evidence | Container ID abbreviation, name, image label, published ports, collector time | Current and limited recent observations | Authenticated local surfaces |
| Project evidence | Project and instance identity, relative source reference, parser type, declared port, confidence | Current scan and bounded change history | Authenticated local surfaces; file contents excluded |
| Configuration | Safe settings and feature gates | Until changed | Authenticated settings surface; credentials never returned |
| Authentication | Token hash or protected token file, session identifier, scope, expiry | Until rotation or expiry | Never returned after bootstrap; logs show outcome only |
| Operational events | Request ID, event type, resource identity, revision, status, timestamp | Bounded local retention | Activity UI and redacted diagnostics |
| AI context and output | Minimized redacted evidence, structured recommendation | No raw prompt retention by default; optional bounded local history only with consent | AI settings and result surface only |
| Diagnostic export | User-selected redacted snapshot and manifest | Created only on explicit action | User controls the resulting local file |

## Sensitive fields

Never persist or emit environment values unrelated to ports, bearer credentials, cookies, private keys, raw authorization headers, full process command lines by default, file contents unrelated to extracted evidence, or Docker registry credentials. Paths are sensitive: normal UI may show a user-approved display path, while logs and exports use project identity or redacted suffixes.

## Retention and deletion

- Current authoritative state persists until the user releases or deletes it.
- Expired leases become non-authoritative immediately and may retain only a bounded audit event.
- Runtime and scan evidence has an explicit freshness window; stale data remains labeled and is pruned on a documented schedule.
- Sessions and one-time bootstrap artifacts expire independently of application data.
- AI raw context is ephemeral by default. If history is later enabled, it requires an explicit retention setting and deletion control.
- Deleting a project removes its stored scan evidence and display metadata but does not alter the source checkout.
- A diagnostic bundle is never uploaded automatically and is not managed after the user saves it.

Exact durations are configuration contract values to be selected and tested during Phase 3; absence of a final duration must default to the shorter, safer behavior.

## User controls

The UI must show collector status and freshness, registered project instances, retention settings, optional-AI status, context preview, and export contents. Users can disable Docker and AI, remove projects, rotate credentials, clear eligible history, and create a redacted diagnostic bundle.

## Privacy verification

Release tests seed unique secret canaries in environment files, process arguments, project paths, Docker labels, authentication headers, and AI inputs. Searches across the database, API responses, SSE payloads, logs, backups, and diagnostic exports must find zero forbidden values.
