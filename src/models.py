"""Modelos de dados do snapshot de saúde do sistema."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CpuMetrics:
    percent: float
    count_logical: int
    count_physical: int | None
    load_avg: tuple[float, float, float] | None = None


@dataclass
class MemoryMetrics:
    total: int
    available: int
    used: int
    percent: float
    swap_total: int
    swap_used: int
    swap_percent: float


@dataclass
class DiskPartition:
    device: str
    mountpoint: str
    fstype: str
    total: int
    used: int
    free: int
    percent: float


@dataclass
class ServiceStatus:
    name: str
    active: bool
    sub_state: str
    description: str = ""


@dataclass
class AuthFailure:
    timestamp: str
    source: str
    username: str
    message: str


@dataclass
class NetworkInterface:
    name: str
    addresses: list[str]
    is_up: bool
    speed_mbps: int | None = None


@dataclass
class ListeningPort:
    protocol: str
    address: str
    port: int
    pid: int | None
    process_name: str | None


@dataclass
class HealthSnapshot:
    hostname: str
    platform: str
    uptime_seconds: float
    collected_at: str
    cpu: CpuMetrics
    memory: MemoryMetrics
    disks: list[DiskPartition]
    services: list[ServiceStatus] = field(default_factory=list)
    failed_services: list[ServiceStatus] = field(default_factory=list)
    auth_failures: list[AuthFailure] = field(default_factory=list)
    interfaces: list[NetworkInterface] = field(default_factory=list)
    listening_ports: list[ListeningPort] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
