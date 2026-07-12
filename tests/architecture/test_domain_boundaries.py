"""TEST-ARCH-001: inward-only dependency and optional-integration tests."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPOSITORY_ROOT / "services" / "core" / "src" / "portatlas"
DOMAIN_ROOT = PACKAGE_ROOT / "domain"
ADAPTER_ROOTS = {
    "ai",
    "api",
    "cli",
    "collectors",
    "mcp",
    "persistence",
    "scanners",
}

BANNED_DOMAIN_ROOTS = {
    "alembic",
    "docker",
    "fastapi",
    "httpx",
    "mcp",
    "ollama",
    "platformdirs",
    "psutil",
    "pydantic",
    "requests",
    "sqlalchemy",
    "typer",
}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_domain_uses_only_standard_library_and_other_domain_modules(self) -> None:
        violations: dict[str, list[str]] = {}
        for path in sorted(DOMAIN_ROOT.rglob("*.py")):
            banned = sorted(imported_roots(path) & BANNED_DOMAIN_ROOTS)
            if banned:
                violations[str(path.relative_to(REPOSITORY_ROOT))] = banned

        self.assertEqual(violations, {})

    def test_adapters_do_not_import_sibling_adapters(self) -> None:
        violations: dict[str, list[str]] = {}
        for adapter in sorted(ADAPTER_ROOTS):
            adapter_root = PACKAGE_ROOT / adapter
            for path in sorted(adapter_root.rglob("*.py")):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                sibling_imports: set[str] = set()
                for node in ast.walk(tree):
                    modules: list[str] = []
                    if isinstance(node, ast.Import):
                        modules.extend(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        modules.append(node.module)
                    for module in modules:
                        parts = module.split(".")
                        if (
                            len(parts) > 1
                            and parts[0] == "portatlas"
                            and parts[1] in ADAPTER_ROOTS
                            and parts[1] != adapter
                        ):
                            sibling_imports.add(parts[1])
                if sibling_imports:
                    violations[str(path.relative_to(REPOSITORY_ROOT))] = sorted(sibling_imports)

        self.assertEqual(violations, {})

    def test_core_package_has_no_concrete_docker_or_ollama_adapter_in_gate_three(self) -> None:
        forbidden_paths = (
            PACKAGE_ROOT / "collectors" / "docker",
            PACKAGE_ROOT / "ai" / "ollama.py",
        )

        self.assertTrue(all(not path.exists() for path in forbidden_paths))


if __name__ == "__main__":
    unittest.main()
