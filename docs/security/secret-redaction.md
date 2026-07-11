# Secret Redaction Contract

Status: **Proposed pre-implementation contract**

## Objective

Redaction is a mandatory boundary before data enters logs, API responses, SSE events, backups, diagnostics, MCP results, or optional AI context. It supplements data minimization; it does not justify collecting fields that are unnecessary.

## Classification

| Class | Examples | Handling |
|---|---|---|
| Credentials | Bearer tokens, cookies, passwords, private keys, registry credentials | Never emit; store only through the authentication contract |
| Secret-like values | High-entropy keys, provider tokens, credential URLs | Replace with typed marker and record only detection category |
| Environment data | Values for keys not explicitly classified as safe port declarations | Do not collect or persist |
| Paths | Home directory, proprietary repository location | Use project identity or user-approved display form; redact in diagnostics by default |
| Process data | Full arguments and inherited environment | Exclude by default; derive only safe executable and port evidence |
| Source content | Configuration lines, comments, prompts embedded in projects | Persist structured extraction and location, not raw content |

## Pipeline

1. Minimize at the collector or parser boundary.
2. Attach a data classification to structured fields.
3. Apply exact-field deny rules before pattern rules.
4. Detect high-confidence credential formats and credential-bearing URLs.
5. Replace the value with a stable typed marker that cannot be mistaken for the original.
6. Scan serialized output again at every export boundary.
7. Reject the operation if mandatory redaction cannot complete.

Redaction must not retain a reversible prefix or suffix for credentials. Where correlation is necessary, use a keyed one-way digest held separately from output; ordinary releases should prefer no credential correlation.

## Port-focused environment parsing

Safe `.env*` parsing considers only allowlisted port key names and validates a numeric port value. Lines for keys such as passwords, secret keys, database URLs, cloud credentials, and arbitrary application settings are skipped without storing their values. Expansion, command substitution, and source semantics are never executed.

## Verification

The test corpus includes synthetic secrets for common provider formats, private-key headers, credential URLs, unicode and delimiter variations, values split across serializer boundaries, and false-positive controls. A release requires zero seeded-secret matches across persistence, HTTP, SSE, CLI, MCP, logs, backups, diagnostics, and AI requests.

Redaction failures are security failures, not warnings. The originating operation returns a stable safe error and a request ID.
