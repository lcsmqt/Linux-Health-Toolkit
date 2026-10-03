"""Relatorio HTML do snapshot de saude."""

from __future__ import annotations

from pathlib import Path

from src.models import HealthSnapshot


def render_html(snapshot: HealthSnapshot) -> str:
    warnings = "".join(f"<li>{item}</li>" for item in snapshot.warnings)
    return (
        "<!DOCTYPE html><html><body>"
        f"<h1>{snapshot.hostname}</h1><ul>{warnings}</ul>"
        "</body></html>"
    )


def write_html(snapshot: HealthSnapshot, output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html(snapshot), encoding="utf-8")
