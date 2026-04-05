"""
ReaScript Portmanteau Tool.
"""

import json
from typing import Any, Literal

from fastmcp import FastMCP

try:
    import reapy
    import reapy.reascript_api as RPR  # noqa: N812 (RPR is ReaScript convention)

    REAPY_AVAILABLE = True
except ImportError:
    REAPY_AVAILABLE = False


def execute_reascript_code(code: str) -> dict[str, Any]:
    """Execute Python ReaScript code and return structured output."""
    if not REAPY_AVAILABLE:
        return {"success": False, "error": "reapy-boost is not installed."}

    if not code.strip():
        return {"success": False, "error": "Code is required."}

    try:
        local_scope: dict[str, Any] = {"reapy": reapy}
        local_scope.update({k: v for k, v in RPR.__dict__.items() if k.startswith("RPR_")})
        local_scope["RPR"] = RPR
        exec(code, local_scope)  # noqa: S102 (intentional ReaScript execution)

        raw_result = local_scope.get("_result")
        if raw_result is None:
            return {"success": True, "message": "Code executed successfully."}
        if isinstance(raw_result, dict):
            return {"success": True, "result": raw_result}
        return {"success": True, "result": raw_result}
    except Exception as e:
        return {"success": False, "error": f"Error executing ReaScript: {e}"}


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
            result = execute_reascript_code(code)
            if not result.get("success"):
                return f"Error: {result.get('error', 'Unknown error')}"
            if "result" in result:
                try:
                    return json.dumps(result["result"], indent=2)
                except Exception as e:
                    return f"Error serializing _result: {e}"
            return result.get("message", "Code executed successfully.")

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
