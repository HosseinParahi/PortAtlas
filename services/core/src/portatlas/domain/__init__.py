"""Framework-free domain kernel."""

from portatlas.domain.clock import Clock, FrozenClock, SystemClock
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.ports import PortKey
from portatlas.domain.projects import Project, ProjectInstance
from portatlas.domain.revision import Revision

__all__ = [
    "Clock",
    "ErrorCode",
    "FrozenClock",
    "OpaqueId",
    "PortKey",
    "Project",
    "ProjectInstance",
    "ResourceKind",
    "Revision",
    "SafeError",
    "SystemClock",
]
