"""
Reaper-MCP Portmanteau Tools

Consolidates tools into unified portmanteau interfaces.
FastMCP 3.1 compliant; supports agentic workflows and dialogic returns.

PORTMANTEAU TOOLS:
1. reaper_transport - Play/stop/pause/record/position/status
2. reaper_tracks - Get/info/mute/solo/arm/bulk operations
3. reaper_project - Info/save/markers/render/stats
4. reaper_system - Status/help/capabilities
5. reaper_reascript - Run/Setup/Docs for Python ReaScript
6. reaper_orchestrator - Stem import, FX chain, regions, end-to-end pipeline
7. reaper_audio - Audio relay for piping Reaper output to butterchurn

BENEFITS:
- Portmanteau reduction for IDE tool limits
- Better UX with grouped operations
- Easier discovery by category
- AI-friendly comprehensive docstrings
"""

from .audio import setup_audio_portmanteau
from .orchestrator import setup_orchestrator_portmanteau
from .project import setup_project_portmanteau
from .reascript import setup_reascript_portmanteau
from .system import setup_system_portmanteau
from .tracks import setup_tracks_portmanteau
from .transport import setup_transport_portmanteau


def setup_all_portmanteau_tools(mcp):
    """Register all portmanteau tools with the MCP server."""
    setup_transport_portmanteau(mcp)
    setup_tracks_portmanteau(mcp)
    setup_project_portmanteau(mcp)
    setup_system_portmanteau(mcp)
    setup_reascript_portmanteau(mcp)
    setup_orchestrator_portmanteau(mcp)
    setup_audio_portmanteau(mcp)


__all__ = [
    "setup_all_portmanteau_tools",
    "setup_audio_portmanteau",
    "setup_orchestrator_portmanteau",
    "setup_project_portmanteau",
    "setup_reascript_portmanteau",
    "setup_system_portmanteau",
    "setup_tracks_portmanteau",
    "setup_transport_portmanteau",
]
