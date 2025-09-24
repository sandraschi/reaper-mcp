"""
tracks.py - Reaper track management tools for FastMCP 2.1
Austrian precision track control and automation
"""

import logging
from typing import Dict, Any, List
from .osc_client import get_reaper_client, ensure_connected
from .validation import TrackValidation, CommonValidation, ValidationError

logger = logging.getLogger(__name__)

def register_track_tools(mcp):
    """Register track management tools with FastMCP server"""
    
    @mcp.tool()
    async def get_tracks() -> List[Dict[str, Any]]:
        """Get list of all tracks in current Reaper project
        
        Returns:
            List of track dictionaries with details
        """
        if not await ensure_connected():
            return [{
                "error": "Not connected to Reaper",
                "suggestion": "Start Reaper and enable OSC control"
            }]
        
        try:
            client = await get_reaper_client()
            track_count = await client.get_track_count()
            
            if track_count == 0:
                return [{
                    "message": "No tracks found",
                    "suggestion": "Create tracks in Reaper first"
                }]
            
            tracks = []
            for track_id in range(1, track_count + 1):
                track_info = await client.get_track_info(track_id)
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Get tracks error: {e}")
            return [{
                "error": str(e),
                "connected": False
            }]
    
    @mcp.tool()
    async def get_track_info(track_id: int) -> Dict[str, Any]:
        """Get detailed information for specific track

        Args:
            track_id: Track number (1-based indexing)

        Returns:
            Dictionary with track details
        """
        # Input validation
        try:
            validated_track_id = TrackValidation.validate_track_id(track_id)
        except ValidationError as e:
            return {
                "track_id": track_id,
                "success": False,
                "error": str(e),
                "suggestion": "Use a valid track number (1 or greater)"
            }

        if not await ensure_connected():
            return {
                "track_id": validated_track_id,
                "success": False,
                "error": "Not connected to Reaper",
                "suggestion": "Start Reaper and enable OSC control"
            }

        try:
            client = await get_reaper_client()
            track_info = await client.get_track_info(validated_track_id)
            return {
                **track_info,
                "track_id": validated_track_id,
                "success": True,
                "austrian_precision": "Track info retrieved! 🎼"
            }
        except Exception as e:
            logger.error(f"Get track info error for track {validated_track_id}: {e}")
            return {
                "track_id": validated_track_id,
                "success": False,
                "error": str(e),
                "suggestion": "Check if track exists and Reaper is responsive"
            }
    
    @mcp.tool()
    async def arm_track_recording(track_id: int, armed: bool = True) -> Dict[str, Any]:
        """Arm or disarm track for recording

        Args:
            track_id: Track number to arm/disarm
            armed: True to arm, False to disarm

        Returns:
            Dictionary with arming status
        """
        # Input validation
        try:
            validated_track_id = TrackValidation.validate_track_id(track_id)
            validated_armed = CommonValidation.validate_boolean(armed)
        except ValidationError as e:
            return {
                "track_id": track_id,
                "armed": armed,
                "success": False,
                "error": str(e),
                "suggestion": "Use valid track ID and true/false for armed parameter"
            }

        if not await ensure_connected():
            return {
                "track_id": validated_track_id,
                "armed": validated_armed,
                "success": False,
                "error": "Not connected to Reaper",
                "suggestion": "Start Reaper and enable OSC control"
            }

        try:
            client = await get_reaper_client()
            result = await client.set_track_arm(validated_track_id, validated_armed)

            action = "🔴 Armed" if validated_armed else "⚪ Disarmed"
            return {
                **result,
                "track_id": validated_track_id,
                "armed": validated_armed,
                "success": True,
                "message": f"{action} track {validated_track_id} for recording",
                "ready_to_record": validated_armed,
                "austrian_precision": "Recording status updated! 🎙️"
            }
        except Exception as e:
            logger.error(f"Track arm error for track {validated_track_id}: {e}")
            return {
                "track_id": validated_track_id,
                "armed": validated_armed,
                "success": False,
                "error": str(e),
                "suggestion": "Check if track exists and Reaper is responsive"
            }
    
    @mcp.tool()
    async def mute_track(track_id: int, muted: bool = True) -> Dict[str, Any]:
        """Mute or unmute a track
        
        Args:
            track_id: Track number to mute/unmute
            muted: True to mute, False to unmute
            
        Returns:
            Dictionary with mute status
        """
        if not await ensure_connected():
            return {
                "track_id": track_id,
                "muted": muted,
                "success": False,
                "error": "Not connected to Reaper"
            }
        
        try:
            client = await get_reaper_client()
            result = await client.set_track_mute(track_id, muted)
            
            action = "🔇 Muted" if muted else "🔊 Unmuted"
            return {
                **result,
                "message": f"{action} track {track_id}",
                "audio_output": not muted
            }
        except Exception as e:
            logger.error(f"Track mute error: {e}")
            return {
                "track_id": track_id,
                "muted": muted,
                "success": False,
                "error": str(e)
            }
    
    @mcp.tool()
    async def solo_track(track_id: int, solo: bool = True) -> Dict[str, Any]:
        """Solo or unsolo a track
        
        Args:
            track_id: Track number to solo/unsolo
            solo: True to solo, False to unsolo
            
        Returns:
            Dictionary with solo status
        """
        if not await ensure_connected():
            return {
                "track_id": track_id,
                "solo": solo,
                "success": False,
                "error": "Not connected to Reaper"
            }
        
        try:
            client = await get_reaper_client()
            result = await client.set_track_solo(track_id, solo)
            
            action = "🎵 Soloed" if solo else "🎼 Unsoloed"
            return {
                **result,
                "message": f"{action} track {track_id}",
                "exclusive_playback": solo
            }
        except Exception as e:
            logger.error(f"Track solo error: {e}")
            return {
                "track_id": track_id,
                "solo": solo,
                "success": False,
                "error": str(e)
            }
    
    @mcp.tool()
    async def get_track_count() -> Dict[str, Any]:
        """Get total number of tracks in project
        
        Returns:
            Dictionary with track count and project info
        """
        if not await ensure_connected():
            return {
                "track_count": 0,
                "connected": False,
                "error": "Not connected to Reaper"
            }
        
        try:
            client = await get_reaper_client()
            count = await client.get_track_count()
            
            return {
                "track_count": count,
                "connected": True,
                "message": f"📊 Found {count} tracks in project",
                "status": "healthy" if count > 0 else "empty_project"
            }
        except Exception as e:
            logger.error(f"Get track count error: {e}")
            return {
                "track_count": 0,
                "connected": False,
                "error": str(e)
            }
    
    @mcp.tool()
    async def bulk_track_operation(operation: str, track_ids: List[int], value: bool = True) -> Dict[str, Any]:
        """Perform bulk operations on multiple tracks
        
        Args:
            operation: Operation type ('mute', 'solo', 'arm')
            track_ids: List of track IDs to operate on
            value: True/False for the operation
            
        Returns:
            Dictionary with bulk operation results
        """
        if not await ensure_connected():
            return {
                "operation": operation,
                "track_ids": track_ids,
                "success": False,
                "error": "Not connected to Reaper"
            }
        
        if operation not in ['mute', 'solo', 'arm']:
            return {
                "operation": operation,
                "track_ids": track_ids,
                "success": False,
                "error": "Invalid operation. Use 'mute', 'solo', or 'arm'"
            }
        
        try:
            client = await get_reaper_client()
            results = []
            
            for track_id in track_ids:
                if operation == 'mute':
                    result = await client.set_track_mute(track_id, value)
                elif operation == 'solo':
                    result = await client.set_track_solo(track_id, value)
                elif operation == 'arm':
                    result = await client.set_track_arm(track_id, value)
                
                results.append({
                    "track_id": track_id,
                    "success": result.get("success", False)
                })
            
            successful = sum(1 for r in results if r["success"])
            
            return {
                "operation": operation,
                "value": value,
                "total_tracks": len(track_ids),
                "successful": successful,
                "failed": len(track_ids) - successful,
                "results": results,
                "message": f"🎛️ Bulk {operation}: {successful}/{len(track_ids)} tracks",
                "austrian_efficiency": "Bulk operations completed! 🇦🇹"
            }
            
        except Exception as e:
            logger.error(f"Bulk track operation error: {e}")
            return {
                "operation": operation,
                "track_ids": track_ids,
                "success": False,
                "error": str(e)
            }
