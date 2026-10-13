"""Audio relay server — captures from a Windows audio device and streams as HTTP audio.

Start: reaper_audio(operation="start_relay", port=11136, device="CABLE Output")
Stop:  reaper_audio(operation="stop_relay")
URL:   http://127.0.0.1:{port}/stream  → paste into butterchurn Stream mode
"""

from __future__ import annotations

import asyncio
import logging
import struct
import threading
import time
from typing import Any

logger = logging.getLogger(__name__)

_SAMPLE_RATE = 44100
_CHANNELS = 1
_DTYPE = "int16"
_BLOCK_SIZE = 1024
_WAV_HEADER = None

_relay_server: Any = None
_relay_thread: threading.Thread | None = None


def _make_wav_header(data_len: int) -> bytes:
    sample_rate = _SAMPLE_RATE
    channels = _CHANNELS
    bits = 16
    byte_rate = sample_rate * channels * bits // 8
    block_align = channels * bits // 8
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        data_len + 36,
        b"WAVE",
        b"fmt ",
        16,
        1,
        channels,
        sample_rate,
        byte_rate,
        block_align,
        bits,
        b"data",
        data_len,
    )
    return header


class RingBuffer:
    def __init__(self, max_seconds: int = 5):
        self.buf = bytearray()
        self.max_bytes = max_seconds * _SAMPLE_RATE * _CHANNELS * 2
        self._lock = threading.Lock()

    def write(self, data: bytes):
        with self._lock:
            self.buf.extend(data)
            if len(self.buf) > self.max_bytes:
                del self.buf[: len(self.buf) - self.max_bytes]

    def read_all(self) -> bytes:
        with self._lock:
            return bytes(self.buf)

    def clear(self):
        with self._lock:
            self.buf.clear()


_ring = RingBuffer()


async def _stream_response(scope, receive, send):
    assert scope["type"] == "http"
    global _WAV_HEADER
    if _WAV_HEADER is None:
        _WAV_HEADER = _make_wav_header(0xFFFFFFFF)

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"audio/wav"),
                (b"cache-control", b"no-cache"),
                (b"access-control-allow-origin", b"*"),
            ],
        }
    )

    sent_header = False
    while True:
        chunk = _ring.read_all() if sent_header else _WAV_HEADER + _ring.read_all()
        sent_header = True
        if chunk:
            await send({"type": "http.response.body", "body": chunk, "more_body": True})
        else:
            await asyncio.sleep(0.05)

        try:
            await asyncio.sleep(0)
        except asyncio.CancelledError:
            break

    await send({"type": "http.response.body", "body": b"", "more_body": False})


def _capture_worker(device: str | None):
    import sounddevice as sd

    def callback(indata, frames, tid, status):
        if status:
            logger.warning("audio relay status: %s", status)
        _ring.write(indata.tobytes())

    try:
        device_id = None
        if device:
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if device.lower() in dev["name"].lower():
                    device_id = i
                    break
            if device_id is None:
                logger.warning("audio device %r not found — using default", device)

        with sd.InputStream(
            samplerate=_SAMPLE_RATE,
            channels=_CHANNELS,
            dtype=_DTYPE,
            blocksize=_BLOCK_SIZE,
            callback=callback,
            device=device_id,
        ):
            while _relay_thread is not None and _relay_thread.is_alive():
                time.sleep(0.5)
    except Exception as e:
        logger.error("audio capture failed: %s", e)


async def _run_server(port: int):
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Route

    app = Starlette(
        routes=[Route("/stream", endpoint=_stream_response)],
    )
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    global _relay_server
    _relay_server = server
    await server.serve()


def start_relay(port: int = 11136, device: str | None = None) -> dict[str, Any]:
    """Start the audio relay server in a background thread."""
    global _relay_thread
    if _relay_thread is not None and _relay_thread.is_alive():
        return {
            "success": True,
            "message": f"Relay already running on port {port}",
            "url": f"http://127.0.0.1:{port}/stream",
        }

    _ring.clear()

    def _run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_run_server(port))

    _relay_thread = threading.Thread(target=_run, daemon=True)
    _relay_thread.start()
    time.sleep(0.5)

    cap_thread = threading.Thread(target=_capture_worker, args=(device,), daemon=True)
    cap_thread.start()

    return {
        "success": True,
        "message": f"Audio relay started on port {port}",
        "url": f"http://127.0.0.1:{port}/stream",
        "device": device or "default",
    }


def stop_relay() -> dict[str, Any]:
    """Stop the audio relay server."""
    global _relay_server, _relay_thread
    if _relay_server is not None:
        _relay_server.should_exit = True
        _relay_server = None
    _relay_thread = None
    _ring.clear()
    return {"success": True, "message": "Audio relay stopped"}


def relay_status() -> dict[str, Any]:
    """Get relay status."""
    running = _relay_thread is not None and _relay_thread.is_alive()
    return {
        "success": True,
        "running": running,
        "url": "http://127.0.0.1:11136/stream" if running else None,
    }
