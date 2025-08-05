#!/usr/bin/env python3
"""
Reaper MCP Server - FastMCP 2.1
Austrian precision digital audio workstation automation via Reaper DAW
"""

import logging
import asyncio
from fastmcp import FastMCP

from reaper_mcp.transport import register_transport_tools
from reaper_mcp.tracks import register_track_tools
from reaper_mcp.project import register_project_tools
from reaper_mcp.osc_client import get_reaper_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP 2.1 server
mcp = FastMCP(
    name="reaper-mcp",
    version="1.0.0", 
    description="Austrian precision audio workstation automation via Reaper DAW with OSC control"
)

def main():
    """Initialize and start the Reaper MCP server"""
    
    # Register all tool modules
    register_transport_tools(mcp)
    register_track_tools(mcp)
    register_project_tools(mcp)
    
    # Register server status tools
    @mcp.tool()
    async def get_server_status() -> dict:
        """Get comprehensive server and Reaper connection status"""
        try:
            client = await get_reaper_client()
            return {
                "server": {
                    "name": "reaper-mcp",
                    "version": "1.0.0",
                    "fastmcp_version": "2.1.0",
                    "status": "running"
                },
                "reaper_connection": {
                    "host": client.host,
                    "port": client.port,
                    "connected": client.connected,
                    "last_status": client.last_status
                },
                "tools_available": len([name for name in mcp._tools.keys()]),
                "resources_available": len([name for name in mcp._resources.keys()]),
                "message": "🎵 Reaper MCP Server operational",
                "austrian_quality": "Erstklassig! 🇦🇹"
            }
        except Exception as e:
            return {
                "server": {
                    "name": "reaper-mcp", 
                    "version": "1.0.0",
                    "status": "running"
                },
                "reaper_connection": {
                    "connected": False,
                    "error": str(e)
                },
                "message": "Server running, but Reaper connection issue"
            }
    
    @mcp.tool()
    def list_capabilities() -> list:
        """List all available MCP tools"""
        tools = list(mcp._tools.keys())
        return {
            "total_tools": len(tools),
            "categories": {
                "transport": [t for t in tools if "transport" in t],
                "tracks": [t for t in tools if "track" in t],
                "project": [t for t in tools if "project" in t or "marker" in t or "render" in t],
                "system": [t for t in tools if "status" in t or "capabilities" in t]
            },
            "all_tools": tools,
            "description": "Austrian audio automation capabilities 🎼"
        }
    
    # Register resources
    @mcp.resource("reaper://config")
    def reaper_config() -> str:
        """Reaper OSC configuration information"""
        import json
        return json.dumps({
            "osc_setup": {
                "host": "127.0.0.1",
                "port": 8000,
                "protocol": "UDP"
            },
            "reaper_setup": [
                "1. Open Reaper preferences (Ctrl+P)",
                "2. Go to Control/OSC/web",
                "3. Add new OSC device",
                "4. Set Local IP: 127.0.0.1",
                "5. Set Local listen port: 8000",
                "6. Set Remote port: 8001", 
                "7. Enable 'Send all feedback'",
                "8. Pattern config: Set to Default.ReaperOSC"
            ],
            "troubleshooting": {
                "connection_failed": "Check Reaper OSC settings and firewall",
                "no_response": "Verify OSC ports (8000/8001) and feedback enabled",
                "permission_denied": "Run as administrator if needed"
            },
            "austrian_support": "Technischer Support auf Deutsch verfügbar! 🇦🇹"
        })
    
    @mcp.resource("reaper://transport")
    def transport_info() -> str:
        """Transport control information"""
        import json
        return json.dumps({
            "commands": {
                "play_transport": "Start playback",
                "stop_transport": "Stop playback", 
                "pause_transport": "Pause playback",
                "record_transport": "Start recording",
                "get_transport_position": "Get current position",
                "transport_status": "Get complete status"
            },
            "osc_patterns": {
                "play": "/play",
                "stop": "/stop", 
                "pause": "/pause",
                "record": "/record",
                "position": "/position"
            }
        })
    
    @mcp.resource("reaper://tracks")
    def tracks_info() -> str:
        """Track management information"""
        import json
        return json.dumps({
            "commands": {
                "get_tracks": "List all tracks",
                "get_track_info": "Get specific track details",
                "arm_track_recording": "Arm/disarm track for recording",
                "mute_track": "Mute/unmute track",
                "solo_track": "Solo/unsolo track",
                "bulk_track_operation": "Bulk operations on multiple tracks"
            },
            "track_properties": ["id", "name", "muted", "solo", "volume", "pan", "armed"],
            "bulk_operations": ["mute", "solo", "arm"]
        })
    
    logger.info("🎵 Starting Reaper MCP Server...")
    logger.info("🇦🇹 Austrian Audio Automation - FastMCP 2.1")
    logger.info("🎛️ Transport, Track & Project control via OSC")
    logger.info("📱 Inspector: http://localhost:8000/inspector")
    
    # Run with stdio transport for Claude Desktop
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
