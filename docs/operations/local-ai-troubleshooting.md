# Local AI Troubleshooting Contract

Status: **Conditional proposal**

AI problems must never be worked around by broadening context, disabling redaction, granting tools, exposing a remote provider, or bypassing schema validation.

| Symptom | Safe interpretation | Safe response |
|---|---|---|
| Feature not shown | AI was excluded from the release or is globally disabled | Use deterministic product features; review the release checklist |
| Provider unavailable | Ollama absent, stopped, wrong loopback endpoint, or timed out | Keep core running; inspect local provider health independently; retry explicitly |
| No compatible model | No locally present model passed capability checks | Select an already installed evaluated model; PortAtlas does not download one |
| Invalid structured output | Model response failed syntax or semantic validation | Discard the entire response and use deterministic evidence |
| Unsupported evidence claim | Output referenced an unknown or stale evidence ID | Refresh deterministic state and retry only if useful; never accept the claim |
| Suspected prompt injection | Project content attempted to alter policy or request forbidden data/action | Reject result, inspect safe category, and continue without AI |
| Slow or resource-heavy request | Model or context exceeds local budget | Cancel, choose a documented smaller evaluated model, or disable AI |
| Secret redaction warning | Context safety could not be proven | Do not send; remove unnecessary context and investigate redaction |
| Provider restarts mid-request | Optional dependency failed | Return a typed error; verify authoritative state is unchanged |
| History cannot be cleared | Retention operation failed | Disable new AI calls and preserve evidence for private security support |

## Diagnostic evidence

Safe evidence includes request ID, provider health category, model identifier, timing, cancellation state, schema version, validation category, context category counts, and redaction outcome. Never request or share raw prompts, full responses containing project data, credentials, private paths, or model service logs without a separate private review.

## Escalation

A secret leak, forbidden action, non-loopback call, validation bypass, or authoritative-state impact is a security defect and excludes AI from the release until root cause, regression coverage, and the entire mandatory evaluation set are green.
