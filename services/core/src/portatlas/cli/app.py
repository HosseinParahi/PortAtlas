"""Gate 3 CLI composition smoke without deferred product commands."""

from __future__ import annotations

import json

import typer

from portatlas import __version__

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help=(
        "PortAtlas (working title) local port intelligence foundation. "
        "Managed assurance is limited to reservations and atomic leases; "
        "unmanaged observations are evidence, not a guarantee."
    ),
)


@app.callback()
def root() -> None:
    """PortAtlas (working title) local foundation commands."""


@app.command()
def version(
    json_output: bool = typer.Option(False, "--json", help="Emit stable JSON output."),
) -> None:
    """Show the local foundation version."""

    payload = {
        "name": "PortAtlas",
        "status": "working-title",
        "version": __version__,
    }
    if json_output:
        typer.echo(json.dumps(payload, separators=(",", ":"), sort_keys=False))
    else:
        typer.echo(f"PortAtlas (working title) {__version__}")


def main() -> None:
    """Installed console-script entrypoint."""

    app()
