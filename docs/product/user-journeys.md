# PortAtlas User Journeys

## Journey conventions

Each journey names its persona, trigger, normal flow, degraded or exception path, and acceptance evidence. Exact testable criteria are maintained in [Acceptance criteria](../requirements/acceptance-criteria.md).

## J-01: First installation and privacy-first setup

**Persona:** P-01 multi-project local developer
**Trigger:** The user installs PortAtlas on macOS for the first time.
**Desired outcome:** Reach a useful dashboard in under five minutes without editing source or granting unnecessary access.

### Normal flow

1. Start the local service and open the loopback browser UI.
2. Read a concise privacy statement explaining local data, approved roots, read-only defaults, Docker privilege, and optional AI.
3. Run host capability and permission checks; see exactly what can and cannot be observed.
4. Detect Docker availability without requiring it.
5. Select a project root through the system picker.
6. Preview logical projects, concrete checkout/worktree `ProjectInstance` records, and exclusions before approving the scan.
7. Choose default port ranges, forbidden/ephemeral ranges, scan cadence, and symlink behavior.
8. Optionally configure a client integration through a previewable, reversible flow.
9. Finish setup and see collector status, active listeners, declarations, reservations, conflicts, and exposure warnings.

### Degraded and recovery paths

- If permissions limit process metadata, show the sockets still visible, the missing fields, why they are missing, and an optional manual remedy; do not request automatic elevation.
- If Docker is absent or stopped, mark only Docker capability unavailable.
- If a root contains permission errors or excessive depth, show scoped errors and allow pause, exclusion, or cancellation.
- If configuration is invalid, preserve the last-known-good configuration and offer a safe reset/import path.

### Evidence

`AC-006`, installation metric `SM-01`, configuration requirement `SRS-SCN-001`, setup requirement `SRS-UI-001`, and reliability requirements `SRS-NFR-003` and `SRS-OPS-004`.

## J-02: Find the owner and source of a port

**Persona:** P-01
**Trigger:** A development URL or launch error references TCP 3000.
**Desired outcome:** Explain the current owner and related project evidence in no more than two interactions.

### Normal flow

1. Search for `3000` from the overview or command palette.
2. Open the matching port row.
3. Review protocol, address, state, process, PID and start time, redacted command, user, logical project, concrete `ProjectInstance`, service, Docker/container mapping, evidence, confidence, and last-seen timestamp.
4. Follow a project or declaration link when additional context is needed.

### Degraded and recovery paths

- When PID/process details are unavailable, label ownership as permission-limited rather than inferred.
- When project association is heuristic, show confidence and competing evidence.
- When IPv4/IPv6 or wildcard semantics affect collision interpretation, explain the interface behavior.

### Evidence

`AC-001`, `SRS-COL-001`, `SRS-COL-002`, `SRS-UI-002`, `SRS-UI-003`, and metrics `SM-04` and `SM-05`.

## J-03: Detect and diagnose a future conflict

**Persona:** P-01
**Trigger:** Two inactive `ProjectInstance` records declare host port 8080, or a Compose host binding conflicts with a native process.
**Desired outcome:** See the conflict before startup and choose a policy-compliant response.

### Normal flow

1. Project scan records both declarations with exact file/location evidence.
2. The conflict engine creates a normalized declared-declared or Docker-native finding.
3. The conflict center shows severity, cause, affected records, evidence, impact, and whether prevention is available.
4. PortAtlas proposes an explained safe alternative that respects policy, observations, reservations, leases, protocols, interfaces, and excluded ranges.
5. The user reserves the alternative or reviews non-executable manual guidance.

### Degraded and recovery paths

- If a parser finding is heuristic, the recommendation displays confidence and does not silently rewrite configuration.
- If availability changes before reservation, recheck and return a typed conflict.
- An ignored finding requires a reason and optional expiry and remains auditable.

### Evidence

`AC-002`, `AC-003`, `SRS-SCN-003` through `SRS-CNF-001`, and `SM-03`.

## J-04: Agent preflights and reserves a port

**Persona:** P-02 agent-assisted developer
**Trigger:** A coding agent needs a port for a new local API.
**Desired outcome:** Receive an explained, atomic lease without unauthorized source or process changes.

### Normal flow

1. Resolve the current logical `Project` and concrete `ProjectInstance` from the approved root.
2. Read instance services, current ports, policy, and evidence through MCP.
3. Run preflight and diagnose conflicts.
4. Request a suggestion with project/service/protocol/range constraints.
5. Acquire a short-lived lease through a guarded tool.
6. Report the leased instance/service/port, expiry, evidence, and manual configuration work outside PortAtlas. The MVP exposes no source-edit, launch, process-control, Docker-lifecycle, or launch-verification tool.

### Degraded and recovery paths

