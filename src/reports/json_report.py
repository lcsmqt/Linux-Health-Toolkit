"""Relatorio JSON do snapshot de saude."""

from __future__ import annotations

import json
from pathlib import Path

from src.models import HealthSnapshot


def render_json(snapshot: HealthSnapshot) -> str:
    return json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False)


def write_json(snapshot: HealthSnapshot, output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(snapshot), encoding="utf-8")
