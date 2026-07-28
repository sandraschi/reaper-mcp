import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Add project root to path
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Mock reapy and pythonosc before any imports
sys.modules["reapy"] = MagicMock()
sys.modules["reapy.core"] = MagicMock()
sys.modules["pythonosc"] = MagicMock()
sys.modules["pythonosc.dispatcher"] = MagicMock()
sys.modules["pythonosc.osc_server"] = MagicMock()
sys.modules["pythonosc.udp_client"] = MagicMock()

import server


class _MockReaperClient:
    host = "127.0.0.1"
    port = 8000
    connected = True
    last_status = {}

    async def get_track_count(self) -> int:
        return 5

    async def get_position(self):
        return {"args": ["0:00:00"]}


@pytest.fixture
def mock_osc_client(monkeypatch):
    """Mock the OSC client to avoid network calls."""
    mock_client = _MockReaperClient()

    async def mock_get_client():
        return mock_client

    monkeypatch.setattr("reaper_mcp.osc_client.get_reaper_client", mock_get_client)
    monkeypatch.setattr("reaper_mcp.portmanteau.tracks.get_reaper_client", mock_get_client)
    monkeypatch.setattr("reaper_mcp.portmanteau.transport.get_reaper_client", mock_get_client)
    ens = AsyncMock(return_value=True)
    monkeypatch.setattr("reaper_mcp.osc_client.ensure_connected", ens)
    monkeypatch.setattr("reaper_mcp.portmanteau.tracks.ensure_connected", ens)
    monkeypatch.setattr("reaper_mcp.portmanteau.transport.ensure_connected", ens)
    return mock_client


@pytest.fixture
def mcp_server(mock_osc_client):
    """Create a FastMCP server instance with mocked dependencies."""
    os.environ["REAPER_TOOL_MODE"] = "portmanteau"
    return server.create_server()
