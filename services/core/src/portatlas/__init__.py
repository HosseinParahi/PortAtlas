"""PortAtlas (working title) native service foundation."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:
    __version__ = version("portatlas-foundation")
except PackageNotFoundError:
    # Direct source-tree execution has no installed package metadata. The root
    # pyproject remains the machine-readable version authority.
    __version__ = "0.0.0.dev0"
