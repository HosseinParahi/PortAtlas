#!/usr/bin/env python3
"""Generate or verify the canonical OpenAPI contract from the app factory."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path

from portatlas.api.app import create_app

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/openapi/v1.json"


def project_version() -> str:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = project.get("project", {}).get("version")
    if not isinstance(version, str):
        raise SystemExit("pyproject.toml does not contain the product version authority")
    return version


def render() -> str:
    specification = create_app().openapi()
    if specification.get("openapi") != "3.1.0":
        raise SystemExit("the foundation contract must use OpenAPI 3.1.0")
    if specification.get("info", {}).get("version") != project_version():
        raise SystemExit("OpenAPI version drifted from pyproject.toml")
    paths = specification.get("paths", {})
    if set(paths) != {"/api/v1/health", "/api/v1/ready"}:
        raise SystemExit("Gate 3 OpenAPI must expose only health and readiness")
    health = paths["/api/v1/health"].get("get", {})
    if health.get("operationId") != "getHealth":
        raise SystemExit("health operationId must remain getHealth")
    return json.dumps(specification, indent=2, sort_keys=True) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    expected = render()
    current = CONTRACT.read_text(encoding="utf-8") if CONTRACT.is_file() else ""
    if args.check:
        if current != expected:
            print(
                "OpenAPI contract drift detected; run scripts/generate_contracts.py",
                file=sys.stderr,
            )
            return 1
        print("OpenAPI contract is current.")
        return 0
    CONTRACT.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT.write_text(expected, encoding="utf-8")
    print(f"Generated {CONTRACT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
