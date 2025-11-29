"""
reaper_tracks - Consolidated track management portmanteau tool.

OPERATIONS:
- list: Get all tracks
- info: Get specific track info
- mute: Mute/unmute track
- solo: Solo/unsolo track
- arm: Arm/disarm track for recording
- count: Get track count
- bulk: Bulk operations on multiple tracks
"""

import logging
from typing import Any

from ..osc_client import get_reaper_client, ensure_connected

logger = logging.getLogger(__name__)


def setup_tracks_portmanteau(mcp):
    """Register the reaper_tracks portmanteau tool."""

    @mcp.tool()
    async def reaper_tracks(
        operation: str,
        track_id: int | None = None,
        track_ids: list[int] | None = None,
        value: bool = True,
        bulk_operation: str | None = None,
    ) -> dict[str, Any]:
        """Consolidated track management for Reaper DAW.

        OPERATIONS:
        - list: Get all tracks in project
        - info: Get specific track details (requires track_id)
        - mute: Mute/unmute track (requires track_id, value=True/False)
        - solo: Solo/unsolo track (requires track_id, value=True/False)
        - arm: Arm/disarm for recording (requires track_id, value=True/False)
        - count: Get total track count
        - bulk: Bulk operations (requires track_ids, bulk_operation, value)

        Args:
            operation: Operation to perform
            track_id: Track number (1-based) for single-track operations
            track_ids: List of track IDs for bulk operations
            value: True/False for mute/solo/arm operations
            bulk_operation: For bulk op: 'mute', 'solo', or 'arm'

        Returns:
            Operation result with track data

        Examples:
            reaper_tracks("list")                           # All tracks
            reaper_tracks("info", track_id=1)              # Track 1 info
            reaper_tracks("mute", track_id=2, value=True)  # Mute track 2
            reaper_tracks("solo", track_id=1)              # Solo track 1
            reaper_tracks("arm", track_id=3, value=True)   # Arm track 3
            reaper_tracks("bulk", track_ids=[1,2,3], bulk_operation="mute", value=True)
        """
        valid_ops = ["list", "info", "mute", "solo", "arm", "count", "bulk"]
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

            if operation == "list":
                track_count = await client.get_track_count()
                if track_count == 0:
                    return {"operation": "list", "tracks": [], "message": "No tracks found"}

                tracks = []
                for tid in range(1, track_count + 1):
                    track_info = await client.get_track_info(tid)
                    tracks.append(track_info)
                return {"operation": "list", "tracks": tracks, "count": track_count, "success": True}

            elif operation == "info":
                if track_id is None:
                    return {"success": False, "error": "track_id required for info operation"}
                track_info = await client.get_track_info(track_id)
                return {**track_info, "operation": "info", "track_id": track_id, "success": True}

            elif operation == "mute":
                if track_id is None:
                    return {"success": False, "error": "track_id required for mute operation"}
                result = await client.set_track_mute(track_id, value)
                action = "🔇 Muted" if value else "🔊 Unmuted"
                return {**result, "operation": "mute", "track_id": track_id, "muted": value, "message": f"{action} track {track_id}"}

            elif operation == "solo":
                if track_id is None:
                    return {"success": False, "error": "track_id required for solo operation"}
                result = await client.set_track_solo(track_id, value)
                action = "🎵 Soloed" if value else "🎼 Unsoloed"
                return {**result, "operation": "solo", "track_id": track_id, "solo": value, "message": f"{action} track {track_id}"}

            elif operation == "arm":
                if track_id is None:
                    return {"success": False, "error": "track_id required for arm operation"}
                result = await client.set_track_arm(track_id, value)
                action = "🔴 Armed" if value else "⚪ Disarmed"
                return {**result, "operation": "arm", "track_id": track_id, "armed": value, "message": f"{action} track {track_id}"}

            elif operation == "count":
                count = await client.get_track_count()
                return {"operation": "count", "track_count": count, "success": True}

            elif operation == "bulk":
                if not track_ids:
                    return {"success": False, "error": "track_ids required for bulk operation"}
                if bulk_operation not in ["mute", "solo", "arm"]:
                    return {"success": False, "error": "bulk_operation must be 'mute', 'solo', or 'arm'"}

                results = []
                for tid in track_ids:
                    if bulk_operation == "mute":
                        result = await client.set_track_mute(tid, value)
                    elif bulk_operation == "solo":
                        result = await client.set_track_solo(tid, value)
                    else:
                        result = await client.set_track_arm(tid, value)
                    results.append({"track_id": tid, "success": result.get("success", False)})

                successful = sum(1 for r in results if r["success"])
                return {
                    "operation": "bulk",
                    "bulk_operation": bulk_operation,
                    "value": value,
                    "total": len(track_ids),
                    "successful": successful,
                    "results": results,
                    "success": True,
                }

        except Exception as e:
            logger.error(f"Tracks {operation} error: {e}")
            return {"operation": operation, "success": False, "error": str(e)}

