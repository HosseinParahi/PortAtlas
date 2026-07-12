#!/usr/bin/env python3
"""Prove optional integration and packaging modules are absent from the default environment."""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_SOURCE = Path("services/core/src/portatlas")

FORBIDDEN_DEFAULT_MODULES = (
    "PyInstaller",
    "docker",
    "mcp",
    "ollama",
    "psutil",
    "psycopg",
)
FORBIDDEN_SOURCE_IMPORTS = frozenset(
    {
        *FORBIDDEN_DEFAULT_MODULES,
        "aiohttp",
        "httpx",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "urllib.request",
    }
)


def source_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def forbidden_source_imports() -> dict[str, list[str]]:
    violations: dict[str, list[str]] = {}
    source_root = ROOT / CORE_SOURCE
    for path in sorted(source_root.rglob("*.py")) if source_root.is_dir() else ():
        imported = source_imports(path)
        forbidden = sorted(
            candidate
            for candidate in FORBIDDEN_SOURCE_IMPORTS
            if any(module == candidate or module.startswith(f"{candidate}.") for module in imported)
        )
        if forbidden:
            violations[path.relative_to(ROOT).as_posix()] = forbidden
    return violations


def rust_artifacts() -> list[str]:
    paths: set[Path] = set()
    root_manifest = ROOT / "Cargo.toml"
    if root_manifest.is_file():
        paths.add(root_manifest)
    for relative in ("apps", "packages", "services", "scripts"):
        base = ROOT / relative
        if not base.is_dir():
            continue
        paths.update(path for path in base.rglob("Cargo.toml") if "node_modules" not in path.parts)
        paths.update(path for path in base.rglob("*.rs") if "node_modules" not in path.parts)
    return sorted(path.relative_to(ROOT).as_posix() for path in paths)


def main() -> int:
    present = [
        module
        for module in FORBIDDEN_DEFAULT_MODULES
        if importlib.util.find_spec(module) is not None
    ]
    source_violations = forbidden_source_imports()
    rust = rust_artifacts()
    if present or source_violations or rust:
        if present:
            print(
                f"optional modules leaked into the default environment: {', '.join(present)}",
                file=sys.stderr,
            )
        for path, modules in source_violations.items():
            print(
                f"forbidden default-path imports in {path}: {', '.join(modules)}",
                file=sys.stderr,
            )
        if rust:
            print(
                f"Rust artifacts are outside Gate 3: {', '.join(rust)}",
                file=sys.stderr,
            )
        return 1
    print(
        "Default core path excludes optional modules, process/network imports, and Rust artifacts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
