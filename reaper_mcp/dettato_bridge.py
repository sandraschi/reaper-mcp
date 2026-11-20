"""
Bridge to KobiMusic's local `dettato` multi-instrument audio-to-MIDI CLI.

Invokes `dettato` as a subprocess so `reaper-mcp` stays lightweight without
requiring PyTorch inside the MCP server's own virtual environment.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

DEFAULT_DETTATO_CANDIDATES: tuple[Path, ...] = (
    Path(r"D:\Dev\tools\dettato\.venv\Scripts\dettato.exe"),
    Path.home() / ".local" / "bin" / "dettato.exe",
    Path.home() / ".local" / "bin" / "dettato",
)

VALID_DEVICES: frozenset[str] = frozenset({"auto", "cuda", "cpu"})


def resolve_dettato_executable(explicit_bin: str | None = None) -> Path | None:
    """Locate the `dettato` CLI executable."""
    candidates: list[str] = []
    if explicit_bin:
        candidates.append(explicit_bin)
    env_bin = os.environ.get("DETTATO_BIN")
    if env_bin:
        candidates.append(env_bin)

    for raw in candidates:
        candidate = Path(raw)
        if candidate.is_file():
            return candidate

    on_path = shutil.which("dettato")
    if on_path:
        return Path(on_path)

    for fallback in DEFAULT_DETTATO_CANDIDATES:
        if fallback.is_file():
            return fallback

    return None


def dettato_status(explicit_bin: str | None = None) -> dict[str, Any]:
    """Report availability of the local `dettato` CLI, offline weights, and ffmpeg."""
    exe = resolve_dettato_executable(explicit_bin)
    weights_env = os.environ.get("DETTATO_WEIGHTS")
    weights_path = Path(weights_env) if weights_env else None
    ffmpeg_path = shutil.which("ffmpeg")
    return {
        "success": True,
        "available": exe is not None,
        "executable": str(exe) if exe is not None else None,
        "weights_dir": str(weights_path) if weights_path is not None else None,
        "weights_dir_exists": bool(weights_path and weights_path.is_dir()),
        "ffmpeg_available": ffmpeg_path is not None,
        "ffmpeg_path": ffmpeg_path,
    }


def transcribe_audio_to_midi(
    audio_path: str,
    output_dir: str | None = None,
    device: str = "auto",
    timeout_seconds: int = 300,
    explicit_bin: str | None = None,
) -> dict[str, Any]:
    """Run `dettato` on an audio file and return the generated MIDI + JSON metadata."""
    normalized_device = (device or "auto").strip().lower()
    if normalized_device not in VALID_DEVICES:
        return {
            "success": False,
            "error": f"Invalid device '{device}'. Expected one of: {sorted(VALID_DEVICES)}",
        }

    src = Path(audio_path)
    if not src.is_file():
        return {
            "success": False,
            "error": f"Audio file not found: {src}",
        }

    exe = resolve_dettato_executable(explicit_bin)
    if exe is None:
        return {
            "success": False,
            "error": "dettato CLI not found. Set DETTATO_BIN or install into D:\\Dev\\tools\\dettato\\.venv.",
            "install_hint": "uv pip install git+https://github.com/kobimusic/dettato",
        }

    out_dir = Path(output_dir) if output_dir else src.parent / "dettato_out"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [str(exe), str(src.resolve()), "-o", str(out_dir.resolve())]
    if normalized_device in {"cpu", "cuda"}:
        cmd.extend(["--device", normalized_device])

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"dettato timed out after {timeout_seconds}s",
            "command": cmd,
        }
    except OSError as exc:
        return {
            "success": False,
            "error": f"Failed to launch dettato: {exc}",
            "command": cmd,
        }

    elapsed = round(time.monotonic() - start, 2)
    if proc.returncode != 0:
        return {
            "success": False,
            "error": f"dettato exited with code {proc.returncode}",
            "returncode": proc.returncode,
            "stderr": (proc.stderr or "").strip()[-2000:],
            "stdout": (proc.stdout or "").strip()[-2000:],
            "elapsed_seconds": elapsed,
        }

    midi_path = out_dir / f"{src.stem}.mid"
    json_path = out_dir / f"{src.stem}.json"
    if not midi_path.is_file():
        mids = sorted(out_dir.glob("*.mid"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not mids:
            return {
                "success": False,
                "error": f"dettato succeeded but produced no .mid file in {out_dir}",
                "stdout": (proc.stdout or "").strip()[-2000:],
                "elapsed_seconds": elapsed,
            }
        midi_path = mids[0]
        candidate_json = midi_path.with_suffix(".json")
        if candidate_json.is_file():
            json_path = candidate_json

    metadata: dict[str, Any] | None = None
    if json_path.is_file():
        try:
            metadata = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            metadata = None

    return {
        "success": True,
        "audio_path": str(src.resolve()),
        "midi_path": str(midi_path.resolve()),
        "metadata_path": str(json_path.resolve()) if json_path.is_file() else None,
        "metadata": metadata,
        "device": normalized_device,
        "elapsed_seconds": elapsed,
    }
