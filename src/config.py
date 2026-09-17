"""Carregamento de configuração via YAML e variáveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG: dict[str, Any] = {
    "thresholds": {
        "cpu_percent": 85.0,
        "memory_percent": 85.0,
        "disk_percent": 90.0,
        "auth_failures_window": 50,
    },
    "auth_log_path": "/var/log/auth.log",
    "collect_services": True,
    "collect_auth": True,
    "collect_network": True,
    "hostname_override": None,
}


@dataclass
class Thresholds:
    cpu_percent: float = 85.0
    memory_percent: float = 85.0
    disk_percent: float = 90.0
    auth_failures_window: int = 50


@dataclass
class AppConfig:
    thresholds: Thresholds = field(default_factory=Thresholds)
    auth_log_path: str = "/var/log/auth.log"
    collect_services: bool = True
    collect_auth: bool = True
    collect_network: bool = True
    hostname_override: str | None = None
    log_level: str = "INFO"
    output_dir: str = "reports/"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | None = None) -> AppConfig:
    config_path = path or os.getenv("HEALTH_CONFIG", "config/config.yaml")
    data = dict(DEFAULT_CONFIG)
    file_path = Path(config_path)
    if file_path.is_file():
        with file_path.open(encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
        data = _deep_merge(data, loaded)

    thresholds = Thresholds(**data.get("thresholds", {}))
    return AppConfig(
        thresholds=thresholds,
        auth_log_path=data.get("auth_log_path", DEFAULT_CONFIG["auth_log_path"]),
        collect_services=bool(data.get("collect_services", True)),
        collect_auth=bool(data.get("collect_auth", True)),
        collect_network=bool(data.get("collect_network", True)),
        hostname_override=data.get("hostname_override"),
        log_level=os.getenv("HEALTH_LOG_LEVEL", "INFO"),
        output_dir=os.getenv("HEALTH_OUTPUT_DIR", "reports/"),
    )
