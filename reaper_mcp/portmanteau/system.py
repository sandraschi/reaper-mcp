"""
reaper_system - Consolidated system management portmanteau tool.

OPERATIONS:
- status: Get server and connection status
- help: Get help for tools and categories
- capabilities: List all available tools
"""

import logging
from typing import Any

from ..osc_client import get_reaper_client, ensure_connected

logger = logging.getLogger(__name__)


def setup_system_portmanteau(mcp):
    """Register the reaper_system portmanteau tool."""

    @mcp.tool()
    async def reaper_system(
        operation: str,
        category: str | None = None,
        tool_name: str | None = None,
    ) -> dict[str, Any]:
        """Consolidated system management for Reaper MCP.

        OPERATIONS:
        - status: Get server and Reaper connection status
        - help: Get help (optional: category or tool_name)
        - capabilities: List all available tools

        Args:
            operation: Operation to perform (status, help, capabilities)
            category: For help - filter by category (transport, tracks, project, system)
            tool_name: For help - get specific tool help

        Returns:
            System information and help content

        Examples:
            reaper_system("status")                    # Connection status
            reaper_system("help")                      # Overview help
            reaper_system("help", category="transport") # Transport help
            reaper_system("capabilities")              # List all tools
        """
        valid_ops = ["status", "help", "capabilities"]
        if operation not in valid_ops:
            return {
                "success": False,
                "error": f"Invalid operation: {operation}",
                "valid_operations": valid_ops,
            }

        if operation == "status":
            try:
                if await ensure_connected():
                    client = await get_reaper_client()
                    return {
                        "operation": "status",
                        "server": {
                            "name": "reaper-mcp",
                            "version": "2.0.0",
                            "fastmcp_version": "2.13.1",
                            "status": "running",
                        },
                        "reaper_connection": {
                            "host": client.host,
                            "port": client.port,
                            "connected": client.connected,
                            "last_status": client.last_status,
                        },
                        "tools_available": 4,
                        "success": True,
                        "message": "🎵 Reaper MCP operational",
                    }
                else:
                    return {
                        "operation": "status",
                        "server": {"name": "reaper-mcp", "version": "2.0.0", "status": "running"},
                        "reaper_connection": {"connected": False},
                        "success": True,
                        "message": "Server running, Reaper not connected",
                    }
            except Exception as e:
                return {"operation": "status", "success": False, "error": str(e)}

        elif operation == "help":
            help_data = {
                "operation": "help",
                "server": "Reaper MCP - FastMCP 2.13.1",
                "description": "Austrian precision DAW automation via OSC",
            }

            tool_help = {
                "reaper_transport": "Transport control: play, stop, pause, record, position, status",
                "reaper_tracks": "Track management: list, info, mute, solo, arm, count, bulk",
                "reaper_project": "Project ops: info, save, marker, render, stats",
                "reaper_system": "System: status, help, capabilities",
            }

            category_help = {
                "transport": {
                    "tool": "reaper_transport",
                    "operations": ["play", "stop", "pause", "record", "position", "status"],
                },
                "tracks": {
                    "tool": "reaper_tracks",
                    "operations": ["list", "info", "mute", "solo", "arm", "count", "bulk"],
                },
                "project": {
                    "tool": "reaper_project",
                    "operations": ["info", "save", "marker", "render", "stats"],
                },
                "system": {
                    "tool": "reaper_system",
                    "operations": ["status", "help", "capabilities"],
                },
            }

            if tool_name:
                if tool_name in tool_help:
                    help_data["tool_help"] = {"name": tool_name, "description": tool_help[tool_name]}
                else:
                    help_data["error"] = f"Tool '{tool_name}' not found"
            elif category:
                if category in category_help:
                    help_data["category_help"] = category_help[category]
                else:
                    help_data["error"] = f"Category '{category}' not found"
            else:
                help_data["tools"] = tool_help
                help_data["categories"] = list(category_help.keys())

            help_data["success"] = True
            return help_data

        elif operation == "capabilities":
            return {
                "operation": "capabilities",
                "total_tools": 4,
                "tools": {
                    "reaper_transport": ["play", "stop", "pause", "record", "position", "status"],
                    "reaper_tracks": ["list", "info", "mute", "solo", "arm", "count", "bulk"],
                    "reaper_project": ["info", "save", "marker", "render", "stats"],
                    "reaper_system": ["status", "help", "capabilities"],
                },
                "protocol": "OSC",
                "fastmcp_version": "2.13.1",
                "success": True,
            }

