from src.config import load_config


def test_load_config_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("HEALTH_CONFIG", raising=False)
    monkeypatch.chdir(tmp_path)
    config = load_config("missing.yaml")
    assert config.thresholds.cpu_percent == 85.0
    assert config.collect_network is True


def test_load_config_yaml(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("thresholds:\n  cpu_percent: 70\ncollect_auth: false\n", encoding="utf-8")
    config = load_config(str(path))
    assert config.thresholds.cpu_percent == 70
    assert config.collect_auth is False
