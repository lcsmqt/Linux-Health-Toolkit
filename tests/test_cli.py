from src.cli import main


def test_cli_snapshot_cpu(capsys):
    code = main(["snapshot", "--section", "cpu"])
    captured = capsys.readouterr()
    assert code == 0
    assert "percent" in captured.out
