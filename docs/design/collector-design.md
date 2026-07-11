# PortAtlas Collector Design

## Objective

Collectors produce time-bounded runtime evidence without changing host or container state. The macOS implementation is first, while Linux and Windows remain explicit adapter contracts. Collector failure degrades visibility and never crashes the native service.

## Contracts

~~~python
class Collector(Protocol):
    descriptor: CollectorDescriptor

    async def probe(self) -> CapabilityReport: ...

    async def collect(
        self,
        request: CollectionRequest,
        cancellation: CancellationToken,
    ) -> CollectionResult: ...
~~~

CollectionRequest contains source, protocol and namespace scope, deadline, output budget, and reason. CollectionResult contains:

- collector ID and version;
- snapshot scope;
- started and completed time;
- completeness: complete, partial, or failed;
- normalized observation candidates;
- process or container identities;
- limitations;
- safe diagnostics;
- source fingerprint or Engine API version where relevant.

The result contains no raw unbounded command output.

## Coordinator

~~~mermaid
flowchart LR
    T[Timer, event, or manual refresh]
    C[Collector coordinator]
    PS[psutil adapter]
    LF[lsof -nP fallback]
    DK[Docker SDK adapter]
    N[Normalizer]
    R[Reconciliation]
    DB[(Registry)]

    T --> C
    C --> PS
    PS -->|missing relationships or unsupported view| LF
    C --> DK
    PS --> N
    LF --> N
    DK --> N
    N --> R
    R --> DB
~~~

The coordinator coalesces equivalent refreshes, bounds concurrency, propagates cancellation, and keeps adapter limitations separate. It may combine psutil and lsof evidence only through deterministic identity rules.

## macOS host collector

### Primary path: psutil

The primary adapter uses psutil to obtain network connections and process metadata when permitted. It captures:

- TCP and UDP;
- IPv4 and IPv6;
- listener state where the protocol exposes one;
- local address and port;
- PID;
- process start time;
- executable identity and safe executable name;
- user;
- parent PID and start time when available;
- current working directory when permitted;
- redacted command metadata;
- permission failures by field.

psutil version and platform version are recorded in CollectionRun metadata.

### Fallback path: lsof

The fallback invokes lsof through a strict argument array equivalent to:

~~~text
lsof -nP -iTCP -sTCP:LISTEN
lsof -nP -iUDP
~~~

Exact flags may be refined by fixture-backed research, but the contract is:

- no shell interpolation;
- fixed executable lookup and identity;
- locale fixed for parsing where possible;
- deadline and termination escalation;
- stdout and stderr byte limits;
- tested parser for supported field layouts;
- no assumption that truncated or permission-denied output is complete.

lsof fills gaps or provides a fallback snapshot. It is not merged by matching PID alone; process start time and executable evidence are required when available.

### Process argument safety

Command lines can contain passwords, tokens, database URLs, cookies, and user content. The collector:

- does not persist the raw command line;
- recognizes only an allowlist of safe executable and port flags;
- redacts values after secret-like flag names;
- stores a structured safe command summary;
- records that redaction occurred;
- omits uncertain values rather than risking disclosure.

## Docker collector

The Docker adapter uses an official or well-maintained Docker SDK and negotiates the Engine API version with the daemon.

It captures:

- running and stopped containers within configured retention;
- container ID, safe name, image and tag;
- compose project and service labels;
- selected non-secret labels;
- networks;
- internal exposed ports;
- published host bindings including interface;
- health;
- start time and state;
- restart policy;
- safe project-association evidence.

Internal EXPOSE or container-port metadata is not a host observation. Only a published host binding creates a host namespace observation.

### Docker events

When available, Docker events trigger a debounced targeted refresh. Periodic reconciliation remains authoritative because event streams can disconnect or omit history. Reconnection performs a full comparable-scope snapshot before retiring old state.

### Docker security

The Docker socket is privileged. The adapter:

