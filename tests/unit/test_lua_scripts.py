"""Unit tests for Lua script CRUD + run (reaper_reascript lua_* ops)."""

import json

import pytest

from reaper_mcp.portmanteau import reascript as rs_mod
from tests.tool_helpers import tool_payload


@pytest.fixture
def lua_dir(tmp_path, monkeypatch):
    target = tmp_path / "lua_scripts"
    monkeypatch.setattr(rs_mod, "LUA_DIR", target)
    return target


def _op_result(payload):
    """Str-returning ops arrive wrapped as {"result": "<json>"} - unwrap one level."""
    if isinstance(payload, dict) and isinstance(payload.get("result"), str):
        return json.loads(payload["result"])
    return payload


def test_lua_crud_roundtrip(lua_dir):
    assert rs_mod.lua_save_script("hello.lua", 'reaper.ShowConsoleMsg("hi\\n")')["success"] is True
    assert rs_mod.lua_list_scripts() == ["hello.lua"]
    got = rs_mod.lua_get_script("hello.lua")
    assert got["success"] is True
    assert "ShowConsoleMsg" in got["code"]
    assert rs_mod.lua_delete_script("hello.lua")["success"] is True
    assert rs_mod.lua_list_scripts() == []


def test_lua_validation(lua_dir):
    for bad in (None, "", "../evil.lua", "sub/dir.lua", "notes.txt", "  "):
        assert rs_mod.lua_get_script(bad)["success"] is False
        assert rs_mod.lua_delete_script(bad)["success"] is False
    assert rs_mod.lua_save_script("empty.lua", "   ")["success"] is False
    assert rs_mod.lua_get_script("missing.lua")["success"] is False
    assert "nothing deleted" in rs_mod.lua_delete_script("missing.lua")["error"]


def test_lua_run_without_reaper(lua_dir):
    rs_mod.lua_save_script("runme.lua", "-- test")
    out = rs_mod.lua_run_script("runme.lua")
    assert out["success"] is False
    assert "REAPER" in out["error"]
    assert rs_mod.lua_run_script("ghost.lua")["success"] is False


def test_lua_run_mocked_success(lua_dir, monkeypatch):
    rs_mod.lua_save_script("runme.lua", "-- test")
    calls = {}

    class FakeRPR:
        def RPR_AddRemoveReaScript(self, add, section, path, commit):
            calls["registered"] = path
            return 4242

        def RPR_Main_OnCommandEx(self, cmd, flag, other):
            calls["invoked"] = cmd

    monkeypatch.setattr(rs_mod, "REAPY_AVAILABLE", True)
    monkeypatch.setattr(rs_mod, "RPR", FakeRPR())
    out = rs_mod.lua_run_script("runme.lua")
    assert out["success"] is True
    assert out["command_id"] == 4242
    assert calls["invoked"] == 4242
    assert calls["registered"].endswith("runme.lua")


def test_lua_run_mocked_drift(lua_dir, monkeypatch):
    rs_mod.lua_save_script("runme.lua", "-- test")
    monkeypatch.setattr(rs_mod, "REAPY_AVAILABLE", True)
    monkeypatch.setattr(rs_mod, "RPR", object())
    out = rs_mod.lua_run_script("runme.lua")
    assert out["success"] is False
    assert "drift" in out["error"]


@pytest.mark.asyncio
async def test_lua_ops_through_mcp(mcp_server, lua_dir):
    payload = _op_result(
        tool_payload(await mcp_server.call_tool("reaper_reascript", arguments={"operation": "lua_list"}))
    )
    assert payload == []
    saved = _op_result(
        tool_payload(
            await mcp_server.call_tool(
                "reaper_reascript",
                arguments={"operation": "lua_save", "script_name": "mcp.lua", "code": "-- via mcp"},
            )
        )
    )
    assert saved["success"] is True
    payload = _op_result(
        tool_payload(await mcp_server.call_tool("reaper_reascript", arguments={"operation": "lua_list"}))
    )
    assert payload == ["mcp.lua"]


@pytest.mark.asyncio
async def test_reascript_tool_lists_lua_ops(mcp_server):
    tools = await mcp_server.list_tools()
    reascript = next(t for t in tools if t.name == "reaper_reascript")
    schema = reascript.parameters
    assert "lua_run" in schema["properties"]["operation"]["enum"]
    assert "script_name" in schema["properties"]
