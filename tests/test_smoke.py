from pathlib import Path

from agent_mission_control.main import main, run_mission


def test_run_mission_writes_replay(tmp_path: Path) -> None:
    output = tmp_path / "replay.html"
    mission = run_mission("fix a smoke test", output)

    assert output.exists()
    assert "fix a smoke test" in output.read_text(encoding="utf-8")
    assert len(mission.events) == 4


def test_cli_demo(tmp_path: Path) -> None:
    output = tmp_path / "demo.html"

    assert main(["demo", "--output", str(output)]) == 0
    assert output.exists()
