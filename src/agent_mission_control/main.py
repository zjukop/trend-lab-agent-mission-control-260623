from __future__ import annotations

import argparse
import html
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Permissions:
    filesystem: bool = False
    network: bool = False
    shell: bool = False
    browser: bool = False


@dataclass
class TraceEvent:
    at: str
    agent: str
    kind: str
    detail: str


@dataclass
class Agent:
    name: str
    role: str
    permissions: Permissions = field(default_factory=Permissions)

    def act(self, task: str) -> TraceEvent:
        allowed = [key for key, value in asdict(self.permissions).items() if value]
        detail = f"{self.role} handled '{task}' with permissions: {allowed or ['none']}"
        return TraceEvent(now(), self.name, "decision", detail)


@dataclass
class Mission:
    title: str
    agents: list[Agent]
    events: list[TraceEvent] = field(default_factory=list)

    def run(self, task: str) -> None:
        self.events.append(TraceEvent(now(), "human", "task", task))
        for agent in self.agents:
            self.events.append(agent.act(task))

    def to_json(self) -> str:
        return json.dumps({"title": self.title, "events": [asdict(e) for e in self.events]}, indent=2)

    def write_replay(self, path: Path) -> Path:
        rows = "\n".join(
            f"<li><b>{html.escape(e.agent)}</b> <code>{html.escape(e.kind)}</code>: "
            f"{html.escape(e.detail)} <small>{html.escape(e.at)}</small></li>"
            for e in self.events
        )
        path.write_text(
            "<!doctype html><meta charset='utf-8'>"
            "<title>Agent Mission Replay</title>"
            "<style>body{font-family:system-ui;max-width:760px;margin:3rem auto;line-height:1.5}"
            "li{margin:.7rem 0}code{background:#eee;padding:.1rem .3rem}</style>"
            f"<h1>{html.escape(self.title)}</h1><ol>{rows}</ol>",
            encoding="utf-8",
        )
        return path


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sample_agents() -> list[Agent]:
    return [
        Agent("researcher", "Finds context", Permissions(network=True, browser=True)),
        Agent("coder", "Plans code changes", Permissions(filesystem=True, shell=True)),
        Agent("reviewer", "Checks risk and quality"),
    ]


def run_mission(task: str, output: Path) -> Mission:
    mission = Mission("Agent Mission Control Demo", sample_agents())
    mission.run(task)
    mission.write_replay(output)
    return mission


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local-first AI agent mission trace demo")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="write a sample HTML replay")
    demo.add_argument("--output", type=Path, default=Path("mission_trace.html"))

    run = sub.add_parser("run", help="run a minimal mission for TASK")
    run.add_argument("task")
    run.add_argument("--output", type=Path, default=Path("mission_trace.html"))
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    task = "Research, implement, and review a tiny GitHub issue" if args.command == "demo" else args.task
    mission = run_mission(task, args.output)
    print(mission.to_json())
    print(f"Replay written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
