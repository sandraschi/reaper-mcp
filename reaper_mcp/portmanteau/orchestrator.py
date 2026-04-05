"""
reaper_orchestrator - High-level production workflows for Reaper.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any

from .reascript import execute_reascript_code

logger = logging.getLogger(__name__)

VIBE_FX_CHAINS: dict[str, str] = {
    "classical_master": "Classical_Master.RfxChain",
    "dark_techno": "Dark_Techno.RfxChain",
}


def _escape_for_python_string(value: str) -> str:
    """Escape a string for safe embedding into generated Python code."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _parse_timestamp_to_seconds(value: str) -> float | None:
    """Parse s, mm:ss, or hh:mm:ss values into seconds."""
    token = value.strip()
    if not token:
        return None
    try:
        if ":" not in token:
            parsed = float(token)
            return parsed if parsed >= 0 else None
        parts = token.split(":")
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), float(parts[1])
            total = minutes * 60 + seconds
            return total if total >= 0 else None
        if len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), float(parts[2])
            total = hours * 3600 + minutes * 60 + seconds
            return total if total >= 0 else None
        return None
    except ValueError:
        return None


def _normalize_regions(raw_regions: str | list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize region input into [{name, start_seconds, end_seconds}]."""
    if isinstance(raw_regions, list):
        normalized: list[dict[str, Any]] = []
        for region in raw_regions:
            name = str(region.get("name", "")).strip()
            start_value = region.get("start")
            end_value = region.get("end")
            if not name:
                continue
            start = (
                float(start_value)
                if isinstance(start_value, int | float)
                else _parse_timestamp_to_seconds(str(start_value))
            )
            end = (
                float(end_value)
                if isinstance(end_value, int | float)
                else _parse_timestamp_to_seconds(str(end_value))
            )
            if start is None or end is None or end <= start:
                continue
            normalized.append(
                {"name": name, "start_seconds": start, "end_seconds": end}
            )
        return normalized

    regions: list[dict[str, Any]] = []
    pattern = re.compile(
        r"\[(?P<name>[^\]]+)\]\s*(?P<start>\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?|\d+(?:\.\d+)?)\s*-\s*(?P<end>\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?|\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(raw_regions):
        name = match.group("name").strip()
        start = _parse_timestamp_to_seconds(match.group("start"))
        end = _parse_timestamp_to_seconds(match.group("end"))
        if start is None or end is None or end <= start:
            continue
        regions.append({"name": name, "start_seconds": start, "end_seconds": end})
    return regions


def _build_stem_import_script(stems: list[dict[str, str]]) -> str:
    stems_json = json.dumps(stems)
    return f"""
import json
stems = json.loads('''{stems_json}''')
inserted = []
for stem in stems:
    file_path = stem["path"]
    track_name = stem["track_name"]
    track_index = int(RPR_CountTracks(0))
    RPR_InsertTrackAtIndex(track_index, True)
    track = RPR_GetTrack(0, track_index)
    RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR_SetOnlyTrackSelected(track)
    RPR_InsertMedia(file_path, 0)
    inserted.append({{"track_index": track_index + 1, "track_name": track_name, "path": file_path}})
_result = {{"operation": "stem_import", "inserted": inserted, "inserted_count": len(inserted)}}
"""


def _build_fx_chain_script(track_name: str, fx_chain_path: str) -> str:
    escaped_track_name = _escape_for_python_string(track_name)
    escaped_fx_chain_path = _escape_for_python_string(fx_chain_path)
    return f"""
target_name = "{escaped_track_name}"
fx_chain_path = "{escaped_fx_chain_path}"
track_count = int(RPR_CountTracks(0))
applied = False
load_result = -1
for idx in range(track_count):
    track = RPR_GetTrack(0, idx)
    _, _, name, _ = RPR_GetTrackName(track, "", 512)
    if name == target_name:
        load_result = RPR_TrackFX_AddByName(track, "FXCHAIN:" + fx_chain_path, False, -1)
        applied = load_result >= 0
        break
_result = {{
    "operation": "fx_chain",
    "track_name": target_name,
    "fx_chain_path": fx_chain_path,
    "applied": applied,
    "load_result": load_result,
}}
"""


def _build_regions_script(regions: list[dict[str, Any]]) -> str:
    regions_json = json.dumps(regions)
    return f"""
import json
regions = json.loads('''{regions_json}''')
created = []
for region in regions:
    name = region["name"]
    start = float(region["start_seconds"])
    end = float(region["end_seconds"])
    RPR_AddProjectMarker2(0, True, start, end, name, -1, 0)
    created.append({{"name": name, "start_seconds": start, "end_seconds": end}})
_result = {{"operation": "regions", "created": created, "count": len(created)}}
"""


def setup_orchestrator_portmanteau(mcp):
    """Register high-level orchestration operations for stem-to-mix workflows."""

    @mcp.tool()
    async def reaper_orchestrator(
        operation: str,
        stems_folder: str | None = None,
        vibe: str | None = None,
        fx_chain_path: str | None = None,
        target_track_name: str = "inst",
        regions_text: str | None = None,
        regions: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """High-level Reaper orchestration for stem ingest, FX chain assignment, and regions.

        OPERATIONS:
        - stem_import: Import SG2 stems (`vocal.wav`, `inst.wav`) as tracks
        - fx_chain: Apply a vibe-mapped or explicit .RfxChain to target track
        - regions: Create REAPER regions from SG2 timestamp metadata
        - full_pipeline: Run stem_import, fx_chain, and regions sequentially
        """
        valid_ops = ["stem_import", "fx_chain", "regions", "full_pipeline"]
        if operation not in valid_ops:
            return {
                "success": False,
                "error": f"Invalid operation: {operation}",
                "valid_operations": valid_ops,
            }

        try:
            if operation in ["stem_import", "full_pipeline"]:
                if not stems_folder:
                    return {"success": False, "error": "stems_folder is required"}
                base = Path(stems_folder)
                stem_specs = [
                    {"filename": "vocal.wav", "track_name": "vocal"},
                    {"filename": "inst.wav", "track_name": "inst"},
                ]
                stems_to_import: list[dict[str, str]] = []
                missing: list[str] = []
                for spec in stem_specs:
                    stem_path = base / spec["filename"]
                    if stem_path.exists():
                        stems_to_import.append(
                            {
                                "path": str(stem_path.resolve()),
                                "track_name": spec["track_name"],
                            }
                        )
                    else:
                        missing.append(spec["filename"])
                if not stems_to_import:
                    return {
                        "success": False,
                        "error": "No SG2 stems found in stems_folder",
                        "expected_files": [s["filename"] for s in stem_specs],
                    }

                import_result = execute_reascript_code(
                    _build_stem_import_script(stems_to_import)
                )
                if not import_result.get("success"):
                    return import_result
                if operation == "stem_import":
                    return {
                        "success": True,
                        "operation": "stem_import",
                        "message": "Stem import completed",
                        "missing_files": missing,
                        "details": import_result.get("result", {}),
                    }

            fx_result: dict[str, Any] = {}
            if operation in ["fx_chain", "full_pipeline"]:
                resolved_vibe = (vibe or "").strip().lower()
                chain = fx_chain_path
                if not chain and resolved_vibe:
                    chain = VIBE_FX_CHAINS.get(resolved_vibe)
                if not chain:
                    return {
                        "success": False,
                        "error": "Provide fx_chain_path or known vibe",
                        "known_vibes": sorted(VIBE_FX_CHAINS.keys()),
                    }
                chain_path = Path(chain)
                if not chain_path.is_absolute() and stems_folder:
                    chain_path = Path(stems_folder) / chain
                if not chain_path.exists():
                    return {
                        "success": False,
                        "error": "FX chain file not found",
                        "fx_chain_path": str(chain_path),
                    }
                fx_result = execute_reascript_code(
                    _build_fx_chain_script(target_track_name, str(chain_path.resolve()))
                )
                if not fx_result.get("success"):
                    return fx_result
                if operation == "fx_chain":
                    return {
                        "success": True,
                        "operation": "fx_chain",
                        "message": "FX chain operation completed",
                        "details": fx_result.get("result", {}),
                    }

            regions_result: dict[str, Any] = {}
            if operation in ["regions", "full_pipeline"]:
                resolved_regions = _normalize_regions(
                    regions if regions is not None else (regions_text or "")
                )
                if not resolved_regions:
                    return {
                        "success": False,
                        "error": "No valid regions parsed",
                        "expected_format": "[chorus] 00:45-01:15",
                    }
                regions_result = execute_reascript_code(
                    _build_regions_script(resolved_regions)
                )
                if not regions_result.get("success"):
                    return regions_result
                if operation == "regions":
                    return {
                        "success": True,
                        "operation": "regions",
                        "message": "Region creation completed",
                        "details": regions_result.get("result", {}),
                    }

            return {
                "success": True,
                "operation": "full_pipeline",
                "message": "Stem import, FX chain, and region workflow completed",
                "steps": {
                    "stem_import": import_result.get("result", {}),
                    "fx_chain": fx_result.get("result", {}),
                    "regions": regions_result.get("result", {}),
                },
            }
        except Exception as e:
            logger.error("reaper_orchestrator error: %s", e)
            return {"success": False, "operation": operation, "error": str(e)}

