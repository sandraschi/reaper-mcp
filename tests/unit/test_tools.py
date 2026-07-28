import pytest

from tests.tool_helpers import tool_payload

# We need to import the tool functions.
# Since they are decorated in the server, we might need to test the logic directly or use the FastMCP call mechanisem.
# FastMCP tools are registered. We can access them via server.tools


@pytest.mark.asyncio
async def test_system_status(mcp_server):
    """Test the system status operation."""
    result = tool_payload(await mcp_server.call_tool("reaper_system", arguments={"operation": "status"}))
    assert result["success"] is True
    assert result["operation"] == "status"
    assert result["server"]["status"] == "running"
    assert "connected" in result["reaper_connection"]


@pytest.mark.asyncio
async def test_system_help(mcp_server):
    """Test the system help operation."""
    result = tool_payload(await mcp_server.call_tool("reaper_system", arguments={"operation": "help"}))
    assert result["success"] is True
    assert "tools" in result


@pytest.mark.asyncio
async def test_transport_status(mcp_server):
    """Test transport status."""
    result = tool_payload(await mcp_server.call_tool("reaper_transport", arguments={"operation": "status"}))
    assert result["success"] is True
    assert result["operation"] == "status"


@pytest.mark.asyncio
async def test_tracks_count(mcp_server):
    """Test track count."""
    result = tool_payload(await mcp_server.call_tool("reaper_tracks", arguments={"operation": "count"}))
    assert result["success"] is True
    assert result["track_count"] == 5


@pytest.mark.asyncio
async def test_reascript_setup(mcp_server):
    """Test reascript tool is registered."""
    tools = await mcp_server.list_tools()
    tool_names = [t.name for t in tools]
    assert "reaper_reascript" in tool_names
