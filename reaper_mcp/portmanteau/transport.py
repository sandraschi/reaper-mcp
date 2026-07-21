"""
reaper_transport - Consolidated transport control portmanteau tool.

OPERATIONS:
- play: Start playback
- stop: Stop playback
- pause: Pause playback
- record: Start recording
- position: Get current position
- status: Get comprehensive transport status
"""

import logging
from typing import Annotated, Any

from pydantic import Field

from ..osc_client import ensure_connected, get_reaper_client

logger = logging.getLogger(__name__)


def setup_transport_portmanteau(mcp):
    """Register the reaper_transport portmanteau tool."""

    @mcp.tool()
    async def reaper_transport(
        operation: Annotated[str, Field(description="Operation: play, stop, pause, record, position, status")],
    ) -> dict[str, Any]:
        """Consolidated transport control for Reaper DAW.

        [RATIONALE]
        Consolidates 6 transport operations into one portmanteau tool to keep
        the tool registry clean while providing full DAW transport control.

        OPERATIONS:
        - play: Start playback
        - stop: Stop playback
        - pause: Pause playback
        - record: Start recording (ensure tracks are armed!)
        - position: Get current transport position
        - status: Get comprehensive transport state

        ## Return Format
        {"success": bool, "operation": str, "message"?: str, "position"?: str, "connected"?: bool, "error"?: str}

        ## Examples
        reaper_transport(operation="play")
        reaper_transport(operation="position")
        reaper_transport(operation="status")
        """
        valid_ops = ["play", "stop", "pause", "record", "position", "status"]
        if operation not in valid_ops:
            return {
                "success": False,
                "error": f"Invalid operation: {operation}",
                "valid_operations": valid_ops,
            }

        if not await ensure_connected():
            return {
                "operation": operation,
                "success": False,
                "error": "Not connected to Reaper",
                "suggestion": "Start Reaper and enable OSC control",
            }

        try:
            client = await get_reaper_client()

            if operation == "play":
                result = await client.play_transport()
                return {
                    **result,
                    "operation": "play",
                    "message": "🎵 Playback started",
                }

            elif operation == "stop":
                result = await client.stop_transport()
                return {
                    **result,
                    "operation": "stop",
                    "message": "⏹️ Playback stopped",
                }

            elif operation == "pause":
                result = await client.pause_transport()
                return {
                    **result,
                    "operation": "pause",
                    "message": "⏸️ Playback paused",
                }

            elif operation == "record":
                result = await client.record_transport()
                return {
                    **result,
                    "operation": "record",
                    "message": "🔴 Recording started",
                    "warning": "Make sure tracks are armed!",
                }

            elif operation == "position":
                result = await client.get_position()
                position = result.get("args", ["0:00:00"])[0] if result.get("args") else "0:00:00"
                return {
                    "operation": "position",
                    "position": position,
                    "connected": True,
                    "success": True,
                }

            elif operation == "status":
                position_info = await client.get_position()
                position = position_info.get("args", ["0:00:00"])[0] if position_info.get("args") else "0:00:00"
                return {
                    "operation": "status",
                    "connected": client.connected,
                    "host": client.host,
                    "port": client.port,
                    "position": position,
                    "last_status": client.last_status,
                    "success": True,
                }

        except Exception as e:
            logger.error(f"Transport {operation} error: {e}")
            return {
                "operation": operation,
                "success": False,
                "error": str(e),
            }
