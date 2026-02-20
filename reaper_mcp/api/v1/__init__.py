from fastapi import APIRouter
from reaper_mcp.api.v1.endpoints import tools

api_router = APIRouter()
api_router.include_router(tools.router)
