"""Shared helpers for MCP tool tests."""

from __future__ import annotations

import json
from typing import Any

from fastmcp.tools.base import ToolResult


def tool_payload(result: ToolResult) -> dict[str, Any]:
    if result.structured_content is not None:
        return dict(result.structured_content)
    for block in result.content or []:
        text = getattr(block, "text", None)
        if text:
            return json.loads(text)
    raise AssertionError("ToolResult has no structured_content or JSON text")
