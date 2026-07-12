#!/usr/bin/env python3
"""Run the supported Gate 3 contributor and CI command surface."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_VERSION = os.environ.get("PORTATLAS_PYTHON_VERSION", "3.13.14")
NODE_VERSION = "v24.18.0"
PNPM_VERSION = "11.10.0"
GATE2_REVISION = "e53f39916b2348e8626375bb33cac147e27bd217"


def run(command: Sequence[str], *, env: dict[str, str] | None = None) -> None:
    """Run one command from the repository root and preserve its exit status."""
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, env=env, check=True)  # noqa: S603


def uv(*arguments: str) -> None:
    run(("uv", *arguments))


def uv_run(*arguments: str) -> None:
    uv("run", "--locked", "--python", PYTHON_VERSION, *arguments)


def pnpm(*arguments: str) -> None:
    run(("corepack", "pnpm", *arguments))


def verify_toolchains() -> None:
    """Reject contributor environments that do not match the committed pins."""
    checks = (
        (("uv", "--version"), "uv 0.11.28"),
        (
            (
                "uv",
                "run",
                "--no-project",
                "--python",
                PYTHON_VERSION,
                "python",
                "--version",
            ),
            f"Python {PYTHON_VERSION}",
        ),
        (("node", "--version"), NODE_VERSION),
        (("corepack", "pnpm", "--version"), PNPM_VERSION),
    )
    for command, expected in checks:
        result = subprocess.run(  # noqa: S603
            command,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        actual = result.stdout.strip() or result.stderr.strip()
        matches = (
            actual.startswith(f"{expected} ")
            if command == ("uv", "--version")
            else actual == expected
        )
        if not matches:
            raise SystemExit(f"expected {expected!r} from {' '.join(command)}, received {actual!r}")
    print(
        f"Toolchains matched: Python {PYTHON_VERSION}, uv 0.11.28, "
        f"Node {NODE_VERSION.removeprefix('v')}, pnpm {PNPM_VERSION}."
    )


def bootstrap() -> None:
    verify_toolchains()
    uv("lock", "--check")
    uv("sync", "--locked", "--group", "dev", "--python", PYTHON_VERSION)
    pnpm("install", "--frozen-lockfile")
    uv_run(
        "pre-commit",
        "install",
        "--hook-type",
        "pre-commit",
        "--hook-type",
        "commit-msg",
    )


def docs() -> None:
    run((sys.executable, "scripts/validate_docs.py"))
    run(
        (
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_validate_docs.py",
            "-v",
        )
    )


def foundation() -> None:
    run((sys.executable, "scripts/validate_foundation.py"))


def dco() -> None:
    run(
        (
            sys.executable,
            "scripts/check_dco.py",
            "--range",
            f"{GATE2_REVISION}..HEAD",
        )
    )


def format_code() -> None:
    uv_run("ruff", "format", ".")
    pnpm("format")


def format_check() -> None:
    format_python()
    format_web()


def format_python() -> None:
    uv_run("ruff", "format", "--check", ".")


def format_web() -> None:
    pnpm("format:check")


def lint() -> None:
    lint_python()
    lint_web()


def lint_python() -> None:
    uv_run("ruff", "check", ".")
    uv_run("lint-imports")


def lint_web() -> None:
    pnpm("peers", "check")
    pnpm("lint")


def typecheck() -> None:
    typecheck_python()
    typecheck_web()


def typecheck_python() -> None:
    uv_run("mypy")


def typecheck_web() -> None:
    pnpm("typecheck")


def test_core() -> None:
    uv_run(
        "pytest",
        "-m",
        "not postgres and not packaging",
        "--cov=portatlas",
        "--cov-report=term-missing",
        "--cov-fail-under=85",
    )


def test_web() -> None:
    pnpm("test")


def contracts() -> None:
    uv_run("python", "scripts/generate_contracts.py", "--check")
    pnpm("contracts:check")


def build() -> None:
    build_python()
    build_web()


def build_python() -> None:
    uv(
        "sync",
        "--locked",
        "--group",
        "dev",
        "--group",
        "build",
        "--no-install-project",
        "--python",
        PYTHON_VERSION,
    )
    uv(
        "build",
        "--no-build-isolation",
        "--no-sources",
        "--python",
        PYTHON_VERSION,
    )


def build_web() -> None:
    pnpm("build")


def security_local() -> None:
    run((sys.executable, "scripts/validate_docs.py"))
    run((sys.executable, "scripts/validate_foundation.py", "--security-only"))


def isolation() -> None:
    uv_run("python", "scripts/check_isolation.py")


def service_smoke() -> None:
    uv_run("python", "scripts/service_smoke.py")


def audit() -> None:
    with tempfile.TemporaryDirectory(prefix="portatlas-audit-") as directory:
        requirements = Path(directory) / "all-locked-requirements.txt"
        uv(
            "export",
            "--quiet",
            "--locked",
            "--all-extras",
            "--all-groups",
            "--no-emit-project",
            "--format",
            "requirements.txt",
            "--output-file",
            str(requirements),
        )
        uv_run(
            "pip-audit",
            "--requirement",
            str(requirements),
            "--require-hashes",
            "--disable-pip",
            "--strict",
            "--progress-spinner",
            "off",
        )
    pnpm("audit", "--audit-level=low")


def pnpm_license_inventory() -> None:
    """Inventory Node licenses and reject the foundation deny set."""
    command = ("corepack", "pnpm", "licenses", "list", "--json")
    print("+", " ".join(command), flush=True)
    result = subprocess.run(  # noqa: S603
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    try:
        inventory = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit("pnpm returned an invalid license inventory") from error
    if not isinstance(inventory, dict) or "error" in inventory:
        raise SystemExit("pnpm returned an invalid license inventory")
    denied_terms = ("AGPL", "AFFERO", "SERVER SIDE PUBLIC LICENSE", "SSPL")
    denied = sorted(
        expression
        for expression in inventory
        if any(term in expression.upper() for term in denied_terms)
    )
    if denied:
        raise SystemExit(f"Node license policy rejected: {', '.join(denied)}")
    package_count = sum(
        len(packages) for packages in inventory.values() if isinstance(packages, list)
    )
    print(
        f"Node license inventory passed: {package_count} packages across "
        f"{len(inventory)} license expressions."
    )


def licenses() -> None:
    uv(
        "run",
        "--locked",
        "--all-extras",
        "--all-groups",
        "--python",
        PYTHON_VERSION,
        "pip-licenses",
        "--format=plain",
        "--order=license",
        "--fail-on",
        "GNU Affero General Public License;Server Side Public License",
        "--partial-match",
    )
    pnpm_license_inventory()


def fast() -> None:
    docs()
    foundation()
    format_check()


def all_checks() -> None:
    docs()
    foundation()
    dco()
    format_check()
    lint()
    typecheck()
    test_core()
    test_web()
    contracts()
    security_local()
    isolation()
    service_smoke()
    build()


COMMANDS: dict[str, Callable[[], None]] = {
    "all": all_checks,
    "audit": audit,
    "bootstrap": bootstrap,
    "build": build,
    "contracts": contracts,
    "docs": docs,
    "dco": dco,
    "fast": fast,
    "format": format_code,
    "format-check": format_check,
    "format-python": format_python,
    "format-web": format_web,
    "foundation": foundation,
    "licenses": licenses,
    "isolation": isolation,
    "lint": lint,
    "lint-python": lint_python,
    "lint-web": lint_web,
    "security": security_local,
    "service-smoke": service_smoke,
    "test-core": test_core,
    "test-web": test_web,
    "toolchains": verify_toolchains,
    "typecheck": typecheck,
    "typecheck-python": typecheck_python,
    "typecheck-web": typecheck_web,
    "build-python": build_python,
    "build-web": build_web,
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=sorted(COMMANDS))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        COMMANDS[args.command]()
    except FileNotFoundError as error:
        missing = error.filename or "required executable"
        print(f"missing {missing}; run the documented bootstrap first", file=sys.stderr)
        return 127
    except subprocess.CalledProcessError as error:
        return error.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
