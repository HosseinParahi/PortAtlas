# ADR 0023: Working-name collision/trademark clearance

- **Status:** Proposed / Blocking public release
- **Date:** 2026-07-11
- **Scope:** Project, package, binary, domain, and public product naming

## Context

PortAtlas is a working title, not a cleared public name. Repository names, package registries, application bundle identifiers, domains, social handles, and trademarks create different collision risks. A permissive source license does not grant a right to use a conflicting mark. No dated, jurisdiction-aware clearance report approved for software and developer-tool use exists in this repository.

Changing a name after public packages, configuration files, binaries, integrations, domains, and user data exist is expensive. ADR 0010 therefore treats .portatlas.yaml as an unpublished working filename, and ADR 0007 blocks branded release artifacts.

## Decision

Keep PortAtlas only as an internal working title until a documented clearance gate is accepted:

- Do not announce a public product, publish a package, reserve a final bundle identifier, distribute a branded installer, publish the manifest schema, create a Homebrew formula or cask, or claim trademark rights under this name.
- The release manager must produce a dated name-clearance report covering exact, spaced, hyphenated, phonetic, and confusingly similar variants.
- Search software and developer-service uses in relevant trademark classes and jurisdictions through official databases, including USPTO, WIPO, EUIPO, and CIPO where distribution is planned.
- Search GitHub, GitLab, Codeberg, npm, PyPI, crates.io, Homebrew, container registries, MCP directories, application stores, search engines, domain records, and major social or documentation hosts.
- Record each query, date, database or registry, result URL or exported evidence, owner, goods or services, status, jurisdiction, first-use information when available, and assessed similarity.
- Check domain and package availability only after collision review; availability is evidence, not legal clearance.
- Obtain qualified trademark counsel review before public release when any live or plausibly related software, network, mapping, monitoring, or developer-tool result exists.
- Resolve the gate by either accepting a cleared public name in a superseding ADR or selecting a new candidate and repeating the complete search.
- After a name is accepted, update repository branding, package names, executable and service names, bundle identifiers, configuration filename, MCP server identity, domains, documentation, and release metadata in one traceable rename plan.

Until then, public-release status remains blocked. Private architecture work may use the working title if documents continue to state that it is not cleared.

## Alternatives considered

### Assume registry availability is enough

A free npm, PyPI, GitHub, or domain name does not rule out common-law or registered trademark conflicts.

### Publish first and rename after an objection

This creates avoidable migration, reputation, package-squatting, and user-confusion costs.

### Treat Apache-2.0 as permission to use the name

Apache-2.0 explicitly separates copyright and patent permissions from trademark rights.

### Quietly reserve every identifier now

Reservation can look like public adoption, incur costs, and anchor the project to an uncleared name.

### Use a descriptive unbranded name permanently

This may reduce some branding risk but still requires collision checks and could be harder to distinguish.

## Consequences

### Positive

- Rename costs are contained before public compatibility promises.
- Package, manifest, binary, domain, and trademark checks are evaluated together.
- The release decision has dated evidence and accountable review.
- License and trademark rights remain clearly separated.

### Costs and risks

- Public branding, package publication, and some packaging work remain blocked.
- Comprehensive searches take time and may require legal expense.
- Database searches are jurisdiction-specific and can miss unregistered uses.
- A new candidate may require repeating product and design review.

## Verification

The ADR may move to Accepted only when:

- A clearance report contains every required registry and trademark search with dates and retained evidence.
- Potentially similar uses are classified by product, services, geography, status, and confusion risk.
- Package, repository, executable, bundle identifier, MCP identity, primary domain, and documentation-host candidates are available or an approved coexistence plan exists.
- Qualified legal review is recorded when related marks or uses exist.
- The founder accepts the name and the complete rename or adoption impact list.
- Release automation blocks branded artifacts until that acceptance is recorded.

## Revisit triggers

- Any new similar product, package, domain, repository, company, or mark appears before release.
- Target jurisdictions or distribution channels expand.
- The product scope moves beyond local developer port coordination.
- A proposed accepted name becomes unavailable during release preparation.

## Sources

- [USPTO Trademark Search](https://tmsearch.uspto.gov/)
- [WIPO Global Brand Database](https://branddb.wipo.int/)
- [EUIPO eSearch](https://euipo.europa.eu/eSearch/)
- [Canadian Trademarks Database](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/trademarks/canadian-trademarks-database)
- [ICANN Registration Data Lookup](https://lookup.icann.org/en)
- [GitHub repository search](https://github.com/search)
- [npm package search](https://www.npmjs.com/search)
- [PyPI package index](https://pypi.org/)
- [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
