"""Coletor de interfaces e portas em escuta (somente host local)."""

from __future__ import annotations

import psutil

from src.models import ListeningPort, NetworkInterface


def collect_interfaces() -> list[NetworkInterface]:
    stats = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()
    interfaces: list[NetworkInterface] = []
    for name, addrs in addresses.items():
        ip_list = [
            addr.address
            for addr in addrs
            if addr.family.name in {"AF_INET", "AF_INET6"}
        ]
        nic = stats.get(name)
        interfaces.append(
            NetworkInterface(
                name=name,
                addresses=ip_list,
                is_up=bool(nic.isup) if nic else False,
                speed_mbps=int(nic.speed) if nic and nic.speed else None,
            )
        )
    return interfaces


def collect_listening_ports() -> list[ListeningPort]:
    ports: list[ListeningPort] = []
    try:
        connections = psutil.net_connections(kind="inet")
    except (psutil.AccessDenied, PermissionError):
        return []

    seen: set[tuple[str, str, int]] = set()
    for conn in connections:
        if conn.status != psutil.CONN_LISTEN or not conn.laddr:
            continue
        protocol = "tcp" if conn.type == 1 else "udp"
        address = conn.laddr.ip
        port = conn.laddr.port
        key = (protocol, address, port)
        if key in seen:
            continue
        seen.add(key)
        process_name = None
        if conn.pid:
            try:
                process_name = psutil.Process(conn.pid).name()
            except (psutil.Error, ProcessLookupError):
                process_name = None
        ports.append(
            ListeningPort(
                protocol=protocol,
                address=address,
                port=port,
                pid=conn.pid,
                process_name=process_name,
            )
        )
    return sorted(ports, key=lambda item: (item.protocol, item.port, item.address))
