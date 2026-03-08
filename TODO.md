# reaper-mcp TODO
> Last updated: 2026-03-04
> For use with Google Antigravity IDE (config: C:\Users\sandr\.gemini\antigravity)

---

## REASCRIPT / REAPY EXTENSION

### Current state (honest assessment)

`reaper_reascript` portmanteau tool exists in `reaper_mcp/portmanteau/reascript.py`
and is wired into the server. It has 3 operations: `run`, `setup`, `api_help`.

**What actually works:**
- `setup` — calls `reapy.configure_reaper()`, one-time setup
- `run` — `exec()`s arbitrary Python code with `reapy` and `RPR.*` in scope,
  returns `_result` as JSON if set
- `api_help` — looks up docstring for any `RPR_*` function

**What is MISSING / broken:**

### TODO-1: reapy connection management
- No connection check before operations — fails silently if Reaper not running
- Need `reapy.connect()` / `reapy.disconnect()` lifecycle handling
- Need a `status` operation that checks if reapy can reach Reaper
- Consider connection pool / singleton pattern to avoid reconnect overhead

### TODO-2: `run` operation is too bare
- No timeout — a hanging script hangs the MCP tool indefinitely
- No stdout capture — `print()` in scripts goes nowhere
- No import whitelist — security consideration (exec is wide open)
- No way to pass parameters into the script cleanly
- Suggestion: wrap exec in a thread with timeout (e.g. 10s default)

### TODO-3: Missing high-level reapy operations
The current tool is basically "exec arbitrary code". Missing convenient
operations that don't require the caller to know the reapy API:

```
operation="get_selected_tracks"   → list selected track names/indices
operation="get_items"             → list media items on a track
operation="get_fx_chain"          → list FX on a track with params
operation="set_fx_param"          → set a specific FX parameter by name
operation="insert_media"          → insert a file as a media item at position
operation="get_markers"           → list all markers with names and positions
operation="set_tempo"             → set project BPM via reapy (not OSC)
operation="get_time_selection"    → return start/end of time selection
operation="apply_fx_preset"       → load a named preset on an FX slot
```

These wrap common reapy patterns so callers don't need to write exec code.

### TODO-4: Webapp reascript page is stub
`web_sota/src/pages/reascript.tsx` exists but check if it's actually wired
to the backend. Needs:
- Code editor (CodeMirror or Monaco — Monaco preferred, lighter bundle)
- Run button → calls `reaper_reascript("run", code=...)`
- Output panel showing result / `_result` JSON
- Preset snippets panel (common scripts)
- History of last N executed scripts (session only)

### TODO-5: ai music integration operations (new)
See `mcp-central-docs/not-mcp-related/ai-music/DAW_INTEGRATION_AND_MCP.md`
for full spec. Needed operations in a new `reaper_ai` portmanteau:

```
operation="insert_clip"           → import WAV to track at position
operation="create_ai_track"       → add labeled track for AI content
operation="region_to_file"        → export named region to WAV
operation="batch_import"          → import folder of WAVs to sequential tracks
operation="set_color_ai"          → color AI tracks distinctly
operation="label_ai_items"        → tag items with source metadata in notes
```

This enables the acestep-mcp → reaper-mcp pipeline.

---

## WEBAPP ADDITIONS

### TODO-6: `/ai-music` page (new)
- Requires acestep-mcp to be running (see acestep-mcp repo when created)
- Quick generate → auto-import to Reaper
- AI track list in current project
- One-click bounce-to-file per track
- Region list with "send to ACE-Step repaint" buttons

### TODO-7: connection resilience
- Dashboard shows OSC connection status (already exists) but reapy
  connection status is not shown — add reapy status indicator
- Auto-reconnect button for both OSC and reapy

---

## KNOWN ISSUES

- `reaper_reascript("run")` with code that calls blocking RPR functions
  (e.g. `RPR.RPR_MB()` which shows a message box) will deadlock the MCP call.
  Fix: thread + timeout wrapper.

- The README documents `REAPER_TOOL_MODE=individual` for 21 individual tools
  but the individual tool files (`transport.py`, `tracks.py`, etc. at root
  `reaper_mcp/`) are the old versions — they may be out of sync with the
  portmanteau versions. Verify or remove individual mode.

- `docs/REASCRIPT_SETUP.md` exists — check it's accurate against the current
  `reascript.py` implementation. Likely written before the portmanteau refactor.

---

## PRIORITY ORDER

1. TODO-1 (connection management) — blocks everything else from being reliable
2. TODO-2 (exec timeout) — correctness/reliability
3. TODO-3 (high-level ops) — usability for Claude/AI workflows
4. TODO-5 (reaper_ai portmanteau) — enables AI music pipeline
5. TODO-4 (webapp reascript page) — usability
6. TODO-6 (webapp /ai-music page) — depends on acestep-mcp existing
7. TODO-7 (connection resilience UI) — polish

Estimated total: 3-5 days with AI-assisted dev.
