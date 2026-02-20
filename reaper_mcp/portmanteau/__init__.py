"""
Reaper-MCP Portmanteau Tools

Consolidates 21 individual tools into 4 unified portmanteau interfaces.
Follows FastMCP 2.13+ best practices for feature-rich MCP servers.

PORTMANTEAU TOOLS (4 total):
1. reaper_transport - Play/stop/pause/record/position/status
2. reaper_tracks - Get/info/mute/solo/arm/bulk operations
3. reaper_project - Info/save/markers/render/stats
4. reaper_system - Status/help/capabilities
5. reaper_reascript - Run/Setup/Docs for Python ReaScript

BENEFITS:
- 21 tools → 4 tools (81% reduction)
- Better UX with grouped operations
- Easier discovery by category
- AI-friendly comprehensive docstrings
"""

from .transport import setup_transport_portmanteau
from .tracks import setup_tracks_portmanteau
from .project import setup_project_portmanteau
from .system import setup_system_portmanteau
from .reascript import setup_reascript_portmanteau


def setup_all_portmanteau_tools(mcp):
    """Register all portmanteau tools with the MCP server."""
    setup_transport_portmanteau(mcp)
    setup_tracks_portmanteau(mcp)
    setup_project_portmanteau(mcp)
    setup_system_portmanteau(mcp)
    setup_reascript_portmanteau(mcp)


__all__ = [
    "setup_all_portmanteau_tools",
    "setup_transport_portmanteau",
    "setup_tracks_portmanteau",
    "setup_project_portmanteau",
    "setup_system_portmanteau",
    "setup_reascript_portmanteau",
]