- A suggestion without a lease is labeled race-prone.
- Expired or collided leases return stable error codes and no partial mutation.
- Requests outside approved canonical instance roots and attempts to edit client/project files are rejected because those MVP tools are absent.
- For unmanaged launches, PortAtlas detects and explains the race but never claims prevention was guaranteed.

### Evidence

`AC-004`, `AC-008`, `AC-009`, `SRS-REG-002`, `SRS-ALC-001`, `SRS-MCP-001`, `SRS-MCP-002`, `SRS-NFR-004`, and `SM-06`.

## J-05: Safely inspect a secret-bearing project

**Persona:** P-01 or P-02
**Trigger:** A project has `.env` files containing both port keys and credentials.
**Desired outcome:** Discover the relevant port while exposing no unrelated or secret value.

### Normal flow

1. A targeted environment parser opens an approved file locally.
2. It extracts only recognized port-relevant keys/values.
3. It stores the safe port declaration, source key, location where safe, parser, timestamp, and confidence.
4. UI/API/MCP/log/audit responses omit credentials and unrelated lines.
5. If optional AI is enabled, the context builder receives only the minimum redacted evidence and exposes a context summary.

### Degraded and recovery paths

- Secret detection before or after context construction blocks the model call.
- Environment scanning can be disabled per configuration or project.
- Diagnostic exports redact sensitive paths/arguments and exclude AI data unless selected.

### Evidence

`AC-005`, `AC-014`, `SRS-SCN-004`, `SRS-AI-003`, `SRS-SEC-001`, and `SRS-SEC-002`.

## J-06: Review an unexpected public binding

**Persona:** P-01
**Trigger:** A database binds to `0.0.0.0` or `::`.
**Desired outcome:** Understand the exposure and receive safe manual guidance.

### Normal flow

1. Runtime reconciliation identifies protocol, wildcard address, port, process/container, and project.
2. Policy marks a database or admin service as loopback-preferred.
3. Dashboard and conflict center show an exposure warning with evidence and severity.
4. The user reviews a safe alternative and non-executable manual guidance.

### Guardrail

PortAtlas does not modify the firewall, terminate the service, or rewrite the binding silently.

### Evidence

`AC-007`, `SRS-COL-002`, `SRS-REG-001`, `SRS-CNF-001`, and `SRS-SEC-003`.

## J-07: Use optional local AI for a grounded explanation

**Persona:** P-01 or P-02
**Trigger:** The user enables an installed Ollama model and asks why a project cannot start.
**Desired outcome:** Receive a concise explanation tied to deterministic evidence with no mutation authority.

### Normal flow

1. User explicitly enables the provider and tests loopback connection, version, model, and capabilities.
2. Context builder resolves authoritative records, selects minimum data, redacts secrets, marks repository content untrusted, and assigns evidence IDs.
3. The model receives a typed read-only task and fixed tool allowlist.
4. Strict JSON/schema, semantic, path, port, protocol, and evidence validation runs.
5. UI labels the result generated/non-authoritative and shows provider/model/version, timestamp, confidence, staleness, warnings, and evidence.

### Degraded and recovery paths

- Missing model, timeout, cancellation, invalid JSON, unsupported tool request, or provider restart returns a safe typed error and leaves authoritative state unchanged.
- Prompt injection cannot alter policy, paths, permissions, or tool access.
- An AI extraction remains `AI suggested` and unconfirmed until deterministic evidence or a user confirms it.
- Disabling Ollama leaves all core capability available and allows deletion of AI-derived data.

### Evidence

`AC-010` through `AC-015`, `SRS-AI-001` through `SRS-AI-003`, and `SRS-AI-004`.

## J-08: Back up, upgrade, restore, and uninstall

**Persona:** P-01 or P-03
**Trigger:** The user upgrades PortAtlas or removes it.
**Desired outcome:** Preserve user-controlled configuration/state, recover safely, and understand all data locations.

### Normal flow

1. Show application, configuration, data, log, and backup locations.
2. Create a validated backup before migration.
3. Upgrade application and run recoverable schema migration.
4. Verify service status, collectors, configuration, and state reconciliation.
5. Roll back or restore if validation fails.
6. Uninstall binaries/service integration while explicitly offering to retain or remove local data.

### Evidence

`SRS-OPS-001`, `SRS-OPS-003`, `SRS-NFR-003`, `SRS-OPS-004`, and metric `SM-11`.

## Journey-to-interface map

| Journey | Primary interface | Supporting interface |
| --- | --- | --- |
| J-01 | Setup wizard | CLI status/config and Help |
| J-02 | Global search and Ports | Project detail and API |
| J-03 | Conflicts | Reservations and project preflight |
| J-04 | MCP | CLI/API and Integrations UI |
| J-05 | Project evidence | Settings/privacy and diagnostic export |
| J-06 | Overview exposure card | Conflict detail |
| J-07 | AI Assistant | Evidence detail and Settings |
| J-08 | Installer/CLI | Settings backup/restore and operations docs |
