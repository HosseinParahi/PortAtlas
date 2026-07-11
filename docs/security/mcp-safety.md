# MCP Safety

Status: **Proposed contract for MCP revision 2025-11-25**

PortAtlas exposes the same application services through MCP that REST and CLI use; MCP does not receive a privileged parallel implementation. Tool descriptions and results must repeat the managed-versus-unmanaged assurance boundary.

## Supported transports

- **STDIO:** one message per protocol framing rules, protocol output isolated from logs, minimal inherited environment, no shell wrapper requirement.
- **Streamable HTTP:** loopback binding only, authentication required, strict `Origin` validation, explicit session and protocol headers, bounded request bodies, and no legacy unauthenticated SSE endpoint.

The server must follow the [MCP 2025-11-25 transport requirements](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports). A later protocol revision requires contract and compatibility review before adoption.

## Tool policy

| Capability | MVP availability | Safety contract |
|---|---|---|
| List ports, projects, conflicts, reservations, collector health | Read-only | Freshness, provenance, confidence, and managed status included |
| Explain a conflict | Read-only deterministic result | Never claim exclusive ownership from unmanaged evidence |
| Create, renew, or release reservation/lease | Scoped mutation | Idempotency key, validation, atomic transaction, current revision |
| Scan a registered instance | Bounded operation | Explicit identity, allowlisted parsers, root confinement, cancellation |
| Patch source, launch project, stop process, mutate Docker | Unavailable | Tool is absent rather than returning a misleading simulation |
| Ask optional local AI | Conditional | Explicit opt-in, context preview, redaction, validated schema, and only the hard-limited read-only internal AI query allowlist; no MCP or mutating tools |

## Authentication and authorization

HTTP MCP uses a scoped bearer credential designed for the MCP audience; browser cookies are not accepted as a substitute. Every request checks scope at the application-service boundary. Credential material is never accepted in a query string or returned by resources. STDIO authorization derives from explicit launch configuration and still applies capability policy.

## Instructions and result language

Instructions must say that PortAtlas makes reservations and leases atomic only among cooperating PortAtlas-aware clients. An active reservation or lease does not reserve an operating-system socket and cannot prevent an unmanaged process from racing or ignoring the registry. Host, Docker, and source scans are observations that may be incomplete or stale. Each relevant result includes evidence source, observation time, freshness, and whether the state is managed.

## Protocol defenses

- Reject invalid JSON-RPC, unsupported versions, duplicate request IDs within the active session, unknown tools, excess nesting, oversized input, and invalid schemas.
- Use stable safe errors and a request ID without echoing secret-bearing input.
- Bound concurrency, scan work, SSE or Streamable HTTP sessions, and cancellation cleanup.
- Never put diagnostic logs on STDIO protocol output.
- Validate session ownership and prevent cross-session event delivery.
- Disable cross-origin credential use and reject missing or untrusted origins for HTTP.

## Release evidence

Contract tests cover both transports, authentication and scope failures, Origin and host attacks, cancellation, reconnect behavior, malformed inputs, redaction, tool absence, managed/unmanaged copy, and deterministic-core availability when MCP is disabled.
