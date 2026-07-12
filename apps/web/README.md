# Browser foundation

This private React workspace is the Gate 3 browser foundation for the `PortAtlas` working title. It proves the selected architecture seams without claiming that later inventory workflows are implemented.

The shell uses TanStack Query for local API state, TanStack Table for semantic inventory presentation, and a project-owned Radix Dialog wrapper for composite interaction behavior. Fixture rows are visibly labeled as synthetic. Statuses always include words and symbols; color is supplementary.

The product boundary is deliberate: reservations and atomic leases coordinate clients that honor the registry. Runtime discovery is point-in-time evidence, and an unmanaged process can ignore the registry. Source patching, managed launch, and process termination are outside the MVP.

From the repository root, use the pinned workspace commands:

```sh
pnpm --filter @portatlas/web format:check
pnpm --filter @portatlas/web lint
pnpm --filter @portatlas/web typecheck
pnpm --filter @portatlas/web test
pnpm --filter @portatlas/web build
```

Tests cover semantic landmarks, assurance language, table structure, Radix focus return, health-client integration, and automatically detectable accessibility defects. Manual keyboard and screen-reader verification remains required at the release gates that introduce complete workflows.
