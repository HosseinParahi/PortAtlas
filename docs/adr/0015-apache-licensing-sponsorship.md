# ADR 0015: Apache licensing/sponsorship

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Source license and voluntary project funding

## Context

The project is intended for public open-source use, including individuals and companies. Users need clear permission to run, modify, redistribute, and use the software commercially. Contributors and downstream users also benefit from an explicit patent grant. Funding may help maintenance, but payment must not be confused with license permission.

## Decision

Release project-owned code under the Apache License, Version 2.0:

- Include the complete Apache-2.0 LICENSE text in source and binary distributions.
- Maintain NOTICE content when project or dependency notices require it.
- Preserve required copyright, license, attribution, and modification notices.
- Review every dependency and bundled asset for compatible license and notice obligations.
- Commercial use, internal use, modification, and redistribution are allowed under Apache-2.0 without payment to the maintainers.
- The Apache-2.0 patent license and termination terms apply as written.
- Apache-2.0 does not grant rights to the project name or trademarks; ADR 0023 governs name clearance.

The project may invite voluntary sponsorship, initially through a maintainer-approved GitHub Sponsors profile or equivalent transparent channel:

- Sponsorship is optional and is not a condition of installation, use, modification, commercial use, support eligibility, security reporting, or contribution.
- No license key, activation, feature gate, telemetry, or preferential security disclosure is tied to payment.
- Sponsor benefits must not imply ownership of the project or trademark rights.
- Funding language must say support is voluntary and distinguish donations from paid services or contracts.

This ADR does not provide legal advice; release verification includes competent license review where risk warrants it.

## Alternatives considered

### MIT license

MIT is short and permissive but does not contain the same express patent-license structure.

### GPL or AGPL

Copyleft could ensure downstream source availability, but it is less aligned with frictionless adoption in proprietary local-development environments.

### Source-available or dual commercial license

These models could monetize use directly but conflict with the approved open-source and no-payment-for-commercial-use direction.

### No sponsorship channel

This avoids funding administration but removes a voluntary path for users who want to support maintenance.

## Consequences

### Positive

- Individuals and companies have a widely understood permissive license.
- The express patent grant improves downstream clarity.
- Sponsorship can fund maintenance without changing user rights.
- License and trademark decisions remain correctly separate.

### Costs and risks

- Downstream proprietary derivatives need not publish their changes.
- NOTICE and dependency-license compliance require release automation and review.
- Sponsorship administration may create tax, platform, and governance obligations.
- A license cannot clear the working title or third-party marks.

## Verification

- Compare the repository LICENSE byte-for-byte with the official Apache-2.0 text.
- Generate and inspect dependency and asset license reports for every release artifact.
- Verify binary distributions include LICENSE and required NOTICE material.
- Scan README, sponsor pages, installer copy, and website text for any implication that commercial use requires payment.
- Confirm sponsor links have no tracking or feature-gating behavior.
- Include license and notice checks in the release checklist and SBOM workflow.

## Revisit triggers

- A dependency is incompatible with Apache-2.0 distribution.
- Governance changes ownership of project copyright or release authority.
- The project proposes paid proprietary components, dual licensing, or trademark licensing.
- The sponsorship platform or maintainer entity changes.

## Sources

- [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- [Apache licensing and distribution FAQ](https://www.apache.org/foundation/license-faq.html)
- [Applying the Apache License, Version 2.0](https://www.apache.org/legal/apply-license)
- [GitHub Sponsors overview](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors)
