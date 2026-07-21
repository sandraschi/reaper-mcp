"""Cross-repo integration API endpoints for ReaperMCP."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["crosslinks"], prefix="/crosslinks")

DEFAULT_REPO_ROOT = Path(os.environ.get("REAPER_CROSSLINK_REPO_ROOT", "D:\\Dev\\repos"))

_crosslink_registry: dict[str, dict[str, Any]] = {}


class RepoLinkRequest(BaseModel):
    repo_name: str
    repo_path: str
    base_url: str | None = None
    mcp_url: str | None = None
    api_base: str | None = None
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None


class RepoLinkInfo(BaseModel):
    repo_name: str
    repo_path: str
    exists: bool
    base_url: str | None = None
    mcp_url: str | None = None
    api_base: str | None = None
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None
    detected_files: list[str] = Field(default_factory=list)


def _collect_detected_files(repo_dir: Path) -> list[str]:
    candidates = [
        "README.md",
        "pyproject.toml",
        "manifest.json",
        "glama.json",
        "server.py",
        "start.ps1",
    ]
    found: list[str] = []
    for candidate in candidates:
        path = repo_dir / candidate
        if path.exists():
            found.append(candidate)
    return found


def _discover_repo(repo_name: str) -> RepoLinkInfo | None:
    repo_dir = DEFAULT_REPO_ROOT / repo_name
    if not repo_dir.exists() or not repo_dir.is_dir():
        return None
    return RepoLinkInfo(
        repo_name=repo_name,
        repo_path=str(repo_dir),
        exists=True,
        detected_files=_collect_detected_files(repo_dir),
    )


def _normalize_repo_info(raw: dict[str, Any]) -> RepoLinkInfo:
    repo_path = Path(raw["repo_path"])
    return RepoLinkInfo(
        repo_name=raw["repo_name"],
        repo_path=str(repo_path),
        exists=repo_path.exists() and repo_path.is_dir(),
        base_url=raw.get("base_url"),
        mcp_url=raw.get("mcp_url"),
        api_base=raw.get("api_base"),
        tags=list(raw.get("tags", [])),
        notes=raw.get("notes"),
        detected_files=_collect_detected_files(repo_path) if repo_path.exists() and repo_path.is_dir() else [],
    )


@router.get("/health")
async def crosslinks_health() -> dict[str, Any]:
    """Return crosslink API operational status and registry stats."""
    return {
        "success": True,
        "service": "crosslinks",
        "repo_root": str(DEFAULT_REPO_ROOT),
        "repo_root_exists": DEFAULT_REPO_ROOT.exists(),
        "registered_repos": len(_crosslink_registry),
    }


@router.get("/repos", response_model=list[RepoLinkInfo])
async def list_crosslinked_repos(
    include_discovered: bool = Query(
        default=True,
        description="Include repo folders auto-discovered under REAPER_CROSSLINK_REPO_ROOT",
    ),
) -> list[RepoLinkInfo]:
    """List explicitly registered repos and optionally discovered repo folders."""
    links: dict[str, RepoLinkInfo] = {name: _normalize_repo_info(raw) for name, raw in _crosslink_registry.items()}

    if include_discovered and DEFAULT_REPO_ROOT.exists() and DEFAULT_REPO_ROOT.is_dir():
        for repo_dir in DEFAULT_REPO_ROOT.iterdir():
            if not repo_dir.is_dir():
                continue
            if repo_dir.name.startswith("."):
                continue
            if repo_dir.name not in links:
                discovered = _discover_repo(repo_dir.name)
                if discovered:
                    links[repo_dir.name] = discovered

    return sorted(links.values(), key=lambda item: item.repo_name.lower())


@router.post("/repos", response_model=RepoLinkInfo)
async def register_crosslinked_repo(payload: RepoLinkRequest) -> RepoLinkInfo:
    """Register metadata for an external repo to integrate with ReaperMCP."""
    repo_name = payload.repo_name.strip()
    if not repo_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="repo_name is required",
        )

    repo_path = Path(payload.repo_path)
    _crosslink_registry[repo_name] = {
        "repo_name": repo_name,
        "repo_path": str(repo_path),
        "base_url": payload.base_url,
        "mcp_url": payload.mcp_url,
        "api_base": payload.api_base,
        "tags": payload.tags,
        "notes": payload.notes,
    }
    return _normalize_repo_info(_crosslink_registry[repo_name])


@router.get("/repos/{repo_name}", response_model=RepoLinkInfo)
async def get_crosslinked_repo(repo_name: str) -> RepoLinkInfo:
    """Get one crosslinked repo by name (registered first, then discovered fallback)."""
    if repo_name in _crosslink_registry:
        return _normalize_repo_info(_crosslink_registry[repo_name])

    discovered = _discover_repo(repo_name)
    if discovered:
        return discovered

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Repo '{repo_name}' not found in registry or discovery",
    )


@router.get("/repos/{repo_name}/endpoints")
async def get_repo_endpoint_templates(repo_name: str) -> dict[str, Any]:
    """Return endpoint templates and payload contracts for cross-repo integrations."""
    repo = await get_crosslinked_repo(repo_name)
    safe_repo_name = repo.repo_name
    return {
        "success": True,
        "repo": repo.model_dump(),
        "templates": {
            "reaper_tools_list": {
                "method": "GET",
                "url": "/api/v1/tools/",
            },
            "reaper_tool_call": {
                "method": "POST",
                "url": "/api/v1/tools/call",
                "body": {
                    "name": "reaper_orchestrator",
                    "arguments": {
                        "operation": "full_pipeline",
                        "stems_folder": f"D:\\media\\{safe_repo_name}\\output",
                        "vibe": "classical_master",
                        "regions_text": "[verse] 00:12-00:42 [chorus] 00:42-01:08",
                    },
                },
            },
            "crosslinks_repo_get": {
                "method": "GET",
                "url": f"/api/v1/crosslinks/repos/{safe_repo_name}",
            },
            "crosslinks_repo_register": {
                "method": "POST",
                "url": "/api/v1/crosslinks/repos",
                "body": {
                    "repo_name": safe_repo_name,
                    "repo_path": repo.repo_path,
                    "api_base": repo.api_base,
                    "mcp_url": repo.mcp_url,
                    "tags": repo.tags,
                },
            },
        },
    }


@router.get("/search")
async def search_crosslinks(
    q: str = Query(..., min_length=1, description="Search by repo name, tag, or notes"),
) -> dict[str, Any]:
    """Search registry by name, tags, and notes content."""
    query = q.lower().strip()
    matches: list[RepoLinkInfo] = []
    for repo_name, raw in _crosslink_registry.items():
        name_match = query in repo_name.lower()
        tags = [str(tag).lower() for tag in raw.get("tags", [])]
        notes = str(raw.get("notes", "")).lower()
        if name_match or any(query in tag for tag in tags) or query in notes:
            matches.append(_normalize_repo_info(raw))

    return {
        "success": True,
        "query": q,
        "count": len(matches),
        "results": [item.model_dump() for item in matches],
    }
