#!/usr/bin/env python3
"""
Development testing script for Reaper MCP Server
Test OSC connection and tools without MCP client
"""

import asyncio
import logging
from reaper_mcp.osc_client import ReaperOSCClient, get_reaper_client
from reaper_mcp import DEFAULT_OSC_HOST, DEFAULT_OSC_PORT

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dev_test.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

async def test_osc_connection():
    """Test basic OSC connection to Reaper"""
    logger.info("🔌 Testing OSC Connection...")

    client = ReaperOSCClient(DEFAULT_OSC_HOST, DEFAULT_OSC_PORT)

    try:
        connected = await client.connect()
        if connected:
            logger.info(f"✅ Connected to Reaper OSC at {DEFAULT_OSC_HOST}:{DEFAULT_OSC_PORT}")

            # Test ping
            ping_result = await client.ping()
            logger.info(f"📡 Ping test: {'✅ Success' if ping_result else '❌ Failed'}")

        else:
            logger.error(f"❌ Failed to connect to Reaper OSC")
            logger.warning("💡 Make sure Reaper is running with OSC enabled")

    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        logger.warning("💡 Check Reaper OSC settings and firewall")

    finally:
        await client.disconnect()

async def test_transport_control():
    """Test transport control functions"""
    logger.info("🎵 Testing Transport Control...")

    try:
        client = await get_reaper_client()

        # Test play
        logger.info("▶️ Testing play...")
        play_result = await client.play_transport()
        logger.info(f"Play result: {play_result}")

        await asyncio.sleep(2)

        # Test stop
        logger.info("⏹️ Testing stop...")
        stop_result = await client.stop_transport()
        logger.info(f"Stop result: {stop_result}")

        # Test position
        logger.info("📍 Testing position...")
        position_result = await client.get_position()
        logger.info(f"Position: {position_result}")

    except Exception as e:
        logger.error(f"❌ Transport test error: {e}")

async def test_track_management():
    """Test track management functions"""
    logger.info("🎛️ Testing Track Management...")

    try:
        client = await get_reaper_client()

        # Get track count
        logger.info("📊 Getting track count...")
        track_count = await client.get_track_count()
        logger.info(f"Track count: {track_count}")

        if track_count > 0:
            # Get info for first track
            logger.info("🎼 Getting track 1 info...")
            track_info = await client.get_track_info(1)
            logger.info(f"Track 1: {track_info}")

            # Test mute/unmute
            logger.info("🔇 Testing mute/unmute...")
            mute_result = await client.set_track_mute(1, True)
            logger.info(f"Mute result: {mute_result}")

            await asyncio.sleep(1)

            unmute_result = await client.set_track_mute(1, False)
            logger.info(f"Unmute result: {unmute_result}")
        else:
            logger.warning("📝 No tracks found - create some tracks in Reaper first")

    except Exception as e:
        logger.error(f"❌ Track test error: {e}")

async def test_project_info():
    """Test project information retrieval"""
    logger.info("📽️ Testing Project Info...")

    try:
        client = await get_reaper_client()

        project_info = await client.get_project_info()
        logger.info(f"Project info: {project_info}")

        # Test marker addition
        logger.info("📍 Testing marker addition...")
        marker_result = await client.add_marker(30.0, "Test Marker")
        logger.info(f"Marker result: {marker_result}")

    except Exception as e:
        logger.error(f"❌ Project test error: {e}")

async def main():
    """Run all development tests"""
    logger.info("🚀 Reaper MCP Development Testing")
    logger.info("🇦🇹 Austrian Audio Automation Test Suite")
    logger.info("=" * 50)

    # Test all components
    await test_osc_connection()
    await test_transport_control()
    await test_track_management()
    await test_project_info()

    logger.info("=" * 50)
    logger.info("🎯 Development testing complete!")
    logger.info("🎼 Ready for Austrian audio automation!")
    logger.info("💡 Next steps:")
    logger.info("1. Make sure Reaper OSC is configured (see README)")
    logger.info("2. Test with: python server.py")
    logger.info("3. Add to Claude Desktop MCP configuration")

if __name__ == "__main__":
    asyncio.run(main())
