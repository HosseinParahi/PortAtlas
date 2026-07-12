#!/usr/bin/env python3
"""Run a disposable PyInstaller feasibility smoke without publishing an artifact."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_VERSION = "3.13.14"
NAME = "portatlas-foundation-spike"


def run(
    command: tuple[str, ...], *, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    return subprocess.run(  # noqa: S603
        command,
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def tree_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    environment = os.environ.copy()
    environment.update({"NO_COLOR": "1", "PYTHONHASHSEED": "0", "SOURCE_DATE_EPOCH": "0"})
    with tempfile.TemporaryDirectory(prefix="portatlas-package-spike-") as temporary:
        temp = Path(temporary)
        command = (
            "uv",
            "run",
            "--locked",
            "--group",
            "packaging",
            "--python",
            PYTHON_VERSION,
            "pyinstaller",
            "--clean",
            "--noconfirm",
            "--onedir",
            "--name",
            NAME,
            "--paths",
            str(ROOT / "services/core/src"),
            "--copy-metadata",
            "portatlas-foundation",
            "--distpath",
            str(temp / "dist"),
            "--workpath",
            str(temp / "build"),
            "--specpath",
            str(temp / "spec"),
            str(ROOT / "services/core/src/portatlas/__main__.py"),
        )
        build = run(command, env=environment)
        bundle = temp / "dist" / NAME
        executable = bundle / NAME
        if not executable.is_file():
            raise SystemExit("PyInstaller did not produce the expected private executable")
        version = run((str(executable), "version"), env=environment).stdout.strip()
        help_output = run((str(executable), "--help"), env=environment).stdout
        if "PortAtlas" not in help_output or "0.0.0.dev0" not in version:
            raise SystemExit("private bundle did not expose the expected CLI contract")
        evidence = {
            "artifact_published": False,
            "bundle_bytes": tree_size(bundle),
            "bundle_sha256": tree_digest(bundle),
            "codesign_available": shutil.which("codesign") is not None,
            "notarytool_probe_performed": False,
            "python": PYTHON_VERSION,
            "pyinstaller": "6.21.0",
            "service_lifecycle_implemented": False,
            "signing_performed": False,
            "version_output": version,
        }
        print(json.dumps(evidence, indent=2, sort_keys=True))
        if build.stderr:
            print(build.stderr.rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
