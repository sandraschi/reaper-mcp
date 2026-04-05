from fastapi import APIRouter

from reaper_mcp.api.v1.endpoints import crosslinks, project, tools

api_router = APIRouter()
api_router.include_router(tools.router)
api_router.include_router(crosslinks.router)
api_router.include_router(project.router)
