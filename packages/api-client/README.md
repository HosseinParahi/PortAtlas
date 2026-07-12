# Local API client foundation

This private package is the schema-checked browser boundary for the `PortAtlas` working title. It is not a published package or namespace claim.

The canonical backend contract is `contracts/openapi/v1.json`. The root contract generator writes that snapshot from the backend OpenAPI model. This package's deterministic generator validates the Gate 3 health operation and writes `src/generated/openapi.ts`. Drift checking never edits the generated file:

```sh
pnpm --filter @portatlas/api-client contracts:check
```

The runtime client accepts additive response fields but copies only schema-approved health and canonical-error fields. It bounds response parsing, validates request IDs, never returns an arbitrary response body, and uses same-origin credentials. The public liveness contract contains no machine inventory or secrets.
