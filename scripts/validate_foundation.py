#!/usr/bin/env python3
"""Validate Gate 3 repository contracts without third-party imports."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    ".node-version",
    ".npmrc",
    ".pre-commit-config.yaml",
    ".python-version",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    "apps/web/package.json",
    "contracts/openapi/v1.json",
    "docs/project/gate-3-evidence.md",
    "docs/project/gate-3-packaging-research.md",
    "docs/testing/test-strategy.md",
    "package.json",
    "packages/api-client/package.json",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
    "pyproject.toml",
    "services/core/src/portatlas/__init__.py",
    "scripts/check_isolation.py",
    "scripts/service_smoke.py",
    "uv.lock",
)
FIXTURE_FAMILIES = (
    "ai",
    "allocator",
    "capacity",
    "docker",
    "project_identity",
    "runtime",
    "scanners",
    "security",
)
ACTION_REF_RE = re.compile(
    r"^\s*(?:-\s*)?uses:\s*(?P<reference>\"[^\"]+\"|'[^']+'|[^#\s]+)", re.MULTILINE
)
REMOTE_ACTION_RE = re.compile(r"[^@\s]+@[0-9a-f]{40}")
DOCKER_ACTION_RE = re.compile(r"docker://.+@sha256:[0-9a-f]{64}")
SERVICE_IMAGE_RE = re.compile(
    r"^\s+image:\s*(?P<reference>\"[^\"]+\"|'[^']+'|[^#\s]+)",
    re.MULTILINE,
)
SERVICE_IMAGE_DIGEST_RE = re.compile(r"[^@\s]+@sha256:[0-9a-f]{64}")
PR_HEAD_REF = "github.event.pull_request.head.sha || github.sha"
WRITE_PERMISSION_RE = re.compile(
    r"^\s*(?:permissions|actions|attestations|checks|contents|deployments|discussions|"
    r"id-token|issues|models|packages|pages|pull-requests|security-events|statuses):"
    r"\s*write\s*(?:#.*)?$",
    re.MULTILINE,
)
PUBLICATION_COMMAND_RE = re.compile(
    r"(?:\b(?:npm|pnpm|yarn|uv)\s+publish\b|\btwine\s+upload\b|\bdocker\s+push\b)",
    re.IGNORECASE,
)
TEST_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
FOCUSED_TEST_ID_RE = re.compile(
    r"\b(?:UT|IT|CT|E2E|PERF|UAT|TEST|SEC-T|AI-EVAL)(?:-[A-Z0-9]+)*-\d{3}\b"
)
MIN_FIXTURE_SCENARIOS = 3
MAX_FIXTURE_BYTES = 1_048_576
SYNTHETIC_SENSITIVITIES = frozenset({"synthetic", "synthetic-canary"})
TELEMETRY_DEPENDENCIES = (
    "@sentry/",
    "analytics-node",
    "datadog",
    "newrelic",
    "opentelemetry-exporter",
    "posthog",
    "sentry-sdk",
)


def load_json(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        path = ROOT / relative
        try:
            substantive = path.is_file() and bool(path.read_bytes().strip())
        except OSError:
            substantive = False
        if not substantive:
            errors.append(f"missing substantive foundation file: {relative}")


def validate_python_metadata(errors: list[str]) -> None:
    project_path = ROOT / "pyproject.toml"
    try:
        project = tomllib.loads(project_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        errors.append(f"invalid foundation metadata: pyproject.toml: {error}")
    else:
        metadata = project.get("project", {})
        if not isinstance(metadata, dict):
            errors.append("invalid foundation metadata: pyproject.toml project must be a table")
        else:
            if metadata.get("name") != "portatlas-foundation":
                errors.append("Python distribution must retain the private foundation name")
            if metadata.get("version") != "0.0.0.dev0":
                errors.append("pyproject.toml must be the 0.0.0.dev0 version authority")
            if "Private :: Do Not Upload" not in metadata.get("classifiers", []):
                errors.append(
                    "Python metadata must prohibit publication while the name gate is open"
                )
        tool = project.get("tool", {})
        uv_config = tool.get("uv", {}) if isinstance(tool, dict) else {}
        if not isinstance(uv_config, dict) or uv_config.get("default-groups") != ["dev"]:
            errors.append("default Python bootstrap must exclude the packaging research group")


def validate_javascript_metadata(errors: list[str]) -> None:
    package_paths = [ROOT / "package.json"]
    package_paths.extend(sorted((ROOT / "apps").glob("*/package.json")))
    package_paths.extend(sorted((ROOT / "packages").glob("*/package.json")))
    for path in package_paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            package = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid foundation metadata: {relative}: {error}")
            continue
        if not isinstance(package, dict):
            errors.append(f"invalid foundation metadata: {relative} must be an object")
            continue
        if package.get("private") is not True:
            errors.append(f"{relative} must be private while the name gate is open")
        if "publishConfig" in package:
            errors.append(f"publication configuration is forbidden in {relative}")
        scripts = package.get("scripts", {})
        if isinstance(scripts, dict) and any(
            "publish" in str(name).lower()
            or PUBLICATION_COMMAND_RE.search(str(command)) is not None
            for name, command in scripts.items()
        ):
            errors.append(f"publication command is forbidden in {relative}")


def validate_toolchain_pins(errors: list[str]) -> None:
    pins = (
        (".python-version", "3.13.14", "Python baseline must be pinned to 3.13.14"),
        (".node-version", "24.18.0", "Node LTS baseline must be pinned to 24.18.0"),
    )
    for relative, expected, message in pins:
        try:
            actual = (ROOT / relative).read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            continue
        if actual != expected:
            errors.append(message)


def validate_metadata(errors: list[str]) -> None:
    validate_python_metadata(errors)
    validate_javascript_metadata(errors)
    validate_toolchain_pins(errors)


def validate_fixture_scenario(
    item: object,
    relative: str,
    scenario_ids: set[str],
    seeds: set[int],
    errors: list[str],
) -> None:
    if not isinstance(item, dict):
        errors.append(f"fixture scenario must be an object: {relative}")
        return
    required = {"id", "kind", "seed", "sensitivity", "test_ids"}
    if not required.issubset(item):
        errors.append(f"fixture scenario lacks metadata: {relative}")
        return
    scenario_id = item.get("id")
    if not isinstance(scenario_id, str) or not scenario_id.strip():
        errors.append(f"fixture scenario needs a non-empty id: {relative}")
    elif scenario_id in scenario_ids:
        errors.append(f"duplicate fixture scenario id {scenario_id}: {relative}")
    else:
        scenario_ids.add(scenario_id)
    seed = item.get("seed")
    if not isinstance(seed, int) or isinstance(seed, bool):
        errors.append(f"fixture scenario needs an integer seed: {relative}")
    elif seed in seeds:
        errors.append(f"duplicate fixture scenario seed {seed}: {relative}")
    else:
        seeds.add(seed)
    if item.get("sensitivity") not in SYNTHETIC_SENSITIVITIES:
        errors.append(f"fixture scenario has non-synthetic sensitivity: {relative}")
    test_ids = item.get("test_ids")
    if (
        not isinstance(test_ids, list)
        or not test_ids
        or any(
            not isinstance(test_id, str) or not TEST_ID_RE.fullmatch(test_id)
            for test_id in test_ids
        )
    ):
        errors.append(f"fixture scenario needs non-empty stable test IDs: {relative}")


def validate_fixture_manifest(
    family: str, relative: str, manifest: dict[str, object], errors: list[str]
) -> None:
    if manifest.get("schema_version") != 1 or manifest.get("family") != family:
        errors.append(f"fixture identity mismatch: {relative}")
    purpose = manifest.get("purpose")
    if not isinstance(purpose, str) or not purpose.strip():
        errors.append(f"fixture manifest needs a substantive purpose: {relative}")
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) < MIN_FIXTURE_SCENARIOS:
        errors.append(f"fixture family needs benign, degraded, and adversarial cases: {relative}")
        return
    kinds = {item.get("kind") for item in scenarios if isinstance(item, dict)}
    if kinds != {"adversarial", "benign", "degraded"}:
        errors.append(f"fixture kinds are incomplete: {relative}")
    scenario_ids: set[str] = set()
    seeds: set[int] = set()
    for item in scenarios:
        validate_fixture_scenario(item, relative, scenario_ids, seeds, errors)


def validate_fixtures(errors: list[str]) -> None:
    for family in FIXTURE_FAMILIES:
        relative = f"tests/fixtures/{family}/manifest.json"
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing fixture manifest: {relative}")
            continue
        try:
            manifest = load_json(relative)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid fixture manifest {relative}: {error}")
            continue
        if not isinstance(manifest, dict):
            errors.append(f"fixture manifest must be an object: {relative}")
            continue
        validate_fixture_manifest(family, relative, manifest, errors)


def validate_focused_test_ids(errors: list[str]) -> None:  # noqa: PLR0912
    definitions: Counter[str] = Counter()
    testing_root = ROOT / "docs" / "testing"
    for path in sorted(testing_root.glob("*.md")) if testing_root.is_dir() else ():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            errors.append(f"cannot inspect focused test definitions: {path}: {error}")
            continue
        for line in lines:
            stripped = line.strip()
            if not (stripped.startswith("|") and stripped.endswith("|")):
                continue
            first_cell = stripped[1:-1].split("|", 1)[0].strip().strip("`*_ ")
            if FOCUSED_TEST_ID_RE.fullmatch(first_cell):
                definitions[first_cell] += 1

    references: set[str] = set()
    for family in FIXTURE_FAMILIES:
        path = ROOT / "tests" / "fixtures" / family / "manifest.json"
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if not isinstance(manifest, dict) or not isinstance(manifest.get("scenarios"), list):
            continue
        for scenario in manifest["scenarios"]:
            if not isinstance(scenario, dict) or not isinstance(scenario.get("test_ids"), list):
                continue
            references.update(
                test_id
                for test_id in scenario["test_ids"]
                if isinstance(test_id, str) and FOCUSED_TEST_ID_RE.fullmatch(test_id)
            )

    test_root = ROOT / "tests"
    for path in sorted(test_root.rglob("*.py")) if test_root.is_dir() else ():
        try:
            module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError):
            continue
        docstring = ast.get_docstring(module, clean=False) or ""
        references.update(FOCUSED_TEST_ID_RE.findall(docstring))

    for identifier, count in sorted(definitions.items()):
        if count > 1:
            errors.append(f"focused test ID is defined more than once: {identifier}")
    errors.extend(
        f"undefined focused test ID: {identifier}"
        for identifier in sorted(references - set(definitions))
    )


def validate_dco_workflow(content: str, relative: str, errors: list[str]) -> None:
    """Keep pull-request provenance checks on authored commits, not merge refs."""
    if (
        "pull_request" in content
        and "scripts/check_dco.py" in content
        and PR_HEAD_REF not in content
    ):
        errors.append(
            "pull-request DCO check must inspect the authored head, not GitHub's "
            f"synthetic merge commit: {relative}"
        )


def validate_workflow(errors: list[str]) -> None:
    workflow_root = ROOT / ".github/workflows"
    workflow_paths = sorted(
        {*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")},
        key=lambda path: path.as_posix(),
    )
    for path in workflow_paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"cannot inspect workflow {relative}: {error}")
            continue
        permissions = re.search(
            r"^permissions:\s*(?:#.*)?$\n(?P<body>(?:^[ \t]+[^\n]*\n?)*)",
            content,
            flags=re.MULTILINE,
        )
        permission_body = permissions.group("body") if permissions else ""
        contents_read = re.search(
            r"^[ \t]+contents:\s*read\s*(?:#.*)?$", permission_body, re.MULTILINE
        )
        if contents_read is None:
            errors.append(
                f"{relative} must declare least-privilege read-only repository permissions"
            )
        if WRITE_PERMISSION_RE.search(content):
            errors.append(f"{relative} grants write permission during the foundation gate")
        for match in ACTION_REF_RE.finditer(content):
            reference = match.group("reference").strip("\"'")
            if reference.startswith("./"):
                continue
            if reference.startswith("docker://"):
                pinned = DOCKER_ACTION_RE.fullmatch(reference) is not None
            else:
                pinned = REMOTE_ACTION_RE.fullmatch(reference) is not None
            if not pinned:
                errors.append(
                    f"{relative} contains an action reference that is not SHA-pinned: {reference}"
                )
        for match in SERVICE_IMAGE_RE.finditer(content):
            reference = match.group("reference").strip("\"'")
            if SERVICE_IMAGE_DIGEST_RE.fullmatch(reference) is None:
                errors.append(f"{relative} service image is not digest-pinned: {reference}")
        validate_dco_workflow(content, relative, errors)
        lowered = content.lower()
        publication_terms = ("npm publish", "pnpm publish", "uv publish", "pypi", "docker push")
        if any(term in lowered for term in publication_terms):
            errors.append(f"{relative} must not publish artifacts or namespaces")


def validate_security(errors: list[str]) -> None:
    dependency_paths = [
        ROOT / "pyproject.toml",
        ROOT / "package.json",
        ROOT / "uv.lock",
        ROOT / "pnpm-lock.yaml",
    ]
    dependency_paths.extend((ROOT / "apps").glob("*/package.json"))
    dependency_paths.extend((ROOT / "packages").glob("*/package.json"))
    dependency_text: list[str] = []
    for path in dependency_paths:
        if not path.is_file():
            continue
        try:
            dependency_text.append(path.read_text(encoding="utf-8").lower())
        except (OSError, UnicodeError) as error:
            errors.append(
                f"cannot inspect dependency metadata {path.relative_to(ROOT).as_posix()}: {error}"
            )
    combined = "\n".join(dependency_text)
    errors.extend(
        f"telemetry dependency is forbidden: {dependency}"
        for dependency in TELEMETRY_DEPENDENCIES
        if dependency in combined
    )
    errors.extend(
        f"fixture exceeds the Gate 3 one-megabyte limit: {path.relative_to(ROOT)}"
        for path in (ROOT / "tests" / "fixtures").rglob("*")
        if path.is_file() and path.stat().st_size > MAX_FIXTURE_BYTES
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--security-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors: list[str] = []
    validate_security(errors)
    if not args.security_only:
        validate_required(errors)
        validate_metadata(errors)
        validate_fixtures(errors)
        validate_focused_test_ids(errors)
        validate_workflow(errors)
    if errors:
        for error in sorted(set(errors)):
            print(f"foundation: {error}", file=sys.stderr)
        return 1
    print("Gate 3 foundation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
