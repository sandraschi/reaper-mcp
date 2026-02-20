import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

# Add project root to path
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Mock reapy and pythonosc before any imports
sys.modules["reapy"] = MagicMock()
sys.modules["reapy.core"] = MagicMock()
sys.modules["pythonosc"] = MagicMock()
sys.modules["pythonosc.udp_client"] = MagicMock()

import server


@pytest.fixture
def mock_osc_client(monkeypatch):
    """Mock the OSC client to avoid network calls."""
    mock_client = AsyncMock()
    mock_client.host = "127.0.0.1"
    mock_client.port = 8000
    mock_client.connected = True

    async def mock_get_client():
        return mock_client

    monkeypatch.setattr("reaper_mcp.osc_client.get_reaper_client", mock_get_client)
    monkeypatch.setattr(
        "reaper_mcp.osc_client.ensure_connected", AsyncMock(return_value=True)
    )
    return mock_client


@pytest.fixture
def mcp_server(mock_osc_client):
    """Create a FastMCP server instance with mocked dependencies."""
    os.environ["REAPER_TOOL_MODE"] = "portmanteau"
    # Re-call create_server to get the configured mcp instance
    return server.create_server()
