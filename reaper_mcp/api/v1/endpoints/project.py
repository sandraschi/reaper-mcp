"""REST project hooks for cross-app workflows (e.g. SongGeneration-MCP drop import)."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["project"], prefix="/project")


@router.post("/import_media")
async def import_media(
    file_path: str = Query(..., description="Absolute path to audio under the Reaper drop folder"),
) -> dict[str, object]:
    """Confirm media exists after SongGeneration-MCP copies into the drop directory.

    Returns success when the file is present on disk. DAW insertion via ReaScript/OSC can be layered later.
    """
    p = Path(file_path)
    if not p.is_file():
        raise HTTPException(status_code=404, detail=f"file not found: {file_path}")
    return {"success": True, "imported": True, "path": str(p.resolve())}
