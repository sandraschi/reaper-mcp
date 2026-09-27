"""
ReaScript Portmanteau Tool (Python exec + Lua script CRUD).
"""

import json
import logging
from pathlib import Path
from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from pydantic import Field

try:
    import reapy
    import reapy.reascript_api as RPR

    REAPY_AVAILABLE = True
except ImportError:
    reapy = None  # type: ignore[assignment]
    RPR = None  # type: ignore[assignment]
    REAPY_AVAILABLE = False

logger = logging.getLogger(__name__)

LUA_DIR = Path(__file__).resolve().parents[2] / "data" / "lua_scripts"


def _lua_script_path(name: str | None) -> Path | None:
    """Validate a plain *.lua filename and resolve it inside the script library."""
    clean = (name or "").strip()
    if not clean or "/" in clean or "\\" in clean or not clean.endswith(".lua"):
        return None
    return LUA_DIR / clean


def lua_list_scripts() -> list[str]:
    LUA_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(p.name for p in LUA_DIR.glob("*.lua"))


def lua_get_script(name: str | None) -> dict[str, Any]:
    path = _lua_script_path(name)
    if path is None:
        return {"success": False, "error": "script_name must be a plain *.lua filename."}
    if not path.exists():
        return {"success": False, "error": f"{path.name} not found."}
    return {"success": True, "name": path.name, "code": path.read_text(encoding="utf-8")}


def lua_save_script(name: str | None, code: str | None) -> dict[str, Any]:
    path = _lua_script_path(name)
    if path is None:
        return {"success": False, "error": "script_name must be a plain *.lua filename."}
    if not (code or "").strip():
        return {"success": False, "error": "code is required."}
    LUA_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(code, encoding="utf-8")
    return {"success": True, "message": f"Saved {path.name}.", "name": path.name}


def lua_delete_script(name: str | None) -> dict[str, Any]:
    path = _lua_script_path(name)
    if path is None:
        return {"success": False, "error": "script_name must be a plain *.lua filename."}
    if not path.exists():
        return {"success": False, "error": f"{path.name} not found - nothing deleted."}
    path.unlink()
    return {"success": True, "message": f"Deleted {path.name}.", "name": path.name}


def lua_run_script(name: str | None) -> dict[str, Any]:
    """Register a library script with REAPER and invoke it (needs reapy + running REAPER)."""
    path = _lua_script_path(name)
    if path is None:
        return {"success": False, "error": "script_name must be a plain *.lua filename."}
    if not path.exists():
        return {"success": False, "error": f"{path.name} not found."}
    if not REAPY_AVAILABLE or RPR is None:
        return {"success": False, "error": "lua_run needs reapy-boost and a running REAPER (CRUD works without)."}
    for func in ("AddRemoveReaScript", "Main_OnCommandEx"):
        if not hasattr(RPR, "RPR_" + func):
            return {"success": False, "error": f"RPR_{func} missing from reapy API (drift?)."}
    try:
        cmd_id = RPR.RPR_AddRemoveReaScript(True, 0, str(path), True)
        if not cmd_id:
            return {"success": False, "error": "REAPER refused to register the script."}
        RPR.RPR_Main_OnCommandEx(cmd_id, 0, 0)
        return {"success": True, "message": f"Executed {path.name} (cmd {cmd_id}).", "command_id": cmd_id}
    except Exception as e:
        logger.exception("Lua script run failed")
        return {"success": False, "error": f"Error running Lua script: {e}"}


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


LuaOp = Literal[
    "run",
    "setup",
    "api_help",
    "lua_list",
    "lua_get",
    "lua_save",
    "lua_delete",
    "lua_run",
]


def setup_reascript_portmanteau(mcp: FastMCP):
    """Register the consolidated reaper_reascript tool."""

    @mcp.tool()
    def reaper_reascript(
        operation: Annotated[
            LuaOp,
            Field(description="Operation: run, setup, api_help, lua_list, lua_get, lua_save, lua_delete, lua_run"),
        ],
        code: Annotated[str | None, Field(description="Python code for 'run', Lua source for 'lua_save'")] = None,
        function_name: Annotated[str | None, Field(description="API function name (for 'api_help' op)")] = None,
        script_name: Annotated[
            str | None, Field(description="Plain *.lua filename (for lua_get, lua_save, lua_delete, lua_run)")
        ] = None,
    ) -> str:
        """
        Unified ReaScript operations for Reaper DAW.

        [RATIONALE]
        Consolidates ReaScript execution, setup, API help, and Lua script CRUD
        into one tool to keep the tool registry lean.

        Operations:
        - run: Execute Python code in Reaper (requires 'code')
        - setup: Configure Reaper for reapy usage (run once)
        - api_help: Get docstring for Reaper API function (requires 'function_name')
        - lua_list: List saved Lua scripts (no args)
        - lua_get: Read a Lua script (requires 'script_name')
        - lua_save: Create/update a Lua script (requires 'script_name' + 'code')
        - lua_delete: Delete a Lua script (requires 'script_name')
        - lua_run: Register + execute a Lua script in REAPER
          (requires 'script_name', reapy + running REAPER; CRUD works without)

        ## Return Format
        str — JSON-formatted result for 'run', success/error message otherwise.

        ## Examples
        reaper_reascript(operation="run", code='RPR_ShowConsoleMsg("hello")')
        reaper_reascript(operation="api_help", function_name="RPR_CountTracks")
        reaper_reascript(operation="lua_save", script_name="hello.lua", code='reaper.ShowConsoleMsg("hi\\n")')
        reaper_reascript(operation="lua_run", script_name="hello.lua")
        """
        if operation == "lua_list":
            return json.dumps(lua_list_scripts(), indent=2)

        elif operation == "lua_get":
            return json.dumps(lua_get_script(script_name), indent=2)

        elif operation == "lua_save":
            return json.dumps(lua_save_script(script_name, code), indent=2)

        elif operation == "lua_delete":
            return json.dumps(lua_delete_script(script_name), indent=2)

        elif operation == "lua_run":
            out = lua_run_script(script_name)
            if not out.get("success"):
                return f"Error: {out.get('error', 'Unknown error')}"
            return out.get("message", "Lua script executed.")

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