- never exposes the socket or SDK client outside the module;
- never accepts arbitrary Docker operations from REST, MCP, CLI, or AI;
- makes read-only calls in the MVP;
- uses bounded API responses and timeouts;
- reports permission and Desktop-unavailable states;
- never opens an unauthenticated remote Docker endpoint.

## Normalization

### Protocol and state

Protocols are tcp or udp. TCP listening is explicit. UDP has no connection-oriented listening state, so a bound UDP socket is represented as bound with protocol-specific semantics rather than mislabeled TCP listening.

### Address

The normalizer preserves:

- 127.0.0.1;
- ::1;
- 0.0.0.0;
- ::;
- specific IPv4 and IPv6 interfaces;
- address family;
- IPv6 dual-stack uncertainty.

It does not collapse wildcard and loopback. Conflict evaluation uses platform-aware bind-overlap rules.

### Host and container namespaces

Every port carries namespace:

- host;
- container with container identity;
- future remote host with host identity.

Docker host publication produces both container metadata and a host binding observation linked by evidence.

### Process identity

Identity fingerprint uses PID, start time, and executable identity. If start time is unavailable, the observation records an identity-limited state. Association confidence is lower and reconciliation avoids destructive replacement based on PID alone.

## Project association

Associating a runtime process with a ProjectInstance is evidence-based:

1. permitted current working directory inside an instance;
2. executable path inside an instance;
3. Docker compose labels mapped to a discovered compose project;
4. parent-process evidence;
5. safe command metadata;
6. user confirmation.

Absolute path containment uses canonical paths. Ambiguous matches remain unassociated rather than choosing by name.

## Reconciliation and freshness

~~~mermaid
stateDiagram-v2
    [*] --> current: successful observation
    current --> current: seen in comparable snapshot
    current --> stale: absent from complete comparable snapshot
    current --> uncertain: collector partial or permission reduced
    uncertain --> current: observed again
    uncertain --> stale: later complete snapshot proves absence
    stale --> current: observed again
    stale --> expired: retention elapsed
~~~

Rules:

- only a complete result can mark unseen records stale;
- a partial result may add or refresh observations;
- adapter failure preserves last-known-good state and timestamps;
- source scopes are independent;
- host and Docker absence are not interchangeable;
- every response exposes freshness and collector status.

## Scheduling

Default scheduling is configurable. The architecture supports:

- periodic host reconciliation;
- Docker event-triggered debounced refresh plus periodic reconciliation;
- manual refresh;
- refresh before high-value preflight;
- backoff after repeated adapter failure;
- pause and battery-aware future policy.

Only one comparable host snapshot runs at a time. Manual requests may join an active run.

## Failure mapping

| Failure | Completeness | Behavior |
| --- | --- | --- |
| psutil access denied for some processes | partial | Keep visible observations; add field and scope limitations |
| psutil unsupported field | partial | Invoke tested lsof fallback where eligible |
| lsof missing | partial or failed | Preserve psutil result and report capability gap |
| lsof timeout or output limit | failed for fallback scope | Discard incomplete fallback proof; keep last-known-good |
| Docker daemon unavailable | failed for Docker | Continue host collection |
| Docker API mismatch | failed for Docker | Report negotiated-version error without raw daemon data |
| Cancellation | partial or cancelled | Never use absence to retire state |
| Normalization rejects malformed record | partial | Quarantine record with bounded counter and safe code |

## Platform contracts

Linux and Windows adapters implement the same CollectionResult semantics. OS-specific discovery, privilege behavior, and address semantics remain isolated. Domain rules receive normalized evidence plus explicit platform behavior metadata.

## Verification

Collector fixtures cover:

- TCP and UDP;
- IPv4 and IPv6;
- wildcard and loopback;
- PID reuse;
- permission denial;
- truncated and localized command output;
- spaces and unusual characters in process metadata;
- Docker internal versus published ports;
- compose labels;
- daemon disconnect and restart;
- redaction of secret-bearing arguments;
- cancellation and output limits.
