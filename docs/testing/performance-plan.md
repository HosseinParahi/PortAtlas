# Performance Plan

Status: **Proposed pre-implementation contract**

## Reference workload

The MVP capacity target is 500 repositories, 2,000 parsed declarations, and 1,000 current runtime observations on a documented developer laptop. Tests use deterministic data and report hardware, OS, power state, build type, database profile, browser, and cold or warm condition.

## Stable benchmarks

| Test ID | Measurement | Target |
|---|---|---|
| PERF-COL-001 | Collector observation through committed normalized state under normal load | p95 within 1.5 seconds, leaving browser rendering budget |
| PERF-SSE-001 | Committed revision through SSE invalidation to visible browser state | p95 within 0.5 seconds and end-to-end p95 within two seconds over 100 controlled changes |
| PERF-SCN-001 | Initial scan of the 500-repository corpus | Complete without unbounded memory growth; duration and per-parser rates reported before threshold lock |
| PERF-API-001 | Cursor page read of 100 inventory rows at target capacity | warm p95 at or below 200 ms locally; cold p95 reported |
| PERF-UI-001 | Filter, sort, select, and open provenance at target capacity | p95 response to next rendered state at or below 100 ms for local interactions and 500 ms when a server read is required |
| PERF-ALC-001 | Atomic lease creation without contention | warm p95 at or below 100 ms; contention test proves uniqueness and reports tail latency |
| PERF-DB-001 | Startup integrity and migration on a target-size database | No partial availability; measured budget finalized with packaging prototype |
| PERF-INSTALL-001 | Clean install to authenticated dashboard | Median under five minutes across three clean supported-macOS runs |

## Method

- Use monotonic timestamps at collector, commit, event emission, client receipt, and render assertion.
- Warm up explicitly and keep cold-start results separate.
- Run enough iterations to report median, p95, maximum, error rate, and confidence caveats.
- Store machine-readable summaries without project contents or personal paths.
- Compare against an accepted baseline and investigate regressions greater than 10% even when the absolute threshold passes.
- Exercise pagination and virtualization without lowering row-count correctness assertions.

“No noticeable UI lag” is operationalized by the interaction targets above, complete row counts, and manual UAT at compact and full layouts. Animation time is excluded only when the interaction is already acknowledged and accessible reduced-motion behavior is tested.

## Resource and degradation budgets

Memory, CPU, battery, database size, event backlog, scan queue, and optional-model resource use are measured. Exact steady-state resource ceilings are set after the Gate 3 prototype; the release cannot proceed without documented values. Docker and AI timeouts must not consume the core worker pool or delay authoritative allocation beyond its target.
