---
description: Reaper DAW automation and session workflows via Reaper MCP (FastMCP 3.1)
---

# Reaper DAW Workflow

**Description:** REAPER DAW automation and session workflows via MCP bridge. Covers track management, MIDI editing, audio FX, project organization, transport control, rendering, and ReaScript execution.

## Trigger Phrases

- "Create a new project with [tracks]"
- "Arm track [N] for recording"
- "Add reverb to [track name]"
- "Render the master mix to WAV"
- "Insert a MIDI clip at bar [N]"
- "Mute all tracks except vocals"
- "Run this ReaScript on the project"
- "Export stems for all tracks"
- "Set loop region from bar [A] to [B]"

## Portmanteau Tools

- **`reaper_transport(operation, ...)`** — Transport control. Operations: `play`, `stop`, `pause`, `record`, `position` (get/set), `status`.
- **`reaper_tracks(operation, ...)`** — Track management. Operations: `list`, `info`, `mute`, `solo`, `arm`, `count`, `bulk` (batch operations), `create`, `delete`, `duplicate`.
- **`reaper_project(operation, ...)`** — Project operations. Operations: `info`, `save`, `marker` (get/set), `render`, `stats`, `tempo` (get/set), `time_signature`.
- **`reaper_system(operation, ...)`** — System info. Operations: `status`, `help`, `capabilities`, `audio_device`, `midi_devices`.
- **`reaper_reascript(operation, script_path, ...)`** — ReaScript execution. Operations: `run` (execute .lua/.eel/.py), `setup` (configure script path), `api_help` (query Reaper API).
- **`reaper_midi(operation, ...)`** — MIDI editing. Operations: `insert_note`, `delete_note`, `quantize`, `list_notes`, `change_velocity`.

## Agentic Workflows

Chain tools for common DAW tasks:
- **Recording**: `reaper_system("status")` → `reaper_transport("record")` → `reaper_project("save")`
- **Mixing**: `reaper_tracks("list")` → `reaper_tracks("mute", tracks=[...])` → `reaper_project("render")`
- **Export**: `reaper_project("render", format="wav", quality=24)` or stem export via `reaper_tracks("bulk", operation="render_stems")`

## Prompts

Use MCP prompts for session templates: `reaper_record_session`, `reaper_mix_session`, `reaper_export_project`, `reaper_transport_control`, `reaper_track_operations`, `reaper_project_help`, `reaper_system_help`.

## Workflow

1. **Session check**: `reaper_project("info")` or `reaper_system("status")` to confirm Reaper is accessible.
2. **Setup**: Create/configure tracks via `reaper_tracks()`. Set tempo and time signature via `reaper_project()`.
3. **Production**: Use transport for recording, MIDI tools for composition, ReaScript for automation.
4. **Deliver**: Render to format via `reaper_project("render")` with format, bit depth, and sample rate params.

## Examples

- "Record a new guitar track." → `reaper_tracks("create", name="Guitar")` → `reaper_tracks("arm", track="Guitar")` → `reaper_transport("record")`
- "Render the project as 24-bit WAV." → `reaper_project("render", format="wav", quality=24, sample_rate=48000)`
- "Quantize all MIDI notes to 16th notes." → `reaper_midi("quantize", track="MIDI", grid="16th", strength=1.0)`
