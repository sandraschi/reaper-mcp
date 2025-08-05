#!/usr/bin/env python3
"""
Development testing script for Reaper MCP Server
Test OSC connection and tools without MCP client
"""

import asyncio
import logging
from reaper_mcp.osc_client import ReaperOSCClient, get_reaper_client
from reaper_mcp import DEFAULT_OSC_HOST, DEFAULT_OSC_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_osc_connection():
    """Test basic OSC connection to Reaper"""
    print("\n🔌 Testing OSC Connection...")
    
    client = ReaperOSCClient(DEFAULT_OSC_HOST, DEFAULT_OSC_PORT)
    
    try:
        connected = await client.connect()
        if connected:
            print(f"✅ Connected to Reaper OSC at {DEFAULT_OSC_HOST}:{DEFAULT_OSC_PORT}")
            
            # Test ping
            ping_result = await client.ping()
            print(f"📡 Ping test: {'✅ Success' if ping_result else '❌ Failed'}")
            
        else:
            print(f"❌ Failed to connect to Reaper OSC")
            print("💡 Make sure Reaper is running with OSC enabled")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Check Reaper OSC settings and firewall")
    
    finally:
        await client.disconnect()

async def test_transport_control():
    """Test transport control functions"""
    print("\n🎵 Testing Transport Control...")
    
    try:
        client = await get_reaper_client()
        
        # Test play
        print("▶️ Testing play...")
        play_result = await client.play_transport()
        print(f"Play result: {play_result}")
        
        await asyncio.sleep(2)
        
        # Test stop
        print("⏹️ Testing stop...")
        stop_result = await client.stop_transport()
        print(f"Stop result: {stop_result}")
        
        # Test position
        print("📍 Testing position...")
        position_result = await client.get_position()
        print(f"Position: {position_result}")
        
    except Exception as e:
        print(f"❌ Transport test error: {e}")

async def test_track_management():
    """Test track management functions"""
    print("\n🎛️ Testing Track Management...")
    
    try:
        client = await get_reaper_client()
        
        # Get track count
        print("📊 Getting track count...")
        track_count = await client.get_track_count()
        print(f"Track count: {track_count}")
        
        if track_count > 0:
            # Get info for first track
            print("🎼 Getting track 1 info...")
            track_info = await client.get_track_info(1)
            print(f"Track 1: {track_info}")
            
            # Test mute/unmute
            print("🔇 Testing mute/unmute...")
            mute_result = await client.set_track_mute(1, True)
            print(f"Mute result: {mute_result}")
            
            await asyncio.sleep(1)
            
            unmute_result = await client.set_track_mute(1, False)
            print(f"Unmute result: {unmute_result}")
        else:
            print("📝 No tracks found - create some tracks in Reaper first")
            
    except Exception as e:
        print(f"❌ Track test error: {e}")

async def test_project_info():
    """Test project information retrieval"""
    print("\n📽️ Testing Project Info...")
    
    try:
        client = await get_reaper_client()
        
        project_info = await client.get_project_info()
        print(f"Project info: {project_info}")
        
        # Test marker addition
        print("📍 Testing marker addition...")
        marker_result = await client.add_marker(30.0, "Test Marker")
        print(f"Marker result: {marker_result}")
        
    except Exception as e:
        print(f"❌ Project test error: {e}")

async def main():
    """Run all development tests"""
    print("🚀 Reaper MCP Development Testing")
    print("🇦🇹 Austrian Audio Automation Test Suite")
    print("=" * 50)
    
    # Test all components
    await test_osc_connection()
    await test_transport_control()
    await test_track_management()
    await test_project_info()
    
    print("\n" + "=" * 50)
    print("🎯 Development testing complete!")
    print("🎼 Ready for Austrian audio automation!")
    print("\n💡 Next steps:")
    print("1. Make sure Reaper OSC is configured (see README)")
    print("2. Test with: python server.py")
    print("3. Add to Claude Desktop MCP configuration")

if __name__ == "__main__":
    asyncio.run(main())
