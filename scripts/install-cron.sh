#!/usr/bin/env bash
set -euo pipefail

# Agenda relatório diário às 07:00 no crontab do usuário atual.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${ROOT}/.venv/bin/python"
OUTPUT="${ROOT}/reports/daily-health.md"

if [[ ! -x "${PYTHON}" ]]; then
  PYTHON="$(command -v python3)"
fi

CRON_LINE="0 7 * * * cd ${ROOT} && ${PYTHON} -m src.cli report --format markdown --output ${OUTPUT} >> ${ROOT}/reports/cron.log 2>&1"

(crontab -l 2>/dev/null | grep -v "src.cli report" || true; echo "${CRON_LINE}") | crontab -
echo "Cron instalado: ${CRON_LINE}"
