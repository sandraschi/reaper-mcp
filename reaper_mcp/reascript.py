"""
ReaScript integration for Reaper MCP using reapy-boost.
Allows executing Python code directly within Reaper's environment.
"""

import logging

from fastmcp import FastMCP

# Try to import reapy, handle failure gracefully if not installed/configured
try:
    import reapy

    REAPY_AVAILABLE = True
except ImportError:
    REAPY_AVAILABLE = False

logger = logging.getLogger(__name__)


def register_reascript_tools(mcp: FastMCP):
    """Register ReaScript-related tools with the MCP server."""

    @mcp.tool()
    def setup_reapy() -> str:
        """
        Configure Reaper to work with reapy-boost.

        This tool attempts to automatically configure Reaper to accept external Python API calls.
        It must be run once before 'run_reascript' can work.

        Returns:
            Status message indicating success or failure.
        """
        if not REAPY_AVAILABLE:
            return "Error: reapy-boost is not installed in the python environment."

        try:
            # Check if already configured (this is a heuristic, reapy doesn't have a simple is_configured check)
            # We'll just run the configuration function which usually handles idempotency or errors if Reaper isn't running
            reapy.configure_reaper()
            return (
                "Reaper configuration for reapy initiated. \n"
                "Please restart Reaper if it was already running to ensure changes take effect.\n"
                "If Reaper was not running, open it now."
            )
        except Exception as e:
            return f"Error configuring reapy: {e!s}. Make sure Reaper is installed."

    @mcp.tool()
    def run_reascript(code: str) -> str:
        """
        Execute arbitrary Python code inside Reaper using ReaScript/reapy.

        The code runs in a context where 'reapy' is imported as 'reapy' and 'RPR' is available.
        This allows full access to the Reaper API.

        Args:
            code: The Python code to execute.
                  Example: 'RPR_ShowConsoleMsg("Hello world")'
                  Example: 'project = reapy.Project.today(); project.add_track()'

        Returns:
            String output/result of the execution or error message.
        """
        if not REAPY_AVAILABLE:
            return "Error: reapy-boost is not installed."

        try:
            # We use reapy.inside_reaper() context manager if we were running a script FROM reaper,
            # but here we are connecting from OUTSIDE.
            # reapy automatically handles the connection if configured.

            # However, reapy's architecture is complex. standard usage from outside is:
            # import reapy
            # p = reapy.Project()
            # ...

            # To execute arbitrary string code effectively, we might need `exec`.
            # But reapy objects are proxies.

            # Let's wrap the execution in a safe dictionary
            local_scope = {"reapy": reapy}

            # We also want to expose the raw Reaper API functions (RPR_*)
            # reapy.reascript_api contains these
            import reapy.reascript_api as RPR

            local_scope.update({k: v for k, v in RPR.__dict__.items() if k.startswith("RPR_")})
            local_scope["RPR"] = RPR

            # Execute the code
            exec(code, local_scope)

            return "Code executed successfully."

        except Exception as e:
            logger.error(f"ReaScript execution failed: {e}")
            return f"Error executing ReaScript: {e!s}"

    @mcp.tool()
    def get_reascript_api_docs(function_name: str = "") -> str:
        """
        Get documentation or signature for a Reaper API function.

        Args:
            function_name: Name of the function to look up (e.g. "GetCursorPosition")

        Returns:
            Docstring or help text.
        """
        if not REAPY_AVAILABLE:
            return "reapy-boost not installed."

        try:
            import reapy.reascript_api as RPR

            if not function_name:
                return "Provide a function name to look up. Common ones: RPR_GetCursorPosition, RPR_AddMediaItemToTrack"

            # Handle RPR_ prefix optionally
            target = function_name
            if not target.startswith("RPR_") and hasattr(RPR, "RPR_" + target):
                target = "RPR_" + target

            if hasattr(RPR, target):
                func = getattr(RPR, target)
                return f"{target}: {func.__doc__}"
            else:
                return f"Function '{function_name}' not found in ReaScript API."

        except Exception as e:
            return f"Error looking up API: {e}"
