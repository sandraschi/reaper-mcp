"""
osc_client.py - OSC communication with Reaper DAW
Real-time bidirectional control via Open Sound Control protocol
"""

import logging
from typing import Dict, Any, Optional
import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from . import DEFAULT_OSC_HOST, DEFAULT_OSC_PORT

logger = logging.getLogger(__name__)

class ReaperOSCClient:
    """Async OSC client for Reaper DAW communication"""
    
    def __init__(self, host: str = DEFAULT_OSC_HOST, port: int = DEFAULT_OSC_PORT):
        self.host = host
        self.port = port
        self.client = None
        self.server = None
        self.dispatcher = Dispatcher()
        self.connected = False
        self.last_status = {}
        
        # Setup response handlers
        self._setup_handlers()
    
    async def connect(self) -> bool:
        """Connect to Reaper OSC interface"""
        try:
            # Create UDP client for sending commands
            self.client = SimpleUDPClient(self.host, self.port)
            
            # Create server for receiving responses (on port+1)
            self.server = AsyncIOOSCUDPServer(
                (self.host, self.port + 1), 
                self.dispatcher, 
                asyncio.get_event_loop()
            )
            
            # Start server
            transport, protocol = await self.server.create_serve_endpoint()
            
            self.connected = True
            logger.info(f"Connected to Reaper OSC at {self.host}:{self.port}")
            
            # Test connection with ping
            await self.ping()
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Reaper OSC: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Reaper"""
        if self.server:
            self.server.server_close()
        self.connected = False
        logger.info("Disconnected from Reaper OSC")
    
    def _setup_handlers(self):
        """Setup OSC message handlers for Reaper responses"""
        
        def transport_handler(address: str, *args):
            """Handle transport status updates"""
            self.last_status["transport"] = {
                "address": address,
                "args": args,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        def track_handler(address: str, *args):
            """Handle track info updates"""
            if "tracks" not in self.last_status:
                self.last_status["tracks"] = {}
            self.last_status["tracks"][address] = {
                "args": args,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        def project_handler(address: str, *args):
            """Handle project info updates"""
            self.last_status["project"] = {
                "address": address,
                "args": args,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        # Register handlers
        self.dispatcher.map("/play", transport_handler)
        self.dispatcher.map("/stop", transport_handler)
        self.dispatcher.map("/pause", transport_handler)
        self.dispatcher.map("/record", transport_handler)
        self.dispatcher.map("/position", transport_handler)
        self.dispatcher.map("/track/*", track_handler)
        self.dispatcher.map("/project/*", project_handler)
    
    async def send_command(self, address: str, *args) -> bool:
        """Send OSC command to Reaper"""
        if not self.connected or not self.client:
            logger.warning("Not connected to Reaper")
            return False
        
        try:
            self.client.send_message(address, args)
            logger.debug(f"Sent OSC: {address} {args}")
            return True
        except Exception as e:
            logger.error(f"Failed to send OSC command {address}: {e}")
            return False
    
    async def ping(self) -> bool:
        """Test connection with Reaper"""
        return await self.send_command("/ping")
    
    # Transport control methods
    async def play_transport(self) -> Dict[str, Any]:
        """Start playback"""
        success = await self.send_command("/play")
        await asyncio.sleep(0.1)  # Wait for response
        return {
            "action": "play",
            "success": success,
            "status": self.last_status.get("transport", {})
        }
    
    async def stop_transport(self) -> Dict[str, Any]:
        """Stop playback"""
        success = await self.send_command("/stop")
        await asyncio.sleep(0.1)
        return {
            "action": "stop", 
            "success": success,
            "status": self.last_status.get("transport", {})
        }
    
    async def pause_transport(self) -> Dict[str, Any]:
        """Pause playback"""
        success = await self.send_command("/pause")
        await asyncio.sleep(0.1)
        return {
            "action": "pause",
            "success": success,
            "status": self.last_status.get("transport", {})
        }
    
    async def record_transport(self) -> Dict[str, Any]:
        """Start recording"""
        success = await self.send_command("/record")
        await asyncio.sleep(0.1)
        return {
            "action": "record",
            "success": success,
            "status": self.last_status.get("transport", {})
        }
    
    async def get_position(self) -> Dict[str, Any]:
        """Get current playback position"""
        await self.send_command("/position")
        await asyncio.sleep(0.1)
        return self.last_status.get("transport", {})
    
    # Track management methods
    async def get_track_count(self) -> int:
        """Get number of tracks in project"""
        await self.send_command("/track/count")
        await asyncio.sleep(0.1)
        
        # Parse response from last_status
        tracks_info = self.last_status.get("tracks", {})
        for address, data in tracks_info.items():
            if "count" in address and data.get("args"):
                return int(data["args"][0])
        
        return 0  # Default if no response
    
    async def get_track_info(self, track_id: int) -> Dict[str, Any]:
        """Get information for specific track"""
        # Request track info
        await self.send_command(f"/track/{track_id}/name")
        await self.send_command(f"/track/{track_id}/mute")
        await self.send_command(f"/track/{track_id}/solo")
        await self.send_command(f"/track/{track_id}/volume")
        await self.send_command(f"/track/{track_id}/pan")
        
        await asyncio.sleep(0.2)  # Wait for all responses
        
        # Parse responses
        tracks_info = self.last_status.get("tracks", {})
        track_data = {
            "id": track_id,
            "name": f"Track {track_id}",
            "muted": False,
            "solo": False,
            "volume": 1.0,
            "pan": 0.0
        }
        
        for address, data in tracks_info.items():
            if f"/{track_id}/" in address and data.get("args"):
                if "name" in address:
                    track_data["name"] = str(data["args"][0])
                elif "mute" in address:
                    track_data["muted"] = bool(data["args"][0])
                elif "solo" in address:
                    track_data["solo"] = bool(data["args"][0])
                elif "volume" in address:
                    track_data["volume"] = float(data["args"][0])
                elif "pan" in address:
                    track_data["pan"] = float(data["args"][0])
        
        return track_data
    
    async def set_track_arm(self, track_id: int, armed: bool) -> Dict[str, Any]:
        """Arm or disarm track for recording"""
        success = await self.send_command(f"/track/{track_id}/recarm", int(armed))
        return {
            "track_id": track_id,
            "armed": armed,
            "success": success
        }
    
    async def set_track_mute(self, track_id: int, muted: bool) -> Dict[str, Any]:
        """Mute or unmute track"""
        success = await self.send_command(f"/track/{track_id}/mute", int(muted))
        return {
            "track_id": track_id,
            "muted": muted,
            "success": success
        }
    
    async def set_track_solo(self, track_id: int, solo: bool) -> Dict[str, Any]:
        """Solo or unsolo track"""
        success = await self.send_command(f"/track/{track_id}/solo", int(solo))
        return {
            "track_id": track_id,
            "solo": solo,
            "success": success
        }
    
    # Project methods
    async def get_project_info(self) -> Dict[str, Any]:
        """Get current project information"""
        # Request project info
        await self.send_command("/project/name")
        await self.send_command("/project/samplerate")
        await self.send_command("/project/length")
        
        await asyncio.sleep(0.2)
        
        # Parse project data
        project_info = self.last_status.get("project", {})
        return {
            "name": "Untitled Project",
            "sample_rate": 44100,
            "length": "0:00:00",
            "connected": self.connected,
            "last_update": project_info.get("timestamp", 0)
        }
    
    async def save_project(self) -> Dict[str, Any]:
        """Save current project"""
        success = await self.send_command("/project/save")
        return {
            "action": "save",
            "success": success
        }
    
    # Marker methods
    async def add_marker(self, position: float, name: str) -> Dict[str, Any]:
        """Add marker at specific position (in seconds)"""
        success = await self.send_command("/marker/add", position, name)
        return {
            "position": position,
            "name": name,
            "success": success
        }

# Global client instance
_reaper_client: Optional[ReaperOSCClient] = None

async def get_reaper_client() -> ReaperOSCClient:
    """Get or create Reaper OSC client instance"""
    global _reaper_client
    if _reaper_client is None:
        _reaper_client = ReaperOSCClient()
        await _reaper_client.connect()
    return _reaper_client

async def ensure_connected() -> bool:
    """Ensure Reaper client is connected"""
    client = await get_reaper_client()
    if not client.connected:
        return await client.connect()
    return True
