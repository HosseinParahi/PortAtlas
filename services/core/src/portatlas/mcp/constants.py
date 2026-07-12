"""Locked MCP revision, transport vocabulary, and assurance instructions."""

from __future__ import annotations

from enum import StrEnum

MCP_SPEC_REVISION = "2025-11-25"


class McpTransport(StrEnum):
    STDIO = "stdio"
    STREAMABLE_HTTP = "streamable-http"


MANAGED_ASSURANCE_NOTICE = (
    "A PortAtlas-managed reservation or atomic lease provides cooperative registry "
    "assurance for its recorded owner, scope, revision, and lifetime; it does not "
    "bind a socket or launch a process."
)

UNMANAGED_EVIDENCE_NOTICE = (
    "An unmanaged listener is time-bounded discovery observation and may race, "
    "be incomplete, or become stale after collection."
)
