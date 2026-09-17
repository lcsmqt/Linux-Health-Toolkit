from src.collectors.auth import collect_auth_failures


def test_collect_auth_failures_from_sample(tmp_path):
    log = tmp_path / "auth.log"
    log.write_text(
        "\n".join(
            [
                "Jan 10 08:11:01 host sshd[10]: Failed password for root from 10.0.0.8 port 22 ssh2",
                "Jan 10 08:11:05 host sshd[11]: Accepted password for lucas from 10.0.0.9",
                "2026-01-10T08:12:00+00:00 host sshd: authentication failure for invalid user admin from 192.168.1.20",
            ]
        ),
        encoding="utf-8",
    )
    failures = collect_auth_failures(str(log))
    assert len(failures) == 2
    assert failures[0].username == "root"
    assert failures[0].source == "10.0.0.8"


def test_missing_log_returns_empty(tmp_path):
    assert collect_auth_failures(str(tmp_path / "nope.log")) == []
