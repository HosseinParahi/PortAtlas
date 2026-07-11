# ADR 0003: Host collector

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Native listener and process observation

## Context

The authoritative runtime view comes from the host operating system. It must cover TCP and UDP, IPv4 and IPv6, interface binding, process identity, and permission limitations. Docker-only collection cannot see every native process. Command output can be localized or change between operating-system releases, and PID alone is unsafe because operating systems reuse process identifiers.

## Decision

Define a typed HostCollector interface and implement macOS first:

- psutil is the primary portable source for socket and process metadata.
- lsof is a macOS fallback and corroborating source where psutil lacks fields or permissions.
- Subprocesses use fixed executables, argument arrays, explicit locale where parsing requires it, timeouts, output limits, and no shell interpolation.
- Every observation carries protocol, address family, bind address, port, state, collection time, collector source, evidence, and permission quality.
- Process identity is PID plus process start time and executable identity. PID is never a durable identity by itself.
- Command lines and working directories are collected only when permitted and are redacted before storage or output.
- Loopback, wildcard, and specific-interface bindings remain distinct. TCP and UDP remain distinct.
- Permission-denied and partial observations are valid degraded results, not silent absence.
- The service never invokes sudo automatically.
- Linux and Windows implementations must satisfy the same normalized contract; OS-specific logic stays in platform adapters.

Periodic reconciliation is mandatory. Event-like optimizations may reduce latency but cannot replace full reconciliation.

## Alternatives considered

### Parse lsof exclusively

lsof is useful on macOS but creates a single command-format dependency and weakens the cross-platform contract.

### Use psutil exclusively

psutil supplies a portable baseline, but permissions and platform-specific gaps require an evidence-preserving fallback.

### Privileged native extension

A privileged helper could reveal more process details, but it materially increases installation and security risk and is not required for the MVP.

### Run the collector in Docker

A container does not provide complete, portable visibility into host processes and sockets, especially with Docker Desktop on macOS.

## Consequences

### Positive

- Host-native runtime evidence remains authoritative and available without Docker.
- Normalized contracts support future operating systems.
- Provenance and permission quality prevent false certainty.
- Safe subprocess rules reduce command-injection and hanging-process risks.

### Costs and risks

- psutil and lsof can disagree or expose different fields.
- macOS permission changes may reduce owner or command visibility.
- UDP state and IPv4/IPv6 wildcard behavior require careful normalization.
- Real-machine fixtures are harder to make deterministic than parser fixtures.

## Verification

- Compare collector output with controlled TCP and UDP listeners on IPv4 loopback, IPv6 loopback, wildcard, and a specific interface.
- Verify PID, start time, executable, and parent metadata against a known child process.
- Run permission-limited tests and assert a degraded result rather than fabricated ownership.
- Feed versioned lsof fixtures through the parser, including malformed and localized output.
- Prove every subprocess call uses an argument array, timeout, output limit, and redaction path.
- Measure refresh propagation against the normal-load two-second target.

## Revisit triggers

- macOS removes or materially changes an observation source.
- Required accuracy cannot be reached without a signed privileged helper.
- Linux or Windows implementation shows the common contract is too macOS-shaped.
- Event APIs can replace polling while preserving reconciliation and provenance.

## Sources

- [psutil network connections](https://psutil.readthedocs.io/en/latest/#psutil.net_connections)
- [Python subprocess security and behavior](https://docs.python.org/3/library/subprocess.html)
- [Python socket address families](https://docs.python.org/3/library/socket.html)
