# Permissions and Capability Boundaries

Status: **Proposed pre-implementation contract**

## Default operating privilege

The MVP runs as the current local user without a privileged daemon. It binds application and MCP HTTP listeners to loopback only. It must not request persistent administrator access, install a kernel extension, modify global firewall rules, or write outside user-approved application state and project-independent configuration locations.

## Capability matrix

| Component | May read | May write or mutate | Explicitly prohibited in MVP |
|---|---|---|---|
| Host collector | Socket and limited process metadata available to the user | Observation cache and health only | Signals, termination, privilege escalation, process injection |
| Docker collector | Container and port metadata through negotiated Engine API | Observation cache and health only | Start, stop, remove, exec, build, pull, network mutation |
| Project scanner | Allowlisted files beneath a registered `ProjectInstance` | Scan evidence in PortAtlas storage | Source edits, symlink escape, arbitrary file search, command evaluation |
| Registry and allocator | Reservation, lease, conflict, and policy state | Atomic reservation and lease transactions | Binding sockets on behalf of projects, source patching, launching processes |
| Browser UI | Authenticated API resources allowed by session | Application commands exposed by approved service methods | Direct database, file, Docker socket, or OS access |
| CLI | Scoped application services | Commands within credential scope | Bypassing validation or repository transactions |
| MCP STDIO | Tool resources allowed by process-scoped configuration | Approved reservation and lease commands only | Inheriting broad secrets, arbitrary subprocesses, hidden mutation |
| MCP HTTP | Same application tools as STDIO with bearer scope | Approved reservation and lease commands only | Non-loopback bind, unauthenticated access, unvalidated Origin |
| Ollama adapter | Explicit minimized and redacted context | Ephemeral provider request and validated result record | Authority over allocations, tools, filesystem, Docker, subprocesses, or network |

## Credential permissions

The service creates a high-entropy root credential using an operating-system cryptographic random source. Its storage must be readable and writable only by the current user. Persistent credentials are stored as protected material or verifiers where the protocol permits; bearer values never appear in URLs, logs, process listings, or browser storage.

CLI and HTTP MCP credentials carry explicit scopes, expiry or revocation metadata, and a stable identifier that is safe to log. The browser receives a one-time bootstrap artifact through a local handoff and exchanges it for an HttpOnly SameSite session. Reuse, expiry, wrong origin, or wrong audience fails closed.

## Project consent

Registering a `ProjectInstance` is explicit user consent to scan the documented allowlist within that root. It is not consent to inspect sibling checkouts, follow external symlinks, transmit source, or modify files. Removing an instance revokes future scans and removes eligible retained evidence.

## Failure behavior

Missing permission produces a typed degraded state with remediation guidance. The application must not silently broaden access, repeatedly prompt for elevation, or reinterpret denied access as an empty trustworthy inventory.
