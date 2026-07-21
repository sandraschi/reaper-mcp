"""Universal Tool API for ReaperMCP (FastMCP 3.1)."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from reaper_mcp.mcp_app import mcp

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tools"], prefix="/tools")


class ToolParameter(BaseModel):
    name: str
    type: str
    description: str | None = None
    required: bool = True


class ToolInfo(BaseModel):
    name: str
    description: str
    parameters: list[ToolParameter] = []


class ToolCallRequest(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


class ToolCallResponse(BaseModel):
    status: str
    result: Any = None
    message: str | None = None


@router.get("/", response_model=list[ToolInfo])
async def list_tools() -> list[ToolInfo]:
    """List all registered MCP tools (FastMCP 3.1 list_tools)."""
    try:
        # FastMCP 3.1: list_tools() returns list of tool objects
        raw = await mcp.list_tools()
        tools_out: list[ToolInfo] = []
        for t in raw:
            params: list[ToolParameter] = []
            schema = getattr(t, "parameters", None) or {}
            props = schema.get("properties", {})
            required_list = schema.get("required", [])
            for p_name, p_info in props.items():
                params.append(
                    ToolParameter(
                        name=p_name,
                        type=p_info.get("type", "string"),
                        description=p_info.get("description"),
                        required=p_name in required_list,
                    )
                )
            tools_out.append(
                ToolInfo(
                    name=t.name,
                    description=getattr(t, "description", None) or "",
                    parameters=params,
                )
            )
        return tools_out
    except Exception as e:
        logger.exception("Error listing tools")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tools: {e!s}",
        ) from e


@router.post("/call", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest) -> ToolCallResponse:
    """Execute a registered MCP tool. Uses MCP protocol path when available."""
    try:
        logger.info("Calling tool via API: %s with args: %s", request.name, request.arguments)
        # FastMCP 3.1: use run_tool if available, else fallback
        if hasattr(mcp, "run_tool"):
            result = await mcp.run_tool(request.name, request.arguments)
        elif hasattr(mcp, "call_tool"):
            result = await mcp.call_tool(request.name, request.arguments)
        else:
            return ToolCallResponse(
                status="error",
                message="Tool execution not available via REST; use MCP client at /mcp",
            )
        return ToolCallResponse(
            status="success",
            result=result,
            message=f"Tool {request.name} executed successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error calling tool %s", request.name)
        return ToolCallResponse(status="error", message=str(e))
