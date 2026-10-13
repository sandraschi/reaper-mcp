"""
reaper_audio — Audio relay for piping Reaper output to butterchurn visualizer.

OPERATIONS:
- start_relay: Start the audio relay server (captures from device, serves HTTP stream)
- stop_relay: Stop the relay
- relay_status: Check if the relay is running
- list_devices: List available audio capture devices
"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from pydantic import Field

logger = logging.getLogger(__name__)


def setup_audio_portmanteau(mcp):
    """Register the reaper_audio portmanteau tool."""

    @mcp.tool()
    async def reaper_audio(
        operation: Annotated[str, Field(description="Operation: start_relay, stop_relay, relay_status, list_devices")],
        port: Annotated[int, Field(description="HTTP port for the relay (default 11136)")] = 11136,
        device: Annotated[
            str | None, Field(description="Windows audio device name substring, e.g. 'CABLE Output' or 'Speakers'")
        ] = None,
    ) -> dict[str, Any]:
        """Audio relay for piping Reaper output to butterchurn visualizer.

        Starts an HTTP server that captures from a local audio device and streams
        it as WAV audio. Paste the returned URL into butterchurn's Stream mode
        to see Reaper audio drive the MilkDrop visualizer.

        Requires: sounddevice (`uv sync --extra audio`).

        OPERATIONS:
        - start_relay: Start the relay. Returns URL to paste into butterchurn.
        - stop_relay: Stop the relay.
        - relay_status: Check if the relay is running.
        - list_devices: List audio devices available for capture.

        ## Return Format
        {"success": bool, "operation": str, "message": str,
         "url"?: str, "device"?: str, "running"?: bool}

        ## Examples
        reaper_audio(operation="list_devices")
        reaper_audio(operation="start_relay", device="CABLE Output")
        reaper_audio(operation="start_relay", port=11136)
        reaper_audio(operation="stop_relay")
        reaper_audio(operation="relay_status")
        """
        valid_ops = ["start_relay", "stop_relay", "relay_status", "list_devices"]
        if operation not in valid_ops:
            return {"success": False, "error": f"Invalid operation: {operation}", "valid_operations": valid_ops}

        if operation == "list_devices":
            try:
                import sounddevice as sd

                devices = []
                for i, dev in enumerate(sd.query_devices()):
                    if dev["max_input_channels"] > 0:
                        devices.append(f"{i}: {dev['name']} ({dev['max_input_channels']}ch)")
                return {"success": True, "operation": "list_devices", "devices": devices}
            except ImportError:
                return {
                    "success": False,
                    "operation": "list_devices",
                    "error": "sounddevice not installed. Run: uv sync --extra audio",
                }
            except Exception as e:
                return {"success": False, "operation": "list_devices", "error": str(e)}

        if operation == "start_relay":
            try:
                from reaper_mcp.audio_relay import start_relay as _start

                return _start(port=port, device=device)
            except ImportError as e:
                return {
                    "success": False,
                    "operation": "start_relay",
                    "error": f"Missing dependency: {e}. Run: uv sync --extra audio",
                }
            except Exception as e:
                return {"success": False, "operation": "start_relay", "error": str(e)}

        if operation == "stop_relay":
            try:
                from reaper_mcp.audio_relay import stop_relay as _stop

                return _stop()
            except Exception as e:
                return {"success": False, "operation": "stop_relay", "error": str(e)}

        if operation == "relay_status":
            try:
                from reaper_mcp.audio_relay import relay_status as _status

                return _status()
            except Exception as e:
                return {"success": False, "operation": "relay_status", "error": str(e)}

        return {"success": False, "error": f"Unknown operation: {operation}"}
