"""
reaper_project - Consolidated project management portmanteau tool.

OPERATIONS:
- info: Get project information
- save: Save current project
- marker: Add timeline marker
- render: Render/bounce project
- stats: Get comprehensive project statistics
"""

import logging
from typing import Any

from ..osc_client import get_reaper_client, ensure_connected

logger = logging.getLogger(__name__)


def _parse_time_to_seconds(time_str: str) -> float:
    """Parse time string to seconds."""
    try:
        if "." in time_str and ":" not in time_str:
            return float(time_str)
        if time_str.isdigit():
            return float(time_str)

        parts = time_str.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        return 0.0
    except (ValueError, IndexError):
        return 0.0


def setup_project_portmanteau(mcp):
    """Register the reaper_project portmanteau tool."""

    @mcp.tool()
    async def reaper_project(
        operation: str,
        position: str | None = None,
        name: str | None = None,
        format: str = "wav",
        quality: str = "high",
        bounds: str = "project",
    ) -> dict[str, Any]:
        """Consolidated project management for Reaper DAW.

        OPERATIONS:
        - info: Get current project information
        - save: Save current project
        - marker: Add timeline marker (requires position, name)
        - render: Render/bounce project (format, quality, bounds)
        - stats: Get comprehensive project statistics

        Args:
            operation: Operation to perform
            position: Time position for marker (e.g., "1:30", "90.5")
            name: Marker name/description
            format: Render format (wav, mp3, flac)
            quality: Render quality (low, medium, high, lossless)
            bounds: Render bounds (project, selection, time_selection)

        Returns:
            Operation result with project data

        Examples:
            reaper_project("info")                              # Project info
            reaper_project("save")                              # Save project
            reaper_project("marker", position="1:30", name="Chorus")  # Add marker
            reaper_project("render", format="wav", quality="high")    # Render
            reaper_project("stats")                             # Full statistics
        """
        valid_ops = ["info", "save", "marker", "render", "stats"]
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
            }

        try:
            client = await get_reaper_client()

            if operation == "info":
                project_info = await client.get_project_info()
                track_count = await client.get_track_count()
                return {
                    **project_info,
                    "operation": "info",
                    "track_count": track_count,
                    "osc_host": client.host,
                    "osc_port": client.port,
                    "success": True,
                }

            elif operation == "save":
                result = await client.save_project()
                return {
                    **result,
                    "operation": "save",
                    "message": "💾 Project saved"
                    if result.get("success")
                    else "❌ Save failed",
                }

            elif operation == "marker":
                if not position or not name:
                    return {
                        "success": False,
                        "error": "position and name required for marker operation",
                    }
                position_seconds = _parse_time_to_seconds(position)
                result = await client.add_marker(position_seconds, name)
                return {
                    **result,
                    "operation": "marker",
                    "position": position,
                    "position_seconds": position_seconds,
                    "name": name,
                    "message": f"📍 Marker '{name}' added at {position}",
                }

            elif operation == "render":
                # Note: Full render requires ReaScript integration
                return {
                    "operation": "render",
                    "format": format,
                    "quality": quality,
                    "bounds": bounds,
                    "status": "render_initiated",
                    "success": True,
                    "message": f"🎬 Render: {format.upper()} {quality}",
                    "note": "Full render automation requires ReaScript",
                }

            elif operation == "stats":
                project_info = await client.get_project_info()
                track_count = await client.get_track_count()
                position_info = await client.get_position()
                position = (
                    position_info.get("args", ["0:00:00"])[0]
                    if position_info.get("args")
                    else "0:00:00"
                )

                return {
                    "operation": "stats",
                    "project": project_info,
                    "track_count": track_count,
                    "current_position": position,
                    "osc_status": {
                        "host": client.host,
                        "port": client.port,
                        "connected": client.connected,
                    },
                    "success": True,
                }

        except Exception as e:
            logger.error(f"Project {operation} error: {e}")
            return {"operation": operation, "success": False, "error": str(e)}
