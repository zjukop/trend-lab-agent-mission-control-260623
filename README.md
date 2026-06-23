# Agent Mission Control

A tiny local-first starter for supervising AI coding agent missions and saving replayable traces.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
agent-mission-control demo
```

Then open `mission_trace.html` in your browser.

## Commands

```bash
agent-mission-control demo      # create a sample mission trace
agent-mission-control run TASK  # run a minimal local mission
pytest                          # smoke tests
```

## What is included

- Small plugin-like agent interface
- Permission flags for shell/network/filesystem/browser
- JSON trace recorder
- HTML replay export
