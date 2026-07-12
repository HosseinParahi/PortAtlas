#!/usr/bin/env python3
"""Require a Developer Certificate of Origin trailer on new commits."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

DCO_RE = re.compile(r"^Signed-off-by: (?P<name>[^<>\r\n]*\S) <(?P<email>[^<>\s@]+@[^<>\s@]+)>$")
TRAILER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*: \S.*$")
EXPECTED_ARGUMENTS = 1
RANGE_ARGUMENTS = 2
ROOT = Path(__file__).resolve().parents[1]


def has_dco_trailer(
    message: str,
    *,
    expected_name: str | None = None,
    expected_email: str | None = None,
) -> bool:
    """Return whether the final trailer block contains a valid DCO sign-off."""
    lines = message.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and (not lines[-1].strip() or lines[-1].lstrip().startswith("#")):
        lines.pop()
    if not lines:
        return False

    separator = len(lines) - 1
    while separator >= 0 and lines[separator].strip():
        separator -= 1
    if separator < 0:
        return False

    trailer_lines = lines[separator + 1 :]
    if not trailer_lines or any(TRAILER_RE.fullmatch(line) is None for line in trailer_lines):
        return False
    matches = [match for line in trailer_lines if (match := DCO_RE.fullmatch(line))]
    if expected_name is None and expected_email is None:
        return bool(matches)
    if expected_name is None or expected_email is None:
        raise ValueError("Both expected DCO identity fields are required.")
    return any(
        match.group("name") == expected_name and match.group("email") == expected_email
        for match in matches
    )


def check_commit_range(revision_range: str) -> list[str]:
    """Return committed-history DCO failures for one Git revision range."""
    git = shutil.which("git")
    if git is None:
        return ["Git is required for committed-history DCO validation."]
    try:
        revisions = subprocess.run(  # noqa: S603
            (git, "rev-list", "--reverse", revision_range),
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except subprocess.CalledProcessError as error:
        details = error.stderr.strip() or "Git could not resolve the revision range."
        return [details]

    failures: list[str] = []
    for revision in revisions:
        result = subprocess.run(  # noqa: S603
            (git, "show", "-s", "--format=%an%x00%ae%x00%B", revision),
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        author_name, author_email, message = result.stdout.split("\x00", 2)
        if not has_dco_trailer(
            message,
            expected_name=author_name,
            expected_email=author_email,
        ):
            failures.append(
                f"{revision}: requires a Signed-off-by trailer matching "
                f"{author_name} <{author_email}>"
            )
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) == RANGE_ARGUMENTS and arguments[0] == "--range":
        failures = check_commit_range(arguments[1])
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1 if failures else 0
    if len(arguments) != EXPECTED_ARGUMENTS:
        print("usage: check_dco.py COMMIT_MESSAGE | --range REVISION_RANGE", file=sys.stderr)
        return 2
    try:
        message = Path(arguments[0]).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"cannot read commit message: {error}", file=sys.stderr)
        return 2
    if has_dco_trailer(message):
        return 0
    print("commit message requires a Signed-off-by trailer", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
