"""Coletor de serviços systemd (Linux) com fallback seguro."""

from __future__ import annotations

import shutil
import subprocess

from src.models import ServiceStatus


def _run_systemctl(args: list[str]) -> str:
    result = subprocess.run(
        ["systemctl", *args],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def collect_services() -> tuple[list[ServiceStatus], list[ServiceStatus]]:
    if shutil.which("systemctl") is None:
        return [], []

    output = _run_systemctl(
        ["list-units", "--type=service", "--all", "--no-pager", "--plain"]
    )
    services: list[ServiceStatus] = []
    failed: list[ServiceStatus] = []
    for line in output.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 4 or not parts[0].endswith(".service"):
            continue
        name, _load, active, sub, *rest = parts
        description = rest[0] if rest else ""
        status = ServiceStatus(
            name=name,
            active=active == "active",
            sub_state=sub,
            description=description,
        )
        services.append(status)
        if active == "failed" or sub == "failed":
            failed.append(status)
    return services, failed
