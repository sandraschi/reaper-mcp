"""
ASGI entry point for uvicorn (web_sota backend).
CLI entry point for python -m reaper_mcp (runs MCP stdio server).

- Web: uvicorn reaper_mcp.server:app --host 127.0.0.1 --port 10797
- Stdio: python -m reaper_mcp or reaper-mcp (for Claude Desktop)
"""

import uvicorn

from reaper_mcp.api.main import app
from reaper_mcp.mcp_app import mcp

__all__ = ["app", "main"]


def main() -> None:
    """Run the MCP server in stdio mode (Claude Desktop, CLI)."""
    mcp.run()


def run_web() -> None:
    """Run the FastAPI backend (web_sota). Prefer: uv run uvicorn reaper_mcp.server:app ..."""
    uvicorn.run(app, host="127.0.0.1", port=10797, log_level="info")
