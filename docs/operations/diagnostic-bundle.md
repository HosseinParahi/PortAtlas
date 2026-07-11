# Diagnostic Bundle Contract

Status: **Proposed explicit-export workflow**

PortAtlas never creates or uploads a support bundle automatically. A user initiates creation, selects categories, reviews a manifest and redaction summary, and chooses where to save the local result.

## Default contents

| Included | Excluded |
|---|---|
| Application version, schema version, supported platform facts | Bearer tokens, cookies, authentication headers, token files |
| Collector and integration health with timestamps | Environment values and full process arguments |
| Stable error codes, request IDs, and bounded local event categories | Project source, configuration file bodies, Git contents |
| Safe counts for projects, evidence, reservations, and conflicts | Full user paths unless separately selected and previewed |
| Configuration keys with values removed or safely classified | Database credential URLs, Docker credentials, Ollama prompts |
| Migration and integrity outcomes | Raw database or backup by default |
| Redaction engine version and canary scan outcome | Browser storage, private keys, model files |

## Manifest

The archive manifest records bundle schema version, creation time, application version, selected categories, file names, sizes, digests, redaction ruleset, omissions, and integrity result. It contains no credential or raw sensitive field.

## Generation pipeline

1. Build structured data from allowlisted fields.
2. Apply classification-aware minimization and redaction.
3. Serialize into an isolated temporary directory with user-only permissions.
4. Run common-secret, canary, and personal-path scans.
5. Abort and remove the temporary result on any mandatory scan failure.
6. Show manifest, size, and disclosure preview.
7. Save only after explicit user confirmation.

## Tests

Security tests seed secrets in every source surface, include serializer boundary and encoding cases, simulate interruption and disk-full conditions, and inspect both successful archives and temporary cleanup. The release threshold is zero forbidden canary values and no file outside the allowlist.
