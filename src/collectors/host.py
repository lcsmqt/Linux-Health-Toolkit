"""Informações do host."""

from __future__ import annotations

import platform
import socket
import time

import psutil


def collect_hostname(override: str | None = None) -> str:
    if override:
        return override
    return socket.gethostname()


def collect_platform() -> str:
    return f"{platform.system()} {platform.release()} ({platform.machine()})"


def collect_uptime_seconds() -> float:
    boot = psutil.boot_time()
    return max(time.time() - boot, 0.0)
