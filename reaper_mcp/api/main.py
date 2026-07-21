"""Main entry point for Reaper-MCP FastAPI server (FastMCP 3.1)."""

import os
import sys

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from reaper_mcp.api import api_router
from reaper_mcp.mcp_app import mcp

app = FastAPI(
    title="Reaper-MCP API",
    description="REST interface for Reaper-MCP tools (FastMCP 3.1)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:10796",
        "http://127.0.0.1:10796",
        "http://localhost:10797",
        "http://127.0.0.1:10797",
        "http://tauri.localhost",
        "https://tauri.localhost",
        "tauri://localhost",
    ],
    allow_origin_regex=r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Mount FastMCP 3.1 HTTP transport at /mcp (streamable HTTP)
app.mount("/mcp", mcp.http_app(path="/"))


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=10793)
