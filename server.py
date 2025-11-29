#!/usr/bin/env python3
"""
Reaper MCP Server - FastMCP 2.13.1
Austrian precision digital audio workstation automation via Reaper DAW

PORTMANTEAU TOOLS (4 total, consolidated from 21):
- reaper_transport: play/stop/pause/record/position/status
- reaper_tracks: list/info/mute/solo/arm/count/bulk
- reaper_project: info/save/marker/render/stats
- reaper_system: status/help/capabilities
"""

import logging
import os
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tool mode: portmanteau (default) or individual
TOOL_MODE = os.environ.get("REAPER_TOOL_MODE", "portmanteau")

# Create FastMCP 2.13.1 server
mcp = FastMCP(
    name="reaper-mcp",
    version="2.0.0",
    instructions="Austrian precision DAW automation via Reaper with OSC control. "
    "Use reaper_transport for playback, reaper_tracks for track management, "
    "reaper_project for project ops, reaper_system for status/help.",
)


def main():
    """Initialize and start the Reaper MCP server."""

    if TOOL_MODE == "portmanteau":
        # Import and register portmanteau tools (4 consolidated tools)
        from reaper_mcp.portmanteau import setup_all_portmanteau_tools

        setup_all_portmanteau_tools(mcp)
        logger.info("🎛️ Registered 4 portmanteau tools (consolidated from 21)")
    else:
        # Legacy: individual tools
        from reaper_mcp.transport import register_transport_tools
        from reaper_mcp.tracks import register_track_tools
        from reaper_mcp.project import register_project_tools

        register_transport_tools(mcp)
        register_track_tools(mcp)
        register_project_tools(mcp)
        logger.info("🎛️ Registered 21 individual tools (legacy mode)")

    # Register resources
    @mcp.resource("reaper://config")
    def reaper_config() -> str:
        """Reaper OSC configuration information."""
        import json

        return json.dumps(
            {
                "osc_setup": {"host": "127.0.0.1", "port": 8000, "protocol": "UDP"},
                "reaper_setup": [
                    "1. Open Reaper preferences (Ctrl+P)",
                    "2. Go to Control/OSC/web",
                    "3. Add new OSC device",
                    "4. Set Local IP: 127.0.0.1, Port: 8000",
                    "5. Enable 'Send all feedback'",
                ],
            }
        )

    logger.info("🎵 Starting Reaper MCP Server v2.0.0")
    logger.info("🇦🇹 Austrian Audio Automation - FastMCP 2.13.1")
    logger.info(f"📦 Tool mode: {TOOL_MODE}")

    # Run with stdio transport for Claude Desktop
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
