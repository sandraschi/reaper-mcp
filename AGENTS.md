# reaper-mcp Agent Context

Quick reference for reaper-mcp — Reaper DAW automation via FastMCP and OSC.

## Quick Ref
```powershell
# Start
uv run python -m reaper_mcp.server
# Tests
uv run pytest tests/ -q
# Lint
uv run ruff check reaper_mcp/ tests/
```

## Ports
| Service | Port |
|---|---|
| Backend | 10797 |
| Frontend | 10796 |

## Architecture
FastMCP server for Reaper DAW automation via OSC and reapy-boost. Provides project management, track/transport control, and crosslink orchestration tools.
