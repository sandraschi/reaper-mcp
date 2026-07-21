"""
transport.py - Reaper transport control tools for FastMCP 2.1
Austrian precision audio playback automation
"""

import logging
from typing import Any

from .osc_client import ensure_connected, get_reaper_client

logger = logging.getLogger(__name__)


def register_transport_tools(mcp):
    """Register transport control tools with FastMCP server"""

    @mcp.tool()
    async def play_transport() -> dict[str, Any]:
        """Start playback in Reaper

        Returns:
            Dictionary with playback status and position
        """
        if not await ensure_connected():
            return {
                "action": "play",
                "success": False,
                "error": "Not connected to Reaper",
                "suggestion": "Start Reaper and enable OSC control",
            }

        try:
            client = await get_reaper_client()
            result = await client.play_transport()
            return {
                **result,
                "message": "🎵 Playback started",
                "austrian_efficiency": "Sehr gut!",
            }
        except Exception as e:
            logger.error(f"Transport play error: {e}")
            return {"action": "play", "success": False, "error": str(e)}

    @mcp.tool()
    async def stop_transport() -> dict[str, Any]:
        """Stop playback in Reaper

        Returns:
            Dictionary with transport status
        """
        if not await ensure_connected():
            return {
                "action": "stop",
                "success": False,
                "error": "Not connected to Reaper",
            }

        try:
            client = await get_reaper_client()
            result = await client.stop_transport()
            return {**result, "message": "⏹️ Playback stopped", "ready_for_next": True}
        except Exception as e:
            logger.error(f"Transport stop error: {e}")
            return {"action": "stop", "success": False, "error": str(e)}

    @mcp.tool()
    async def pause_transport() -> dict[str, Any]:
        """Pause playback in Reaper

        Returns:
            Dictionary with pause status
        """
        if not await ensure_connected():
            return {
                "action": "pause",
                "success": False,
                "error": "Not connected to Reaper",
            }

        try:
            client = await get_reaper_client()
            result = await client.pause_transport()
            return {**result, "message": "⏸️ Playback paused"}
        except Exception as e:
            logger.error(f"Transport pause error: {e}")
            return {"action": "pause", "success": False, "error": str(e)}

    @mcp.tool()
    async def record_transport() -> dict[str, Any]:
        """Start recording in Reaper

        Returns:
            Dictionary with recording status
        """
        if not await ensure_connected():
            return {
                "action": "record",
                "success": False,
                "error": "Not connected to Reaper",
            }

        try:
            client = await get_reaper_client()
            result = await client.record_transport()
            return {
                **result,
                "message": "🔴 Recording started",
                "warning": "Make sure tracks are armed!",
            }
        except Exception as e:
            logger.error(f"Transport record error: {e}")
            return {"action": "record", "success": False, "error": str(e)}

    @mcp.tool()
    async def get_transport_position() -> dict[str, Any]:
        """Get current transport position

        Returns:
            Dictionary with current position and timing info
        """
        if not await ensure_connected():
            return {
                "position": "0:00:00",
                "connected": False,
                "error": "Not connected to Reaper",
            }

        try:
            client = await get_reaper_client()
            result = await client.get_position()
            return {
                "position": result.get("args", ["0:00:00"])[0] if result.get("args") else "0:00:00",
                "connected": True,
                "last_update": result.get("timestamp", 0),
                "transport_info": result,
            }
        except Exception as e:
            logger.error(f"Get position error: {e}")
            return {"position": "0:00:00", "connected": False, "error": str(e)}

    @mcp.tool()
    async def transport_status() -> dict[str, Any]:
        """Get comprehensive transport status

        Returns:
            Dictionary with complete transport state
        """
        if not await ensure_connected():
            return {
                "connected": False,
                "playing": False,
                "recording": False,
                "position": "0:00:00",
                "error": "Not connected to Reaper",
            }

        try:
            client = await get_reaper_client()
            position_info = await client.get_position()

            return {
                "connected": client.connected,
                "host": client.host,
                "port": client.port,
                "position": position_info.get("args", ["0:00:00"])[0] if position_info.get("args") else "0:00:00",
                "last_status": client.last_status,
                "reaper_responsive": bool(position_info),
                "austrian_status": "Alles in Ordnung! 🇦🇹",
            }
        except Exception as e:
            logger.error(f"Transport status error: {e}")
            return {"connected": False, "error": str(e)}
