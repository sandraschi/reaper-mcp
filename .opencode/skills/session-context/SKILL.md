---
name: session-context
description: Reaper-MCP tool-awareness for every session
---

## Session Context (Reaper MCP)

You have access to Reaper DAW automation tools via 6 portmanteau tools.

**Before starting work:**
1. Check transport status: reaper_transport(operation="status")
2. List tracks: reaper_tracks(operation="list")

**At end of work:**
- Save the project: reaper_project(operation="save")
