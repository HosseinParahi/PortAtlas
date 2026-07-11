#!/usr/bin/env python3
"""Validate the PortAtlas documentation checkpoint with the standard library."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import unquote


REQUIRED_FILES: tuple[str, ...] = (
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SUPPORT.md",
    "docs/project/work-log.md",
    "docs/project/assumptions-register.md",
    "docs/project/decision-register.md",
    "docs/project/risk-register.md",
    "docs/project/open-questions.md",
    "docs/project/research-sources.md",
    "docs/project/first-checkpoint-plan.md",
    "docs/product/project-charter.md",
    "docs/product/vision.md",
    "docs/product/brd.md",
    "docs/product/prd.md",
    "docs/product/personas.md",
    "docs/product/user-journeys.md",
    "docs/product/scope-and-non-goals.md",
    "docs/product/success-metrics.md",
    "docs/product/wireframes.md",
    "docs/product/information-architecture.md",
    "docs/product/backlog.md",
    "docs/product/roadmap.md",
    "docs/requirements/srs.md",
    "docs/requirements/functional-requirements.md",
    "docs/requirements/non-functional-requirements.md",
    "docs/requirements/acceptance-criteria.md",
    "docs/requirements/traceability-matrix.md",
    "docs/requirements/assumptions-and-constraints.md",
    "docs/architecture/system-context.md",
    "docs/architecture/system-architecture.md",
    "docs/architecture/hld.md",
    "docs/design/lld.md",
    "docs/design/domain-model.md",
    "docs/design/data-model.md",
    "docs/design/api-design.md",
    "docs/design/mcp-design.md",
    "docs/design/collector-design.md",
    "docs/design/scanner-design.md",
    "docs/design/allocator-design.md",
    "docs/design/conflict-engine.md",
    "docs/design/configuration-schema.md",
    "docs/design/project-manifest-schema.md",
    "docs/design/error-model.md",
    "docs/design/local-ai-design.md",
    "docs/design/ollama-provider.md",
    "docs/design/ai-context-builder.md",
    "docs/design/ai-structured-output.md",
    "docs/security/threat-model.md",
    "docs/security/privacy-model.md",
    "docs/security/permissions.md",
    "docs/security/secret-redaction.md",
    "docs/security/mcp-safety.md",
    "docs/security/local-ai-threat-model.md",
    "docs/security/prompt-injection-defense.md",
    "docs/security/ai-data-handling.md",
    "docs/testing/test-strategy.md",
    "docs/testing/qa-plan.md",
    "docs/testing/uat-plan.md",
    "docs/testing/test-data-strategy.md",
    "docs/testing/platform-compatibility.md",
    "docs/testing/performance-plan.md",
    "docs/testing/local-ai-evaluation.md",
    "docs/operations/development-setup.md",
    "docs/operations/local-installation.md",
    "docs/operations/configuration.md",
    "docs/operations/backup-and-restore.md",
    "docs/operations/troubleshooting.md",
    "docs/operations/diagnostic-bundle.md",
    "docs/operations/ollama-setup.md",
    "docs/operations/local-ai-troubleshooting.md",
    "docs/releases/release-process.md",
    "docs/releases/versioning.md",
    "docs/releases/mvp-checklist.md",
    "docs/adr/README.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/CODEOWNERS",
    "scripts/validate_docs.py",
    "tests/test_validate_docs.py",
)

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
IGNORED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_DEFINITION_RE = re.compile(r"^\s*\[([^\]]+)\]:\s*(<[^>]+>|\S+)")
REFERENCE_USE_RE = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
PLACEHOLDER_RE = re.compile(r"\b(?:TO" + r"DO|T" + r"BD|FIX" + r"ME|CHANGE" + r"ME)\b", re.I)
PERSONAL_PATH_PATTERNS = (
    re.compile(r"/Us" + r"ers/(?!Shared(?:/|\s|$))[^/\s]+/"),
    re.compile(r"/ho" + r"me/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Us" + r"ers\\[^\\\s]+\\"),
    re.compile(r"/Vol" + r"umes/[^/\s]+/(?:Github|Documents|Desktop|Downloads)/"),
)
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("fine-grained GitHub token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("OpenAI-style token", re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b")),
    (
        "credential-bearing URL",
        re.compile(r"\b(?:https?|postgres(?:ql)?|mysql)://[^\s/:]+:[^\s/@]+@", re.I),
    ),
)

REQUIREMENT_ID_RE = re.compile(
    r"\b(?:BO-\d{2,3}|PF-\d{3}|US-\d{3}|BRD-(?:OBJ|REQ)-\d{3}|"
    r"PRD-(?:FEAT|STORY|US)-\d{3}|"
    r"SRS-(?:COL|SCN|REG|ALC|CNF|API|UI|CLI|MCP|SEC|AI|OPS|NFR)-\d{3})\b"
)
SRS_ID_RE = re.compile(
    r"\bSRS-(?:COL|SCN|REG|ALC|CNF|API|UI|CLI|MCP|SEC|AI|OPS|NFR)-\d{3}\b"
)
TEST_ID_RE = re.compile(
    r"\b(?:UT|IT|CT|E2E|PERF|UAT|TEST|SEC-T|AI-EVAL)(?:-[A-Z0-9]+)*-\d{3}\b|\bUAT-\d{3}\b"
)
VT_SRS_ID_RE = re.compile(
    r"\bVT-SRS-(?:COL|SCN|REG|ALC|CNF|API|UI|CLI|MCP|SEC|AI|OPS|NFR)-\d{3}\b"
)
@dataclass(frozen=True, order=True)
class Issue:
    """One deterministic validation finding."""

    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        location = self.path if self.line <= 0 else f"{self.path}:{self.line}"
        return f"{location}: {self.code}: {self.message}"


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _try_read_text(path: Path) -> str | None:
    try:
        return _read_text(path)
    except (OSError, UnicodeDecodeError):
        return None


def _is_ignored(path: Path, root: Path) -> bool:
    relative_parts = path.relative_to(root).parts
    return any(part in IGNORED_PARTS for part in relative_parts)


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or _is_ignored(path, root):
            continue
        if path.name in {"LICENSE", ".editorconfig", ".gitattributes", ".gitignore"}:
            yield path
        elif path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if path.is_file() and not _is_ignored(path, root):
            yield path


def check_required_files(root: Path, required_files: Sequence[str]) -> list[Issue]:
    issues: list[Issue] = []
    for relative in required_files:
        path = root / relative
        if not path.is_file():
            issues.append(Issue(relative, 0, "REQUIRED_MISSING", "required file does not exist"))
            continue
        try:
            content = _read_text(path)
        except UnicodeDecodeError:
            issues.append(Issue(relative, 0, "REQUIRED_ENCODING", "file is not valid UTF-8 text"))
            continue
        except OSError as error:
            details = error.strerror or str(error)
            issues.append(Issue(relative, 0, "REQUIRED_READ", f"required file cannot be read: {details}"))
            continue
        if not content.strip():
            issues.append(Issue(relative, 0, "REQUIRED_EMPTY", "required file has no substantive content"))
    return issues


def check_text_readability(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_text_files(root):
        relative = _relative(path, root)
        try:
            _read_text(path)
        except UnicodeDecodeError:
            issues.append(Issue(relative, 0, "CONTENT_ENCODING", "text file is not valid UTF-8"))
        except OSError as error:
            details = error.strerror or str(error)
            issues.append(Issue(relative, 0, "CONTENT_READ", f"text file cannot be read: {details}"))
    return issues


def _slugify_heading(heading: str) -> str:
    value = re.sub(r"<[^>]+>", "", heading.strip().lower())
    value = re.sub(r"[`*_~]", "", value)
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "-", value)
    return value.strip("-")


def _markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: Counter[str] = Counter()
    content = _try_read_text(path)
    if content is None:
        return anchors
    for line in content.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = _slugify_heading(match.group(1))
        if not base:
            continue
        count = counts[base]
        counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def _link_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    if re.search(r"\s+[\"']", value):
        value = re.split(r"\s+[\"']", value, maxsplit=1)[0]
    return value


def _check_link_destination(
    root: Path,
    source: Path,
    relative: str,
    line_number: int,
    raw_destination: str,
) -> list[Issue]:
    destination = unquote(_link_destination(raw_destination))
    schemes = ("http://", "https://", "mailto:", "tel:", "data:")
    if not destination or destination.startswith(schemes):
        return []

    path_part, separator, fragment = destination.partition("#")
    path_part = path_part.split("?", 1)[0]
    if path_part.startswith("/"):
        return [Issue(relative, line_number, "LINK_ABSOLUTE", f"local link must be relative: {destination}")]

    target = source if not path_part else (source.parent / path_part).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return [Issue(relative, line_number, "LINK_OUTSIDE_ROOT", f"link escapes repository: {destination}")]
    if not target.exists():
        return [Issue(relative, line_number, "LINK_TARGET_MISSING", f"target does not exist: {destination}")]
    if separator and fragment and target.is_file() and target.suffix.lower() == ".md":
        normalized_fragment = _slugify_heading(fragment)
        if normalized_fragment not in _markdown_anchors(target):
            return [
                Issue(
                    relative,
                    line_number,
                    "LINK_ANCHOR_MISSING",
                    f"heading fragment does not exist: {destination}",
                )
            ]
    return []


def _reference_key(value: str) -> str:
    return " ".join(value.casefold().split())


def check_internal_links(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for source in iter_markdown_files(root):
        relative = _relative(source, root)
        content = _try_read_text(source)
        if content is None:
            continue
        lines = content.splitlines()
        definitions: dict[str, tuple[int, str]] = {}

        for line_number, line in enumerate(lines, start=1):
            definition = REFERENCE_DEFINITION_RE.match(line)
            if definition:
                key = _reference_key(definition.group(1))
                definitions[key] = (line_number, definition.group(2))
                issues.extend(
                    _check_link_destination(root, source, relative, line_number, definition.group(2))
                )
            for match in MARKDOWN_LINK_RE.finditer(line):
                issues.extend(_check_link_destination(root, source, relative, line_number, match.group(1)))

        for line_number, line in enumerate(lines, start=1):
            for match in REFERENCE_USE_RE.finditer(line):
                label, reference = match.groups()
                key = _reference_key(reference or label)
                if key not in definitions:
                    issues.append(
                        Issue(
                            relative,
                            line_number,
                            "LINK_REFERENCE_MISSING",
                            f"reference definition does not exist: {reference or label}",
                        )
                    )
    return issues


def check_adr_numbering(root: Path, expected_count: int = 23) -> list[Issue]:
    adr_dir = root / "docs/adr"
    files = sorted(adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md")) if adr_dir.is_dir() else []
    numbers: list[int] = []
    paths_by_number: dict[int, list[str]] = defaultdict(list)
    issues: list[Issue] = []
    for path in files:
        number = int(path.name[:4])
        relative = _relative(path, root)
        numbers.append(number)
        paths_by_number[number].append(relative)
        content = _try_read_text(path)
        if content is None:
            issues.append(Issue(relative, 0, "ADR_ENCODING", "ADR is not readable UTF-8 text"))
            continue
        if not content.strip():
            issues.append(Issue(relative, 0, "ADR_EMPTY", "ADR has no substantive content"))
            continue
        heading = next((line.strip() for line in content.splitlines() if line.strip()), "")
        heading_pattern = re.compile(rf"^#\s+ADR(?:-|\s)+{number:04d}\b", re.I)
        if not heading_pattern.search(heading):
            issues.append(
                Issue(
                    relative,
                    1,
                    "ADR_HEADING_MISMATCH",
                    f"first heading must identify ADR {number:04d}",
                )
            )
    for number, paths in sorted(paths_by_number.items()):
        if len(paths) > 1:
            issues.append(
                Issue(paths[1], 0, "ADR_DUPLICATE", f"ADR-{number:04d} is defined by {', '.join(paths)}")
            )
    expected = set(range(1, expected_count + 1))
    observed = set(numbers)
    if observed != expected:
        missing = ", ".join(f"{number:04d}" for number in sorted(expected - observed)) or "none"
        extra = ", ".join(f"{number:04d}" for number in sorted(observed - expected)) or "none"
        issues.append(
            Issue("docs/adr", 0, "ADR_SEQUENCE", f"expected 0001–{expected_count:04d}; missing {missing}; extra {extra}")
        )
    return issues


def _definition_ids(
    path: Path,
    pattern: re.Pattern[str],
    *,
    style: str = "both",
) -> Iterable[tuple[str, int]]:
    content = _try_read_text(path)
    if content is None:
        return
    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        candidate = ""
        if style in {"both", "heading"} and stripped.startswith("#"):
            candidate = stripped.lstrip("#").strip()
        elif style in {"both", "table"} and stripped.startswith("|"):
            candidate = stripped[1:].split("|", 1)[0].strip()
        elif style == "both" and stripped.startswith(("- **", "* **")):
            candidate = stripped[1:].strip().lstrip("*").strip()
        if not candidate:
            continue
        candidate = candidate.strip("`*_ ")
        match = pattern.match(candidate)
        if match:
            yield match.group(0), line_number


def _requirement_definition_locations(root: Path) -> Iterable[tuple[str, str, int]]:
    sources: tuple[tuple[str, re.Pattern[str], str], ...] = (
        ("docs/product/brd.md", re.compile(r"\bBO-\d{2,3}\b"), "table"),
        ("docs/product/prd.md", re.compile(r"\bPF-\d{3}\b"), "table"),
        ("docs/product/backlog.md", re.compile(r"\bUS-\d{3}\b"), "table"),
        ("docs/requirements/functional-requirements.md", SRS_ID_RE, "heading"),
        ("docs/requirements/non-functional-requirements.md", SRS_ID_RE, "heading"),
    )
    for relative, pattern, style in sources:
        path = root / relative
        if not path.is_file():
            continue
        for identifier, line_number in _definition_ids(path, pattern, style=style):
            yield identifier, relative, line_number


def _test_definition_locations(root: Path) -> Iterable[tuple[str, str, int]]:
    testing_dir = root / "docs/testing"
    if testing_dir.is_dir():
        for path in sorted(testing_dir.glob("*.md")):
            relative = _relative(path, root)
            for identifier, line_number in _definition_ids(path, TEST_ID_RE):
                yield identifier, relative, line_number

    acceptance = root / "docs/requirements/acceptance-criteria.md"
    if acceptance.is_file():
        for identifier, line_number in _definition_ids(acceptance, VT_SRS_ID_RE, style="table"):
            yield identifier, _relative(acceptance, root), line_number


def check_unique_id_definitions(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    requirement_definitions: dict[str, list[tuple[str, int]]] = defaultdict(list)
    test_definitions: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for identifier, relative, line_number in _requirement_definition_locations(root):
        requirement_definitions[identifier].append((relative, line_number))

    for identifier, relative, line_number in _test_definition_locations(root):
        test_definitions[identifier].append((relative, line_number))

    for identifier, locations in sorted(requirement_definitions.items()):
        if len(locations) > 1:
            path, line_number = locations[1]
            rendered = ", ".join(f"{item_path}:{item_line}" for item_path, item_line in locations)
            issues.append(
                Issue(path, line_number, "REQUIREMENT_ID_DUPLICATE", f"{identifier} defined more than once: {rendered}")
            )
    for identifier, locations in sorted(test_definitions.items()):
        if len(locations) > 1:
            path, line_number = locations[1]
            rendered = ", ".join(f"{item_path}:{item_line}" for item_path, item_line in locations)
            issues.append(
                Issue(path, line_number, "TEST_ID_DUPLICATE", f"{identifier} defined more than once: {rendered}")
            )
    return issues


def check_traceability(root: Path) -> list[Issue]:
    relative = "docs/requirements/traceability-matrix.md"
    path = root / relative
    if not path.is_file():
        return [Issue(relative, 0, "TRACEABILITY_MISSING", "traceability matrix does not exist")]

    content = _try_read_text(path)
    if content is None:
        return [Issue(relative, 0, "TRACEABILITY_ENCODING", "traceability matrix is not readable UTF-8 text")]

    scenario_rows: dict[str, tuple[int, list[str]]] = {}
    issues: list[Issue] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        match = re.match(r"^`?(AC-\d{3})`?(?:\s+.*)?$", cells[0]) if cells else None
        if not match:
            continue
        scenario_id = match.group(1)
        if scenario_id in scenario_rows:
            issues.append(
                Issue(relative, line_number, "TRACEABILITY_DUPLICATE", f"{scenario_id} appears in more than one row")
            )
        scenario_rows[scenario_id] = (line_number, cells)
        if len(cells) != 7:
            issues.append(
                Issue(
                    relative,
                    line_number,
                    "TRACEABILITY_COLUMNS",
                    f"{scenario_id} must have exactly seven traceability columns",
                )
            )

    expected = {f"AC-{number:03d}" for number in range(1, 16)}
    observed = set(scenario_rows)
    if observed != expected:
        missing = ", ".join(sorted(expected - observed)) or "none"
        extra = ", ".join(sorted(observed - expected)) or "none"
        issues.append(
            Issue(relative, 0, "TRACEABILITY_COUNT", f"expected AC-001 through AC-015; missing {missing}; extra {extra}")
        )

    completeness_patterns = (
        (1, "BRD", re.compile(r"\b(?:BO-\d{2,3}|BRD-(?:OBJ|REQ)-\d{3})\b")),
        (2, "PRD", re.compile(r"\b(?:PF-\d{3}|US-\d{3}|PRD-(?:FEAT|STORY|US)-\d{3})\b")),
        (3, "SRS", SRS_ID_RE),
        (4, "component", re.compile(r"\bCMP-[A-Z0-9-]+\b")),
        (5, "test", TEST_ID_RE),
        (6, "release gate", re.compile(r"\bGate\s+[2-9]\b", re.I)),
    )
    for scenario_id, (line_number, cells) in sorted(scenario_rows.items()):
        missing_fields = [
            label
            for index, label, pattern in completeness_patterns
            if index >= len(cells) or not pattern.search(cells[index])
        ]
        if missing_fields:
            issues.append(
                Issue(
                    relative,
                    line_number,
                    "TRACEABILITY_INCOMPLETE",
                    f"{scenario_id} lacks {', '.join(missing_fields)} reference",
                )
            )
    return issues


def check_traceability_reference_integrity(root: Path) -> list[Issue]:
    matrix = root / "docs/requirements/traceability-matrix.md"
    if not matrix.is_file():
        return []
    matrix_text = _try_read_text(matrix)
    if matrix_text is None:
        return [
            Issue(
                "docs/requirements/traceability-matrix.md",
                0,
                "TRACEABILITY_ENCODING",
                "traceability matrix is not readable UTF-8 text",
            )
        ]
    requirement_refs = set(SRS_ID_RE.findall(matrix_text))
    test_refs = set(TEST_ID_RE.findall(matrix_text))

    requirement_definitions = {
        identifier
        for identifier, _, _ in _requirement_definition_locations(root)
        if identifier.startswith("SRS-")
    }
    test_definitions = {
        identifier
        for identifier, _, _ in _test_definition_locations(root)
        if TEST_ID_RE.fullmatch(identifier)
    }

    issues: list[Issue] = []
    for identifier in sorted(requirement_refs - requirement_definitions):
        issues.append(
            Issue(
                "docs/requirements/traceability-matrix.md",
                0,
                "TRACEABILITY_REQUIREMENT_UNDEFINED",
                f"{identifier} has no requirement definition",
            )
        )
    for identifier in sorted(test_refs - test_definitions):
        issues.append(
            Issue(
                "docs/requirements/traceability-matrix.md",
                0,
                "TRACEABILITY_TEST_UNDEFINED",
                f"{identifier} has no test definition",
            )
        )
    return issues


def check_content_safety(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_text_files(root):
        relative = _relative(path, root)
        content = _try_read_text(path)
        if content is None:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            if PLACEHOLDER_RE.search(line):
                issues.append(
                    Issue(relative, line_number, "PLACEHOLDER", "unresolved placeholder marker is not allowed")
                )
            if any(pattern.search(line) for pattern in PERSONAL_PATH_PATTERNS):
                issues.append(
                    Issue(relative, line_number, "PERSONAL_PATH", "absolute personal path is not allowed")
                )
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        Issue(relative, line_number, "SECRET_PATTERN", f"possible {label} must be removed or redacted")
                    )
    return issues


def validate_repository(
    root: Path,
    *,
    required_files: Sequence[str] = REQUIRED_FILES,
    require_full_adr_set: bool = True,
    require_traceability: bool = True,
) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    issues.extend(check_required_files(root, required_files))
    issues.extend(check_text_readability(root))
    issues.extend(check_internal_links(root))
    if require_full_adr_set:
        issues.extend(check_adr_numbering(root))
    issues.extend(check_unique_id_definitions(root))
    if require_traceability:
        issues.extend(check_traceability(root))
        issues.extend(check_traceability_reference_integrity(root))
    issues.extend(check_content_safety(root))
    return sorted(set(issues))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    issues = validate_repository(args.root)
    if issues:
        print(f"Documentation validation failed with {len(issues)} issue(s):")
        for issue in issues:
            print(f"- {issue.render()}")
        return 1
    print(
        "Documentation validation passed: required files, links, ADR sequence, "
        "IDs, traceability, placeholders, personal paths, and secret patterns are clean."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
