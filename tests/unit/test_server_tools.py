import pytest

pytestmark = pytest.mark.skip(reason="Legacy granular-tool tests; server uses portmanteau tools")

"""
Unit tests for server-level MCP tools
Tests help tool and other server functionality
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP


class TestHelpTool:
    """Test the get_help tool functionality"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock FastMCP server with tools"""
        mcp = Mock(spec=FastMCP)
        mcp._tools = {
            "play_transport": Mock(),
            "stop_transport": Mock(),
            "get_tracks": Mock(),
            "get_help": Mock(),
            "get_server_status": Mock(),
        }
        mcp._resources = {}
        return mcp

    def test_get_help_overview(self, mock_mcp):
        """Test get_help with no parameters returns overview"""
        # Import here to avoid circular imports
        from unittest.mock import patch

        # Mock the server module to return our mock MCP
        with patch("server.mcp", mock_mcp):
            from server import get_help

            result = get_help()

            assert "server_info" in result
            assert "categories_overview" in result
            assert "usage_tips" in result
            assert result["server_info"]["name"] == "Reaper MCP Server"
            assert len(result["categories_overview"]) == 4  # transport, tracks, project, system

    def test_get_help_category_transport(self, mock_mcp):
        """Test get_help with transport category"""
        from unittest.mock import patch

        with patch("server.mcp", mock_mcp):
            from server import get_help

            result = get_help(category="transport")

            assert "category_help" in result
            assert result["category_help"]["category"] == "transport"
            assert "tools" in result["category_help"]
            assert "play_transport" in result["category_help"]["tools"]

    def test_get_help_category_invalid(self, mock_mcp):
        """Test get_help with invalid category"""
        from unittest.mock import patch

        with patch("server.mcp", mock_mcp):
            from server import get_help

            result = get_help(category="invalid")

            assert "error" in result
            assert "not found" in result["error"]

    def test_get_help_tool_valid(self, mock_mcp):
        """Test get_help with valid tool name"""
        from unittest.mock import patch

        with patch("server.mcp", mock_mcp):
            from server import get_help

            result = get_help(tool_name="play_transport")

            assert "tool_help" in result
            assert result["tool_help"]["name"] == "play_transport"
            assert "description" in result["tool_help"]
            assert "usage" in result["tool_help"]

    def test_get_help_tool_invalid(self, mock_mcp):
        """Test get_help with invalid tool name"""
        from unittest.mock import patch

        with patch("server.mcp", mock_mcp):
            from server import get_help

            result = get_help(tool_name="invalid_tool")

            assert "error" in result
            assert "not found" in result["error"]


class TestServerStatusTool:
    """Test the get_server_status tool"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock FastMCP server"""
        mcp = Mock(spec=FastMCP)
        mcp._tools = {"tool1": Mock(), "tool2": Mock()}
        mcp._resources = {"resource1": Mock()}
        return mcp

    @pytest.mark.asyncio
    async def test_get_server_status_connected(self, mock_mcp):
        """Test get_server_status when connected to Reaper"""
        # Mock the OSC client
        mock_client = AsyncMock()
        mock_client.host = "127.0.0.1"
        mock_client.port = 8000
        mock_client.connected = True
        mock_client.last_status = "OK"

        from unittest.mock import patch

        with (
            patch("server.get_reaper_client", return_value=mock_client),
            patch("server.mcp", mock_mcp),
        ):
            from server import get_server_status

            result = await get_server_status()

            assert result["server"]["status"] == "running"
            assert result["reaper_connection"]["connected"] is True
            assert result["tools_available"] == 2
            assert "austrian_quality" in result

    @pytest.mark.asyncio
    async def test_get_server_status_disconnected(self, mock_mcp):
        """Test get_server_status when not connected to Reaper"""
        from unittest.mock import patch

        with (
            patch("server.get_reaper_client", side_effect=Exception("Connection failed")),
            patch("server.mcp", mock_mcp),
        ):
            from server import get_server_status

            result = await get_server_status()

            assert result["server"]["status"] == "running"
            assert result["reaper_connection"]["connected"] is False
            assert "error" in result["reaper_connection"]


if __name__ == "__main__":
    pytest.main([__file__])
