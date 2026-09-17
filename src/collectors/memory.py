"""Coletor de memória."""

from __future__ import annotations

import psutil

from src.models import MemoryMetrics


def collect_memory() -> MemoryMetrics:
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return MemoryMetrics(
        total=virtual.total,
        available=virtual.available,
        used=virtual.used,
        percent=virtual.percent,
        swap_total=swap.total,
        swap_used=swap.used,
        swap_percent=swap.percent,
    )
