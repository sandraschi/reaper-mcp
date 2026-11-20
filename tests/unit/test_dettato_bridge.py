"""Unit tests for the dettato audio-to-MIDI bridge and orchestrator integration."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from reaper_mcp.dettato_bridge import (
    dettato_status,
    resolve_dettato_executable,
    transcribe_audio_to_midi,
)
from reaper_mcp.portmanteau.orchestrator import _build_midi_import_script, setup_orchestrator_portmanteau


class _DummyMCP:
    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def tool(self):
        def _decorator(fn):
            self.tools[fn.__name__] = fn
            return fn

        return _decorator


def test_resolve_dettato_executable_prefers_explicit_and_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    explicit = tmp_path / "explicit_dettato.exe"
    explicit.write_text("", encoding="utf-8")
    env_bin = tmp_path / "env_dettato.exe"
    env_bin.write_text("", encoding="utf-8")

    monkeypatch.setenv("DETTATO_BIN", str(env_bin))
    assert resolve_dettato_executable(str(explicit)) == explicit
    assert resolve_dettato_executable() == env_bin


def test_dettato_status_reports_env_weights(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_exe = tmp_path / "dettato.exe"
    fake_exe.write_text("", encoding="utf-8")
    weights = tmp_path / "weights"
    weights.mkdir()

    monkeypatch.setenv("DETTATO_BIN", str(fake_exe))
    monkeypatch.setenv("DETTATO_WEIGHTS", str(weights))

    status = dettato_status()
    assert status["success"] is True
    assert status["available"] is True
    assert status["executable"] == str(fake_exe)
    assert status["weights_dir_exists"] is True


def test_transcribe_validation_errors(tmp_path: Path) -> None:
    bad_dev = transcribe_audio_to_midi(str(tmp_path / "a.wav"), device="tpu")
    assert bad_dev["success"] is False
    assert "Invalid device" in bad_dev["error"]

    missing = transcribe_audio_to_midi(str(tmp_path / "missing.wav"))
    assert missing["success"] is False
    assert "not found" in missing["error"]


def test_transcribe_success_parses_mid_and_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    audio = tmp_path / "demo_song.mp3"
    audio.write_bytes(b"fake-audio")
    fake_exe = tmp_path / "dettato.exe"
    fake_exe.write_text("", encoding="utf-8")
    out_dir = tmp_path / "out"

    def _fake_run(cmd: list[str], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        assert cmd[0] == str(fake_exe)
        assert "--device" in cmd
        assert "cuda" in cmd
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "demo_song.mid").write_bytes(b"MThd")
        (out_dir / "demo_song.json").write_text(
            json.dumps({"tuning_cents": -3.2, "tracks": [{"name": "Piano", "notes": 42}]}),
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(cmd, 0, stdout="ok", stderr="")

    monkeypatch.setattr("reaper_mcp.dettato_bridge.subprocess.run", _fake_run)

    result = transcribe_audio_to_midi(
        audio_path=str(audio),
        output_dir=str(out_dir),
        device="cuda",
        explicit_bin=str(fake_exe),
    )
    assert result["success"] is True
    assert result["midi_path"].endswith("demo_song.mid")
    assert result["metadata"]["tuning_cents"] == -3.2
    assert result["metadata"]["tracks"][0]["notes"] == 42


def test_transcribe_nonzero_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    audio = tmp_path / "broken.mp3"
    audio.write_bytes(b"bad")
    fake_exe = tmp_path / "dettato.exe"
    fake_exe.write_text("", encoding="utf-8")

    def _fake_run(cmd: list[str], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(cmd, 2, stdout="", stderr="CUDA out of memory")

    monkeypatch.setattr("reaper_mcp.dettato_bridge.subprocess.run", _fake_run)

    result = transcribe_audio_to_midi(str(audio), output_dir=str(tmp_path / "out"), explicit_bin=str(fake_exe))
    assert result["success"] is False
    assert result["returncode"] == 2
    assert "CUDA out of memory" in result["stderr"]


def test_build_midi_import_script_escapes_paths() -> None:
    script = _build_midi_import_script(r"D:\audio\demo_song.mid", "demo_song")
    assert "RPR_InsertMedia" in script
    assert r"D:\\audio\\demo_song.mid" in script


@pytest.mark.asyncio
async def test_orchestrator_audio_to_midi_and_reaper_import(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mcp = _DummyMCP()
    setup_orchestrator_portmanteau(mcp)
    tool = mcp.tools["reaper_orchestrator"]

    missing_arg = await tool(operation="audio_to_midi")
    assert missing_arg["success"] is False
    assert "audio_path" in missing_arg["error"]

    fake_mid = str(tmp_path / "song.mid")
    monkeypatch.setattr(
        "reaper_mcp.portmanteau.orchestrator._transcribe_audio_to_midi",
        lambda **_kw: {"success": True, "midi_path": fake_mid, "metadata": {"tracks": []}},
    )
    monkeypatch.setattr(
        "reaper_mcp.portmanteau.orchestrator.execute_reascript_code",
        lambda _code: {"success": True, "result": {"operation": "midi_import", "track_index": 1}},
    )

    res = await tool(operation="audio_to_midi", audio_path="song.mp3", import_to_reaper=True)
    assert res["success"] is True
    assert res["details"]["midi_path"] == fake_mid
    assert res["reaper_import"]["operation"] == "midi_import"
