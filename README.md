# Reaper MCP Server 🎵

[![FastMCP](https://img.shields.io/badge/FastMCP-2.13.1-blue.svg)](https://gofastmcp.com)
[![Portmanteau](https://img.shields.io/badge/Tools-4%20Portmanteau-purple.svg)](#-portmanteau-tools)

**Austrian precision DAW automation via Reaper with OSC control.**

## ✨ What's New (v2.0)

- **FastMCP 2.13.1** - Latest MCP framework
- **Portmanteau Tools** - 21 tools consolidated into 4 clean interfaces (81% reduction!)
- **Streamlined CI/CD** - Single workflow, ruff linting

## 🎛️ Portmanteau Tools

| Tool | Operations | Description |
|------|------------|-------------|
| `reaper_transport` | play, stop, pause, record, position, status | Playback control |
| `reaper_tracks` | list, info, mute, solo, arm, count, bulk | Track management |
| `reaper_project` | info, save, marker, render, stats | Project operations |
| `reaper_system` | status, help, capabilities | System status |

### Tool Mode

Set `REAPER_TOOL_MODE` environment variable:
- `portmanteau` (default) - 4 consolidated tools
- `individual` - 21 individual tools (backward compatibility)

## 🚀 Quick Start

### Prerequisites

- **Reaper DAW** installed and running
- **Python 3.10+**
- **OSC enabled** in Reaper

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx reaper-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "reaper-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/reaper-mcp", "run", "reaper-mcp"]
  }
}
```
### Reaper OSC Setup 🎛️

1. Open **Reaper preferences** (Ctrl+P)
2. Go to **Control/OSC/web**
3. Click **Add** → new OSC device
4. Configure:
   - **Local IP**: `127.0.0.1`
   - **Local listen port**: `8000`
   - **Remote port**: `8001`
   - ✅ Enable **"Send all feedback"**
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

## 🎼 Usage Examples

### Natural Language (via Claude)

```
"Play the project"
"Mute track 3"
"Solo tracks 1 and 2"
"Add a marker called 'Chorus' at 1:30"
"Save the project"
"Arm track 1 for recording and start recording"
```

### ReaScript JSON Support 📊

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
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude / Cursor                          │
│                         (MCP Client)                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │ MCP Protocol (stdio)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Reaper MCP Server                          │
│                       (FastMCP 2.13.1)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              4 Portmanteau Tools                          │   │
│  │  reaper_transport │ reaper_tracks │ reaper_project │ ...  │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             ▼                                    │
│              ┌─────────────────────┐                            │
│              │     OSC Client      │                            │
│              │    (python-osc)     │                            │
│              └──────────┬──────────┘                            │
└─────────────────────────┼───────────────────────────────────────┘
                          │ OSC UDP (localhost:8000)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Reaper DAW                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   OSC Control Surface                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────────┐  │
│  │ Transport │  │  Tracks   │  │  Mixer    │  │   Project   │  │
│  └───────────┘  └───────────┘  └───────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
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

## 🧪 Testing Scaffold

This project includes an extensive testing scaffold for both local development and CI:

- **Unit Tests**: `pytest tests/unit` (Mocked OSC/Reapy)
- **Integration Tests**: `pytest tests/integration` (Local server loopback)
- **E2E Verification**: `python scripts/verify_e2e.py` (Stdio transport verification)

## Troubleshooting

### "Not connected to Reaper"

1. Ensure Reaper is running
2. Verify OSC is enabled in Reaper preferences
3. Check port 8000 isn't blocked

### "OSC no response"

1. Enable "Send all feedback" in Reaper OSC settings
2. Verify Local listen port matches (8000)

## 🇦🇹 Austrian Efficiency

- **4 tools** instead of 21 (81% reduction!)
- **Practical solutions** over theoretical complexity
- **No decision paralysis** - exactly what you need

---

**Built with Austrian precision for professional DAW automation! 🎵🇦🇹**


## 🌐 Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10796**.
*(Assigned ports: **10796** (Web dashboard frontend), **10797** (Web dashboard backend))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10796` in your browser.
