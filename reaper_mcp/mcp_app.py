"""
FastMCP 3.1 application for Reaper MCP.

Single MCP instance: tools (portmanteau), prompts, optional skills provider.
Used for stdio (__main__), HTTP mount (api/main.py), and REST tool listing.
"""

from pathlib import Path

from fastmcp import FastMCP

from reaper_mcp.portmanteau import setup_all_portmanteau_tools
from reaper_mcp.prompts import register_prompts

MCP_INSTRUCTIONS = """You are ReaperMCP, a FastMCP 3.1 server for Reaper DAW automation.

FASTMCP 3.1 FEATURES:
- Conversational (dialogic) tool returns for natural AI interaction
- Sampling and agentic workflows: chain transport, tracks, project, and system tools for multi-step sessions
- Prompts: use registered prompts for session templates (record, mix, export)
- Skills: optional skills provider exposes Reaper workflows as MCP resources

CORE CAPABILITIES:
- Transport: play, stop, pause, record, position, status
- Tracks: list, info, mute, solo, arm, count, bulk operations
- Project: info, save, markers, render, stats
- System: status, help, capabilities; start Reaper
- ReaScript: run Python in Reaper, setup reapy, API help

AGENTIC WORKFLOWS:
- Chain tools (e.g. reaper_system status -> reaper_transport play -> reaper_tracks list)
- Use sampling so the model can orchestrate record, edit, export in one flow
- All tools return success, message, and structured data for chaining

RESPONSE FORMAT:
- Dict with success, message; errors include error field
- Success includes relevant data and natural language summaries

PORTMANTEAU DESIGN:
Tools are consolidated; each supports multiple operations via an operation parameter.
"""


def create_mcp() -> FastMCP:
    """Create and configure the FastMCP 3.1 instance."""
    mcp = FastMCP(
        "ReaperMCP",
        instructions=MCP_INSTRUCTIONS,
    )
    setup_all_portmanteau_tools(mcp)
    register_prompts(mcp)

    # Optional: expose skills directory as MCP resources (Reaper workflow skills)
    try:
        from fastmcp.server.providers.skills import SkillsDirectoryProvider

        skills_root = Path(__file__).resolve().parent / "skills"
        if skills_root.is_dir():
            mcp.add_provider(SkillsDirectoryProvider(roots=[skills_root]))
    except ImportError:
        pass

    return mcp


# Singleton used by server, API, and __main__
mcp = create_mcp()
