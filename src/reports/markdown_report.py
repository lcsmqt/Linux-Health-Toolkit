"""Relatorio Markdown do snapshot de saude."""

from __future__ import annotations

from pathlib import Path

from src.models import HealthSnapshot


def render_markdown(snapshot: HealthSnapshot) -> str:
    warnings = "\n".join(f"- {item}" for item in snapshot.warnings) or "- nenhum"
    return (
        f"# Relatorio de saude\n\n"
        f"Host: {snapshot.hostname}\n\n"
        f"## Avisos\n\n"
        f"{warnings}\n"
    )


def write_markdown(snapshot: HealthSnapshot, output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(snapshot), encoding="utf-8")
