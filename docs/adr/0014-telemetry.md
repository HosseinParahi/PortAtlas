# ADR 0014: Telemetry

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Metrics, traces, logs, crash data, and usage reporting

## Context

PortAtlas observes sensitive local facts: paths, processes, commands, projects, listeners, containers, and agent actions. Even anonymous event combinations can fingerprint a developer or reveal work patterns. Core observability is still necessary for troubleshooting, performance, and safe diagnostics.

## Decision

Collect no external telemetry in the MVP:

- Do not send usage events, installation pings, crash reports, traces, metrics, logs, project metadata, port inventory, AI prompts, or model metadata to a maintainer or third party.
- Do not bundle a configured remote exporter or analytics SDK.
- Structured logs, metrics, and traces are local only and use safe field allowlists, redaction, bounded retention, and user-visible locations.
- Internal instrumentation may use OpenTelemetry-compatible APIs, but the default and release configuration has no network exporter.
- Diagnostic bundles are generated only by an explicit user action, previewed before sharing, and redacted. PortAtlas never uploads a bundle itself in the MVP.
- Demo mode never mixes synthetic events into real machine diagnostics without a visible label.
- Sponsorship links defined by ADR 0015 do not include tracking parameters or unlock telemetry-gated behavior.
- Any future telemetry requires a new ADR, privacy review, exact event schema, retention and recipient documentation, explicit opt-in, a complete off switch, and proof that declining does not reduce core functionality.

## Alternatives considered

### Anonymous opt-out telemetry

Opt-out collection could improve product prioritization but conflicts with local-first privacy expectations and sends data before informed consent.

### Anonymous opt-in telemetry in the MVP

Opt-in is safer but still requires governance, schemas, infrastructure, deletion policy, and security work that is not needed to validate the core product.

### No instrumentation at all

This avoids data collection but makes local troubleshooting, performance testing, and degraded-state diagnosis unnecessarily difficult.

### Automatic crash uploads

Crash reports are useful but can contain process arguments, paths, environment fragments, stack data, and local identifiers.

## Consequences

### Positive

- Offline and private-by-default claims are straightforward.
- There is no telemetry backend, credential, or breach surface.
- Users control every diagnostic disclosure.
- Local instrumentation still supports development and support.

### Costs and risks

- Maintainers cannot measure adoption or failures automatically.
- Bug reports depend on users choosing to share redacted evidence.
- Redaction quality still matters for local logs and bundles.
- A future telemetry proposal must start from an explicit privacy gate.

## Verification

- Run the release build with network capture while exercising every workflow and prove no telemetry or crash-report destinations are contacted.
- Search dependencies and built assets for analytics SDKs, remote exporters, collection endpoints, and tracking pixels.
- Test diagnostic-bundle preview, redaction, cancellation, and local-only output.
- Assert logs, metrics, and traces exclude environment values, credentials, full command lines, and unapproved source content.
- Run all core features with the network disabled.

## Revisit triggers

- The founder explicitly requests an opt-in telemetry proposal.
- Support cannot diagnose critical failures with user-controlled bundles.
- A dependency introduces hidden or default network reporting.
- Law, platform policy, or distribution channels require disclosure changes.

## Sources

- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)
- [OpenTelemetry SDK environment-variable specification](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
