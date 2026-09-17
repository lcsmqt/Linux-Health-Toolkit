"""Interface de linha de comando."""

from __future__ import annotations

import argparse
import json
import sys

from src.aggregator import build_snapshot
from src.config import load_config
from src.logging_setup import setup_logging
from src.reports.html_report import render_html, write_html
from src.reports.json_report import render_json, write_json
from src.reports.markdown_report import render_markdown, write_markdown


def _write(snapshot, fmt: str, output: str | None) -> None:
    if output:
        if fmt == "json":
            write_json(snapshot, output)
        elif fmt == "html":
            write_html(snapshot, output)
        else:
            write_markdown(snapshot, output)
        print(f"Relatório gravado em {output}")
        return

    if fmt == "json":
        print(render_json(snapshot))
    elif fmt == "html":
        print(render_html(snapshot))
    else:
        print(render_markdown(snapshot))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Toolkit de saúde de sistemas Linux / Windows (métricas locais)."
    )
    parser.add_argument("--config", help="Caminho do YAML de configuração")
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="Gera relatório completo")
    report.add_argument("--format", choices=["markdown", "json", "html"], default="markdown")
    report.add_argument("--output", help="Arquivo de saída")

    snapshot_cmd = sub.add_parser("snapshot", help="Exibe seções específicas")
    snapshot_cmd.add_argument(
        "--section",
        default="cpu,memory,disk",
        help="Seções separadas por vírgula: cpu,memory,disk,network,auth,services",
    )

    args = parser.parse_args(argv)
    config = load_config(args.config)
    setup_logging(config.log_level)
    snapshot = build_snapshot(config)

    if args.command == "report":
        _write(snapshot, args.format, args.output)
        return 0

    data = snapshot.to_dict()
    wanted = {item.strip() for item in args.section.split(",") if item.strip()}
    mapping = {
        "cpu": data["cpu"],
        "memory": data["memory"],
        "disk": data["disks"],
        "network": {"interfaces": data["interfaces"], "ports": data["listening_ports"]},
        "auth": data["auth_failures"],
        "services": {"all": data["services"], "failed": data["failed_services"]},
    }
    payload = {key: mapping[key] for key in wanted if key in mapping}
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
