from src.aggregator import build_snapshot
from src.config import AppConfig, Thresholds


def test_build_snapshot_runs_locally():
    config = AppConfig(
        thresholds=Thresholds(cpu_percent=100, memory_percent=100, disk_percent=100),
        collect_services=False,
        collect_auth=False,
        collect_network=True,
    )
    snapshot = build_snapshot(config)
    assert snapshot.hostname
    assert snapshot.cpu.count_logical >= 1
    assert snapshot.memory.total > 0
    assert isinstance(snapshot.disks, list)
