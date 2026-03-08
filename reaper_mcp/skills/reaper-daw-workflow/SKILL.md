---
description: Reaper DAW automation and session workflows via Reaper MCP (FastMCP 3.1)
---

# Reaper DAW Workflow

Use Reaper MCP tools to control Reaper: transport, tracks, project, and system.

## Portmanteau tools

- **reaper_transport**: play, stop, pause, record, position, status
- **reaper_tracks**: list, info, mute, solo, arm, count, bulk
- **reaper_project**: info, save, marker, render, stats
- **reaper_system**: status, help, capabilities
- **reaper_reascript**: run, setup, api_help

## Agentic workflows

Chain tools for recording (system status -> transport record -> tracks arm), mixing (tracks mute/solo -> project render), or export (project render with format/quality).

## Prompts

Use MCP prompts for session templates: reaper_record_session, reaper_mix_session, reaper_export_project, reaper_transport_control, reaper_track_operations, reaper_project_help, reaper_system_help.
