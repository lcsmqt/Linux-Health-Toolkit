"""Coletor de disco."""

from __future__ import annotations

import psutil

from src.models import DiskPartition

SKIP_FSTYPES = {"squashfs", "overlay", "tmpfs", "devtmpfs", "proc", "sysfs", "cgroup2"}


def collect_disks() -> list[DiskPartition]:
    partitions: list[DiskPartition] = []
    for part in psutil.disk_partitions(all=False):
        if part.fstype.lower() in SKIP_FSTYPES:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, FileNotFoundError, OSError):
            continue
        partitions.append(
            DiskPartition(
                device=part.device,
                mountpoint=part.mountpoint,
                fstype=part.fstype,
                total=usage.total,
                used=usage.used,
                free=usage.free,
                percent=usage.percent,
            )
        )
    return partitions
