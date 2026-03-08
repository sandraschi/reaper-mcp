"""
ReaScript Portmanteau Tool
"""

from typing import Literal

from fastmcp import FastMCP

try:
    import reapy
    import reapy.reascript_api as RPR  # noqa: N812 (RPR is ReaScript convention)

    REAPY_AVAILABLE = True
except ImportError:
    REAPY_AVAILABLE = False


def setup_reascript_portmanteau(mcp: FastMCP):
    """Register the consolidated reaper_reascript tool."""

    @mcp.tool()
    def reaper_reascript(
        operation: Literal["run", "setup", "api_help"],
        code: str | None = None,
        function_name: str | None = None,
    ) -> str:
        """
        Unified ReaScript operations for Reaper DAW.

        Operations:
        - run: Execute Python code in Reaper (requires 'code')
        - setup: Configure Reaper for reapy usage (run once)
        - api_help: Get docstring for Reaper API function (requires 'function_name')

        Args:
            operation: Action to perform
            code: Python code to execute (for 'run')
            function_name: API function name to look up (for 'api_help')
        """
        if not REAPY_AVAILABLE:
            return "Error: reapy-boost is not installed."

        if operation == "setup":
            try:
                reapy.configure_reaper()
                return "Reaper configuration initiated. Restart Reaper to apply changes."
            except Exception as e:
                return f"Error configuring reapy: {e}"

        elif operation == "run":
            if not code:
                return "Error: 'code' argument required for 'run' operation."
            try:
                # Execute
                local_scope = {"reapy": reapy}
                # Inject RPR functions
                local_scope.update({k: v for k, v in RPR.__dict__.items() if k.startswith("RPR_")})
                local_scope["RPR"] = RPR

                exec(code, local_scope)  # noqa: S102 (intentional ReaScript execution)

                # Check for structured result
                if "_result" in local_scope:
                    import json

                    try:
                        return json.dumps(local_scope["_result"], indent=2)
                    except Exception as e:
                        return f"Error serializing _result: {e}"

                return "Code executed successfully."
            except Exception as e:
                return f"Error executing ReaScript: {e}"

        elif operation == "api_help":
            if not function_name:
                return "Error: 'function_name' argument required for 'api_help' operation."

            target = function_name
            if not target.startswith("RPR_") and hasattr(RPR, "RPR_" + target):
                target = "RPR_" + target

            if hasattr(RPR, target):
                return f"{target}: {getattr(RPR, target).__doc__}"
            else:
                return f"Function '{function_name}' not found."

        return f"Unknown operation: {operation}"
