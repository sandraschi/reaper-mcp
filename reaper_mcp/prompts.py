"""
Reaper MCP prompt templates (FastMCP 3.1).

Registered with the MCP server for session templates and agentic workflows.
"""

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register all prompt templates with the FastMCP server."""

    @mcp.prompt()
    def reaper_record_session() -> str:
        """Prepare for a recording session: check transport, tracks armed, levels."""
        return """Prepare for a Reaper recording session. Check transport status, ensure tracks that need to be recorded are armed, and suggest level checks. Use reaper_system status, reaper_transport status, and reaper_tracks as needed. Summarize what is ready and what to fix before recording."""

    @mcp.prompt()
    def reaper_mix_session() -> str:
        """Guide a mixing pass: balance tracks, suggest automation, export stems."""
        return """Guide a mixing pass in Reaper. Suggest track balance order, key automation moves, and when to use reaper_tracks for mute/solo to A/B. Include when to use reaper_project render for stems or final bounce."""

    @mcp.prompt()
    def reaper_export_project() -> str:
        """Export or render the current project with format and quality options."""
        return """Help export the current Reaper project. Use reaper_project with operation render. Consider format (wav, mp3), quality, and bounds (project, time selection). Suggest settings and run the render."""

    @mcp.prompt()
    def reaper_transport_control() -> str:
        """Control transport: play, stop, pause, record, or report position."""
        return """Control Reaper transport. Use reaper_transport with operation play, stop, pause, record, position, or status as needed. Confirm state after each change."""

    @mcp.prompt()
    def reaper_track_operations() -> str:
        """List tracks, mute/solo/arm, or run bulk operations on multiple tracks."""
        return """Work with Reaper tracks. Use reaper_tracks to list tracks, get info, or set mute/solo/arm. For bulk changes use operation bulk with track_ids and bulk_operation."""

    @mcp.prompt()
    def reaper_project_help() -> str:
        """Get project info, save, add markers, or view project stats."""
        return """Help with Reaper project: info, save, markers, or stats. Use reaper_project with the appropriate operation. For markers provide position and name if needed."""

    @mcp.prompt()
    def reaper_system_help() -> str:
        """Check Reaper connection, list capabilities, or get help on tools."""
        return """Check Reaper MCP system: connection status, capabilities, or tool help. Use reaper_system with operation status, capabilities, or help. Optionally pass category or tool_name for targeted help."""
