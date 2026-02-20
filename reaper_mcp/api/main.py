"""Main entry point for Reaper-MCP FastAPI server."""

import uvicorn
import os
import sys

# Add current directory to sys.path to allow importing from server.py in root
sys.path.append(os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reaper_mcp.api import api_router

app = FastAPI(
    title="Reaper-MCP API",
    description="REST interface for Reaper-MCP tools",
    version="1.0.0",
)

# Enable CORS for the webapp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10793)
