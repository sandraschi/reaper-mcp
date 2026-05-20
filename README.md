# Reaper MCP Server

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**Austrian precision DAW automation via Reaper with OSC control.**

## Quick Start

```powershell
git clone https://github.com/sandraschi/reaper-mcp
cd reaper-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## What's New (FastMCP 3.1)

- **FastMCP 3.1** - Full alignment: tools, prompts, skills, sampling-ready
- **Portmanteau tools** - 6 consolidated interfaces (transport, tracks, project, system, reascript, orchestrator)
- **Prompts** - Session templates: record, mix, export, transport, tracks, project, system help
- **Skills** - Optional skills provider exposes `reaper_mcp/skills` as MCP resources (`skill://`)
- **Agentic workflows** - Chain tools; use sampling so the model can orchestrate record/edit/export in one flow
- **HTTP + stdio** - Web backend mounts MCP at `/mcp` (streamable HTTP); CLI runs stdio for Claude Desktop

## Portmanteau Tools

| Tool | Operations | Description |
|------|------------|-------------|
| `reaper_transport` | play, stop, pause, record, position, status | Playback control |
| `reaper_tracks` | list, info, mute, solo, arm, count, bulk | Track management |
| `reaper_project` | info, save, marker, render, stats | Project operations |
| `reaper_system` | status, help, capabilities | System status |
| `reaper_reascript` | run, setup, api_help | ReaScript execution and API help |
| `reaper_orchestrator` | stem_import, fx_chain, regions, full_pipeline | SG2-to-mix workflow automation |

##  Quick Start

### Prerequisites

- **Reaper DAW** installed and running
- **Python 3.10+**
- **OSC enabled** in Reaper

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx reaper-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "reaper-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/reaper-mcp", "run", "reaper-mcp"]
  }
}
```
### Reaper OSC Setup 

1. Open **Reaper preferences** (Ctrl+P)
2. Go to **Control/OSC/web**
3. Click **Add**  new OSC device
4. Configure:
   - **Local IP**: `127.0.0.1`
   - **Local listen port**: `8000`
   - **Remote port**: `8001`
   -  Enable **"Send all feedback"**
5. Click **OK** and **Apply**

### Claude Desktop Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "reaper-mcp": {
      "command": "python",
      "args": ["D:\\Dev\\repos\\reaper-mcp\\server.py"],
      "env": {}
    }
  }
}
```

##  Usage Examples

### Natural Language (via Claude)

```
"Play the project"
"Mute track 3"
"Solo tracks 1 and 2"
"Add a marker called 'Chorus' at 1:30"
"Save the project"
"Arm track 1 for recording and start recording"
```

### ReaScript JSON Support 

Scripts can now return structured data by setting the `_result` variable:

```python
import reapy
project = reapy.Project.today()
_result = {
    "name": project.name, 
    "tracks": project.n_tracks, 
    "sample_rate": project.sample_rate
}
```

The `reaper_reascript` tool will automatically detect and return this data as a JSON object.

### Portmanteau Tool Examples

```python
# Transport control
reaper_transport("play")
reaper_transport("stop")
reaper_transport("record")
reaper_transport("status")

# Track management
reaper_tracks("list")
reaper_tracks("mute", track_id=3, value=True)
reaper_tracks("solo", track_id=1)
reaper_tracks("arm", track_id=1, value=True)
reaper_tracks("bulk", track_ids=[1,2,3], bulk_operation="mute", value=True)

# Project operations
reaper_project("info")
reaper_project("save")
reaper_project("marker", position="1:30", name="Chorus")
reaper_project("render", format="wav", quality="high")

# System status
reaper_system("status")
reaper_system("help")
reaper_system("capabilities")

# Orchestrator workflow
reaper_orchestrator("stem_import", stems_folder="D:/music/sg2-output")
reaper_orchestrator("fx_chain", vibe="classical_master", stems_folder="D:/music/sg2-output")
reaper_orchestrator("regions", regions_text="[verse] 00:10-00:42 [chorus] 00:42-01:10")
reaper_orchestrator(
    "full_pipeline",
    stems_folder="D:/music/sg2-output",
    vibe="dark_techno",
    regions_text="[intro] 00:00-00:16 [drop] 00:48-01:20",
)
```

## Architecture

```

                        Claude / Cursor                          
                         (MCP Client)                            

                           MCP Protocol (stdio)
                          

                      Reaper MCP Server                          
                        (FastMCP 3.1)                           
     
    Portmanteau Tools + Prompts + Skills (optional)             
    transport  tracks  project  system  reascript           
     
                                                                 
                                          
                   OSC Client                                  
                  (python-osc)                                 
                                          

                           OSC UDP (localhost:8000)
                          

                         Reaper DAW                              
    
                     OSC Control Surface                        
    
          
   Transport     Tracks       Mixer         Project     
          

```

## Configuration

### Environment Variables

```env
# OSC Settings
OSC_HOST=127.0.0.1
OSC_PORT=8000

# Tool mode
REAPER_TOOL_MODE=portmanteau  # or "individual"

# Reaper paths (optional)
REAPER_PATH=C:/Program Files/REAPER/reaper.exe
REAPER_PROJECT_PATH=D:/Music/Projects
```

##  Testing Scaffold

This project includes an extensive testing scaffold for both local development and CI:

- **Unit Tests**: `pytest tests/unit` (Mocked OSC/Reapy)
- **Integration Tests**: `pytest tests/integration` (Local server loopback)
- **E2E Verification**: `python scripts/verify_e2e.py` (Stdio transport verification)

## Crosslink API Endpoints

The backend now exposes a cross-repo integration surface at `\api\v1\crosslinks`:

- `GET /api/v1/crosslinks/health` - crosslink API status and registry metrics
- `GET /api/v1/crosslinks/repos` - list registered and discovered repos
- `POST /api/v1/crosslinks/repos` - register repo metadata for integration
- `GET /api/v1/crosslinks/repos/{repo_name}` - fetch one repo link entry
- `GET /api/v1/crosslinks/repos/{repo_name}/endpoints` - integration endpoint templates
- `GET /api/v1/crosslinks/search?q=...` - search registered links by name, tags, notes

Set `REAPER_CROSSLINK_REPO_ROOT` if your repos are not under `D:\Dev\repos`.

## Troubleshooting

### "Not connected to Reaper"

1. Ensure Reaper is running
2. Verify OSC is enabled in Reaper preferences
3. Check port 8000 isn't blocked

### "OSC no response"

1. Enable "Send all feedback" in Reaper OSC settings
2. Verify Local listen port matches (8000)

## Sampling and agentic workflows

- **Sampling**: Clients that support MCP sampling can let the server request LLM completions during tool runs; Reaper MCP is sampling-ready (dialogic returns, tool chaining).
- **Agentic**: Chain tools (e.g. `reaper_system status` -> `reaper_transport play` -> `reaper_tracks list`). Use registered prompts for session templates (record, mix, export).

## Austrian efficiency

- **5 portmanteau tools** instead of 21 individual tools
- **Prompts** for session templates; **skills** for workflow resources
- **FastMCP 3.1** - single stdio or HTTP transport, no 2.x patterns

---

**Built with Austrian precision for professional DAW automation.**


## Web dashboard (web_sota)

Web interface for monitoring and control. Ports: **10796** (frontend), **10797** (backend). MCP streamable HTTP at **http://localhost:10797/mcp**.

To start: from repo root run `web_sota\start.ps1` (PowerShell), then open `http://localhost:10796`.


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.
