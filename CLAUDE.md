# reaper-mcp — Agent Instructions

FastMCP 3.4 Reaper DAW automation server via OSC and reapy-boost.

## Quick Start
powershell
uv run python -m reaper_mcp.server          # stdio mode (HTTP on :10797)
uv run python -m reaper_mcp                 # via __main__.py

## Key Files
- reaper_mcp/mcp_app.py — FastMCP server instance and core tools
- reaper_mcp/api/main.py — FastAPI REST wrapper (port 10797)
- reaper_mcp/portmanteau/ — 6 portmanteau tools (transport, tracks, project, etc.)
- reaper_mcp/osc_client.py — OSC communication layer
- web_sota/ — React frontend (Vite, :10796)
- native/ — Tauri 2.0 NSIS desktop wrapper

## Commands
powershell
just lint          # ruff + biome
just test          # pytest
just fmt           # ruff format
just types         # tsc --noEmit
just gates-green   # all gates

## Standards
- Ports: BE :10797, FE :10796 (WEBAPP_PORTS.md)
- Tools use portmanteau pattern via operation: Literal[...]
- Use Annotated[T, Field(description="...")] for params (no Args: blocks)
- Return {"success": bool, "message": str, "data": ...}
