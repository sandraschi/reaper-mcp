import pytest

pytestmark = pytest.mark.skip(reason="Legacy granular-tool tests; server uses portmanteau tools")

"""
Integration tests for transport control tools
Tests end-to-end functionality with mocked Reaper OSC client
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastmcp import FastMCP


@pytest.fixture
def mock_mcp():
    """Create a mock FastMCP server for testing"""
    mcp = Mock(spec=FastMCP)
    # Help the mock handle attribute access for tools
    mcp.tools = []
    return mcp


@pytest.fixture
def mock_reaper_client():
    """Create a mock Reaper OSC client"""
    client = AsyncMock()
    client.host = "127.0.0.1"
    client.port = 8000
    client.connected = True
    client.last_status = "OK"

    # Mock transport methods
    client.play_transport.return_value = {"success": True, "position": "0:00:00"}
    client.stop_transport.return_value = {"success": True, "position": "0:05:30"}
    client.pause_transport.return_value = {"success": True, "position": "0:02:15"}
    client.record_transport.return_value = {"success": True, "recording": True}
    client.get_position.return_value = {"args": ["0:01:23"], "timestamp": 1234567890}

    return client


class TestTransportIntegration:
    """Integration tests for transport control functionality"""

    @pytest.mark.asyncio
    async def test_play_transport_integration(self, mock_mcp, mock_reaper_client):
        """Test full play transport workflow"""
        with (
            patch(
                "reaper_mcp.transport.get_reaper_client",
                return_value=mock_reaper_client,
            ),
            patch("reaper_mcp.transport.ensure_connected", return_value=True),
        ):
            from reaper_mcp.transport import register_transport_tools

            # Register tools with mock MCP
            register_transport_tools(mock_mcp)

            # Get the play_transport tool (it's stored as an attribute on the mock)
            # In real usage, this would be called via MCP, but for testing we call directly
            play_result = await mock_mcp.play_transport()

            assert play_result["success"] is True
            assert play_result["message"] == "🎵 Playback started"
            assert "austrian_efficiency" in play_result

            # Verify the OSC client was called
            mock_reaper_client.play_transport.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_transport_integration(self, mock_mcp, mock_reaper_client):
        """Test full stop transport workflow"""
        with (
            patch(
                "reaper_mcp.transport.get_reaper_client",
                return_value=mock_reaper_client,
            ),
            patch("reaper_mcp.transport.ensure_connected", return_value=True),
        ):
            from reaper_mcp.transport import register_transport_tools

            register_transport_tools(mock_mcp)

            stop_result = await mock_mcp.stop_transport()

            assert stop_result["success"] is True
            assert stop_result["message"] == "⏹️ Playback stopped"
            assert stop_result["ready_for_next"] is True

            mock_reaper_client.stop_transport.assert_called_once()

    @pytest.mark.asyncio
    async def test_transport_status_integration(self, mock_mcp, mock_reaper_client):
        """Test transport status retrieval"""
        with (
            patch(
                "reaper_mcp.transport.get_reaper_client",
                return_value=mock_reaper_client,
            ),
            patch("reaper_mcp.transport.ensure_connected", return_value=True),
        ):
            from reaper_mcp.transport import register_transport_tools

            register_transport_tools(mock_mcp)

            status_result = await mock_mcp.transport_status()

            assert status_result["connected"] is True
            assert status_result["host"] == "127.0.0.1"
            assert status_result["port"] == 8000
            assert status_result["position"] == "0:01:23"
            assert status_result["reaper_responsive"] is True
            assert "austrian_status" in status_result

    @pytest.mark.asyncio
    async def test_transport_connection_failure(self, mock_mcp):
        """Test transport operations when connection fails"""
        with patch("reaper_mcp.transport.ensure_connected", return_value=False):
            from reaper_mcp.transport import register_transport_tools

            register_transport_tools(mock_mcp)

            play_result = await mock_mcp.play_transport()

            assert play_result["success"] is False
            assert "Not connected to Reaper" in play_result["error"]
            assert "suggestion" in play_result

    @pytest.mark.asyncio
    async def test_transport_osc_error(self, mock_mcp, mock_reaper_client):
        """Test transport operations when OSC command fails"""
        mock_reaper_client.play_transport.side_effect = Exception("OSC timeout")

        with (
            patch(
                "reaper_mcp.transport.get_reaper_client",
                return_value=mock_reaper_client,
            ),
            patch("reaper_mcp.transport.ensure_connected", return_value=True),
        ):
            from reaper_mcp.transport import register_transport_tools

            register_transport_tools(mock_mcp)

            play_result = await mock_mcp.play_transport()

            assert play_result["success"] is False
            assert play_result["error"] == "OSC timeout"
            assert play_result["action"] == "play"


class TestTransportWorkflow:
    """Test complete transport control workflows"""

    @pytest.mark.asyncio
    async def test_record_workflow(self, mock_mcp, mock_reaper_client):
        """Test recording workflow: play -> record -> stop"""
        with (
            patch(
                "reaper_mcp.transport.get_reaper_client",
                return_value=mock_reaper_client,
            ),
            patch("reaper_mcp.transport.ensure_connected", return_value=True),
        ):
            from reaper_mcp.transport import register_transport_tools

            register_transport_tools(mock_mcp)

            # Start playback
            play_result = await mock_mcp.play_transport()
            assert play_result["success"] is True

            # Start recording
            record_result = await mock_mcp.record_transport()
            assert record_result["success"] is True
            assert record_result["message"] == "🔴 Recording started"
            assert record_result["warning"] == "Make sure tracks are armed!"

            # Stop everything
            stop_result = await mock_mcp.stop_transport()
            assert stop_result["success"] is True

            # Verify all methods were called
            mock_reaper_client.play_transport.assert_called_once()
            mock_reaper_client.record_transport.assert_called_once()
            mock_reaper_client.stop_transport.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
