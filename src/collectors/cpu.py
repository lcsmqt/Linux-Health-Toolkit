"""Coletor de CPU."""

from __future__ import annotations

import os

import psutil

from src.models import CpuMetrics


def collect_cpu() -> CpuMetrics:
    load_avg = None
    if hasattr(os, "getloadavg"):
        try:
            load_avg = os.getloadavg()
        except OSError:
            load_avg = None

    return CpuMetrics(
        percent=psutil.cpu_percent(interval=0.1),
        count_logical=psutil.cpu_count(logical=True) or 1,
        count_physical=psutil.cpu_count(logical=False),
        load_avg=load_avg,
    )
