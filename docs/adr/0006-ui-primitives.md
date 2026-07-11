# ADR 0006: UI primitives

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Browser data, interaction, accessibility, and table foundations

## Context

The dashboard is dominated by changing server state, large sortable tables, filters, dialogs, command-palette interactions, status badges, and evidence views. Building accessible keyboard behavior from unstyled div elements would be risky. Adopting a visually prescriptive component suite would make the product identity harder to evolve and could couple data behavior to presentation.

## Decision

Use a small set of headless or behavior-focused React primitives:

- TanStack Query, formerly React Query, owns remote server-state fetching, caching, invalidation, retries, and mutation lifecycle.
- Radix Primitives supplies accessible behavior for dialogs, menus, popovers, tabs, tooltips, selects, and similar composite controls.
- TanStack Table supplies the headless model for the ports, projects, conflicts, reservations, and audit tables.
- React component state owns short-lived local interaction state. Navigable filters, sorting, selection targets, and view identity belong in the URL when practical.
- A project-owned UI layer wraps Radix and TanStack integrations so screens consume stable PortAtlas components rather than vendor APIs directly.
- Native HTML elements take priority where they satisfy the interaction.
- Table sorting, filtering, and pagination use server-side contracts for large collections. Virtualization is added only after measurement and must preserve keyboard and screen-reader behavior.
- Observed, declared, reserved, leased, desired, conflicted, stale, unknown, and ignored states use text and icon semantics; color is supplementary.
- Destructive or mutating actions remain visually distinct, explain scope, and present dry-run or confirmation information.

This ADR selects interaction and data primitives, not a frozen visual theme.

## Alternatives considered

### Build every primitive in-house

This maximizes visual control but repeats difficult focus, keyboard, labeling, layering, and assistive-technology work.

### Adopt a full visual component suite

A suite such as Material UI could accelerate screens but imposes stronger visual and styling conventions and creates a broader dependency surface.

### Store all state in a global client store

This can centralize data but duplicates server-state freshness, retry, and cache invalidation behavior already handled by TanStack Query.

### Hand-build tables

Simple tables are easy, but the required sorting, filtering, selection, column visibility, and large-data behavior justify a tested headless model.

## Consequences

### Positive

- Accessible interaction behavior has a maintained baseline.
- Server state and local UI state have clear ownership.
- Headless primitives permit a distinctive visual system.
- Table capabilities can grow without replacing the data model.

### Costs and risks

- Wrappers require maintenance when vendor APIs change.
- A primitive being accessibility-oriented does not make a composed screen automatically accessible.
- Cache invalidation rules must align with ADR 0005 events.
- Headless libraries still require substantial styling and product-specific behavior.

## Verification

- Test every primary workflow using keyboard only, including focus return and escape behavior.
- Run automated accessibility checks and manual screen-reader checks on dialogs, menus, tabs, tables, forms, status announcements, and the command palette.
- Verify status meaning without color and at supported contrast modes.
- Exercise SSE invalidation, stale data, retries, optimistic mutations, rollback, and offline service states.
- Test 1,000 observations and 2,000 declarations without noticeable interaction lag.
- Pin dependency versions and run wrapper contract tests before upgrades.

## Revisit triggers

- Required interactions cannot be made accessible through the selected primitives.
- Bundle or runtime measurements show a material regression.
- The wrapper layer becomes more complex than a smaller replacement.
- A desktop shell introduces native controls that should replace browser primitives.

## Sources

- [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview)
- [Radix Primitives introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [Radix accessibility guidance](https://www.radix-ui.com/primitives/docs/overview/accessibility)
- [TanStack Table documentation](https://tanstack.com/table/latest/docs/introduction)
- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
