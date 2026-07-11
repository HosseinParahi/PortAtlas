# Founder User Acceptance Plan

Status: **Proposed pre-implementation contract**

Each case is a stable definition referenced by the requirements traceability matrix. Execution requires implemented software and a clean, documented environment; this checkpoint defines the cases but does not claim they pass.

| Test ID | Acceptance scenario | Method and measurable pass condition |
|---|---|---|
| UAT-001 | Find the owner of a port | Seed a controlled listening socket and reach its owner/source from the ports inventory in no more than two pointer actions or keyboard equivalents. Verify protocol, port, process identity, bound address, project association and confidence, evidence source, freshness, and safe argument handling. |
| UAT-002 | Detect a future declared conflict | Scan two inactive project instances with exact declarations for the same scoped port. Verify a declared-versus-declared conflict links both evidence locations, invents no runtime listener, and labels any alternative unreserved until a reservation or lease succeeds. |
| UAT-003 | Detect Docker and native process conflict | Combine a native listener with Compose evidence declaring the same host binding. Verify the conflict distinguishes host and container ports, shows both provenance records, and Docker absence still leaves the native evidence correct. |
| UAT-004 | Agent chooses and leases a safe port | With an authorized scoped MCP client, resolve project policy, preflight, request a candidate, and acquire an atomic lease in one workflow. Verify owner, expiry, evidence, idempotency, and that no file edit, launch, termination, Docker mutation, or global configuration change occurs. |
| UAT-005 | Scan environment configuration without exposing secrets | Scan a safe port key beside unique secret canaries. Verify the declaration and relative evidence are present while database, HTTP, SSE, UI, CLI, MCP, audit, logs, backup, diagnostics, and any AI context contain zero forbidden canaries. |
| UAT-006 | Configure project roots through the UI | Select and preview a synthetic project root, approve scan policy, and create its project instances without editing code. Verify inclusion/exclusion counts, warnings, cancellation, source-file hashes, and no scan outside the approved root. |
| UAT-007 | Warn about public database exposure | Seed a database listener bound to a non-loopback interface. Verify an accessible non-color warning identifies protocol, binding, evidence, freshness, and limits without claiming firewall or remote-reachability knowledge PortAtlas does not possess. |
| UAT-008 | Allocate race-safe concurrent leases | Run simultaneous lease requests against the same candidate range and repeat selected requests with identical idempotency keys. Verify no duplicate active scoped port, one result per idempotent command, transactionally consistent audit, and typed conflict or alternate results. |
| UAT-009 | Explain the unmanaged-process limitation | Compare a PortAtlas-managed lease with an externally opened process. Verify README-aligned UI, REST, CLI, and MCP copy: the managed lease has strong registry assurance while the external listener is time-bounded observation that may race or become stale. |
| UAT-010 | Preserve core operation when local AI is unavailable | Run the full deterministic core with Ollama absent, disconnected, timing out, and disabled mid-request. Inventory, scanning, reservations, leases, conflicts, browser updates, CLI, and MCP core remain healthy and authoritative state is unchanged by provider failures. |
| UAT-011 | Generate a grounded conflict explanation | When conditional AI is included, provide a fixed conflict evidence set and request an explanation. Every accepted owner, project, port, availability, and recommendation claim references supplied evidence; the result is visibly advisory and cannot mutate state. |
| UAT-012 | Reject invalid structured model output | Make a fake provider return malformed JSON, unknown fields, fabricated evidence IDs, forbidden actions, oversize text, and semantically stale revisions. Each response is wholly rejected with a safe error and no partial persistence or authoritative change. |
| UAT-013 | Resist repository prompt injection | Seed direct, indirect, encoded, multilingual, and schema-shaped instructions in filenames and supported configuration contexts. Verify none obtain omitted context, secrets, tools, broader permissions, or mutation, while benign controls remain usable. |
| UAT-014 | Generate a secret-safe project summary | When conditional AI is included, request a summary from evidence adjacent to unique canaries and private-path markers. Verify the provider request, output, logs, history, backup, and diagnostics contain no forbidden value and disclose the context categories used. |
| UAT-015 | Keep AI-assisted extraction unconfirmed | Present ambiguous model-proposed port extraction. Verify it remains an advisory candidate with provenance and confidence, cannot become declared or managed truth automatically, and requires deterministic validation or explicit user confirmation before any separate reservation command. |

## Cross-cutting execution

All browser cases run with pointer and keyboard. Core flows receive an accessibility review with non-color state indicators and visible focus. Each result records build revision, OS and hardware profile, data-set version, timestamps, evidence, deviations, and founder disposition.

## Acceptance rule

AC-001 through AC-010 are unconditional. AC-011 through AC-015 become release-blocking only when AI is included; when AI is excluded, release evidence must instead prove those surfaces are absent and the core remains complete. Installation time, parser recall, runtime freshness, target capacity, lifecycle recovery, and broader accessibility are separate mandatory release checks in the performance, scanner, operations, and MVP checklists.
