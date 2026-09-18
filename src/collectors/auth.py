"""Coletor de falhas de autenticação a partir de logs locais."""

from __future__ import annotations

import re
from pathlib import Path

from src.models import AuthFailure

AUTH_PATTERNS = [
    re.compile(
        r"^(?P<ts>\w+\s+\d+\s+\d+:\d+:\d+).*(?:Failed password|authentication failure)",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2}T[\d:.+-]+).*(?:Failed password|authentication failure)",
        re.IGNORECASE,
    ),
]

# Extraidos separadamente do restante da linha: um .* voraz antes de um grupo
# opcional nunca "sobra" caracteres para o grupo opcional casar, entao usuario
# e origem sao buscados com regexes proprias em vez de ficarem dentro do padrao acima.
USER_PATTERN = re.compile(r"for(?: invalid user)? (?P<user>\S+)", re.IGNORECASE)
SOURCE_PATTERN = re.compile(r"from (?P<source>\S+)", re.IGNORECASE)


def collect_auth_failures(log_path: str, limit: int = 50) -> list[AuthFailure]:
    path = Path(log_path)
    if not path.is_file():
        return []

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    failures: list[AuthFailure] = []
    for line in lines[-5000:]:
        for pattern in AUTH_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            user_match = USER_PATTERN.search(line)
            source_match = SOURCE_PATTERN.search(line)
            failures.append(
                AuthFailure(
                    timestamp=match.group("ts") or "",
                    source=source_match.group("source") if source_match else "unknown",
                    username=user_match.group("user") if user_match else "unknown",
                    message=line.strip()[:300],
                )
            )
            break
    return failures[-limit:]
