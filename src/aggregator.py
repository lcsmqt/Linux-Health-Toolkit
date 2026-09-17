"""Agrega coletores em um snapshot único e aplica limiares."""

from __future__ import annotations

from src.collectors.auth import collect_auth_failures
from src.collectors.cpu import collect_cpu
from src.collectors.disk import collect_disks
from src.collectors.host import collect_hostname, collect_platform, collect_uptime_seconds
from src.collectors.memory import collect_memory
from src.collectors.network import collect_interfaces, collect_listening_ports
from src.collectors.services import collect_services
from src.config import AppConfig
from src.models import HealthSnapshot, utc_now_iso


def build_snapshot(config: AppConfig) -> HealthSnapshot:
    cpu = collect_cpu()
    memory = collect_memory()
    disks = collect_disks()
    services, failed = ([], [])
    auth_failures = []
    interfaces = []
    listening = []
    warnings: list[str] = []

    if config.collect_services:
        services, failed = collect_services()
        if failed:
            warnings.append(f"{len(failed)} serviço(s) em estado failed")

    if config.collect_auth:
        auth_failures = collect_auth_failures(
            config.auth_log_path, config.thresholds.auth_failures_window
        )
        if len(auth_failures) >= 10:
            warnings.append(f"{len(auth_failures)} falhas de autenticação recentes")

    if config.collect_network:
        interfaces = collect_interfaces()
        listening = collect_listening_ports()

    if cpu.percent >= config.thresholds.cpu_percent:
        warnings.append(f"CPU acima do limiar ({cpu.percent:.1f}%)")
    if memory.percent >= config.thresholds.memory_percent:
        warnings.append(f"Memória acima do limiar ({memory.percent:.1f}%)")
    for disk in disks:
        if disk.percent >= config.thresholds.disk_percent:
            warnings.append(
                f"Disco {disk.mountpoint} acima do limiar ({disk.percent:.1f}%)"
            )

    return HealthSnapshot(
        hostname=collect_hostname(config.hostname_override),
        platform=collect_platform(),
        uptime_seconds=collect_uptime_seconds(),
        collected_at=utc_now_iso(),
        cpu=cpu,
        memory=memory,
        disks=disks,
        services=services,
        failed_services=failed,
        auth_failures=auth_failures,
        interfaces=interfaces,
        listening_ports=listening,
        warnings=warnings,
    )
