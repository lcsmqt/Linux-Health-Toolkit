from src.models import (
    CpuMetrics,
    DiskPartition,
    HealthSnapshot,
    MemoryMetrics,
)
from src.reports.json_report import render_json
from src.reports.markdown_report import render_markdown


def _snapshot() -> HealthSnapshot:
    return HealthSnapshot(
        hostname="lab-01",
        platform="Linux 6.8",
        uptime_seconds=3600,
        collected_at="2026-01-01T00:00:00+00:00",
        cpu=CpuMetrics(percent=10.0, count_logical=4, count_physical=2, load_avg=(0.1, 0.2, 0.3)),
        memory=MemoryMetrics(
            total=8 * 1024**3,
            available=4 * 1024**3,
            used=4 * 1024**3,
            percent=50.0,
            swap_total=0,
            swap_used=0,
            swap_percent=0.0,
        ),
        disks=[
            DiskPartition(
                device="/dev/sda1",
                mountpoint="/",
                fstype="ext4",
                total=100,
                used=40,
                free=60,
                percent=40.0,
            )
        ],
        warnings=["CPU acima do limiar (90.0%)"],
    )


def test_markdown_contains_hostname():
    text = render_markdown(_snapshot())
    assert "lab-01" in text
    assert "CPU acima do limiar" in text


def test_json_is_valid():
    raw = render_json(_snapshot())
    assert '"hostname": "lab-01"' in raw
