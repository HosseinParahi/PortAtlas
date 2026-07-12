#!/usr/bin/env python3
"""Start the foundation API on loopback, verify liveness, and stop it cleanly."""

from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

REQUEST_ID_RE = re.compile(r"^req_[0-9a-f-]{36}$")


def available_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def stop(process: subprocess.Popen[str]) -> None:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    port = available_loopback_port()
    command = (
        sys.executable,
        "-m",
        "uvicorn",
        "portatlas.api.app:create_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--log-level",
        "warning",
        "--no-access-log",
    )
    process = subprocess.Popen(  # noqa: S603
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    url = f"http://127.0.0.1:{port}/api/v1/health"
    try:
        for _attempt in range(50):
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(
                    f"service exited before liveness: {stdout[-500:]} {stderr[-500:]}",
                    file=sys.stderr,
                )
                return 1
            try:
                with urllib.request.urlopen(url, timeout=0.5) as response:  # noqa: S310
                    body = json.loads(response.read(4096))
                    request_id = response.headers.get("X-Request-ID", "")
            except (ConnectionError, TimeoutError, urllib.error.URLError):
                time.sleep(0.1)
            else:
                if body != {
                    "schema_version": 1,
                    "service": "portatlas-core",
                    "status": "ok",
                    "version": "0.0.0.dev0",
                }:
                    print("liveness response drifted from the foundation contract", file=sys.stderr)
                    return 1
                if REQUEST_ID_RE.fullmatch(request_id) is None:
                    print("liveness response did not include a safe request ID", file=sys.stderr)
                    return 1
                print(f"Loopback liveness passed on an ephemeral port with {request_id}.")
                return 0
        print("loopback service did not become ready within five seconds", file=sys.stderr)
        return 1
    finally:
        stop(process)


if __name__ == "__main__":
    raise SystemExit(main())
