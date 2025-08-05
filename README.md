# Reaper MCP Server 🎵

**FastMCP 2.1** compliant server for **Austrian precision digital audio workstation automation via Reaper DAW**.

## Features 🎯

- ✅ **FastMCP 2.1 compliance** - Modern async/await patterns
- ✅ **Real OSC integration** - Bidirectional communication with Reaper
- ✅ **Transport control** - Play, stop, pause, record automation
- ✅ **Track management** - Mute, solo, arm, bulk operations
- ✅ **Project automation** - Save, markers, rendering control
- ✅ **Austrian engineering quality** - Precision and reliability 🇦🇹

## Quick Start 🚀

### Prerequisites

- **Reaper DAW** installed and running
- **Python 3.9+** with asyncio support
- **OSC enabled** in Reaper (see setup below)

### Installation

```bash
cd D:\Dev\repos\reaper-mcp
pip install -r requirements.txt
```

### Reaper OSC Setup 🎛️

1. Open **Reaper preferences** (Ctrl+P)
2. Go to **Control/OSC/web**
3. Click **Add** to create new OSC device
4. Configure:
   - **Local IP**: `127.0.0.1`
   - **Local listen port**: `8000`
   - **Remote port**: `8001`
   - **Pattern config**: `Default.ReaperOSC`
   - ✅ Enable **"Send all feedback"**
5. Click **OK** and **Apply**

### Testing

```bash
python dev_test.py    # Test OSC connection and functionality
python server.py      # Start MCP server
```

## Usage Examples 🎼

### Transport Control

```python
# Start playback
await play_transport()

# Stop and get position
await stop_transport()
position = await get_transport_position()

# Record with armed tracks
await record_transport()
```

### Track Management

```python
# Get all tracks
tracks = await get_tracks()

# Mute track 3
await mute_track(3, muted=True)

# Bulk solo tracks 1,2,3
await bulk_track_operation("solo", [1,2,3], True)

# Arm track for recording
await arm_track_recording(1, armed=True)
```

### Project Operations

```python
# Get project info
info = await get_project_info()

# Add marker at 2:30
await add_marker("2:30", "Chorus Start")

# Save project
await save_project()

# Render project
await render_project("wav", "high", "project")
```

## FastMCP 2.1 Tools 🔧

### Transport Control

- `play_transport()` - Start playback
- `stop_transport()` - Stop playback  
- `pause_transport()` - Pause playback
- `record_transport()` - Start recording
- `get_transport_position()` - Get current position
- `transport_status()` - Complete transport state

### Track Management

- `get_tracks()` - List all tracks with details
- `get_track_info(track_id)` - Specific track information
- `arm_track_recording(track_id, armed)` - Arm/disarm for recording
- `mute_track(track_id, muted)` - Mute/unmute track
- `solo_track(track_id, solo)` - Solo/unsolo track
- `get_track_count()` - Total track count
- `bulk_track_operation(operation, track_ids, value)` - Bulk operations

### Project Management

- `get_project_info()` - Project details and statistics
- `save_project()` - Save current project
- `add_marker(position, name)` - Add timeline marker
- `render_project(format, quality, bounds)` - Render/bounce
- `get_project_stats()` - Comprehensive project metrics

### System Tools

- `get_server_status()` - Server and connection status
- `list_capabilities()` - Available tools and categories

## Claude Desktop Integration 📱

Add to Claude Desktop MCP configuration:

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

## Configuration ⚙️

Copy `.env.template` to `.env` and customize:

```env
# Server configuration
SERVER_NAME=reaper-mcp
SERVER_VERSION=1.0.0
DEBUG=true

# Reaper configuration  
REAPER_PATH="C:\Program Files\REAPER\reaper.exe"
REAPER_PROJECT_PATH=D:\Music\Projects
OSC_HOST=127.0.0.1
OSC_PORT=8000

# Audio settings
DEFAULT_SAMPLE_RATE=44100
DEFAULT_BIT_DEPTH=24
AUTO_SAVE_INTERVAL=300
```

## Troubleshooting 🔍

### Connection Issues

- **OSC not connecting**: Check Reaper OSC settings and firewall
- **No feedback**: Verify "Send all feedback" is enabled
- **Port conflicts**: Ensure ports 8000/8001 are available
- **Permission denied**: Run as administrator if needed

### Common Solutions

```bash
# Test OSC connection
python dev_test.py

# Check Reaper OSC status
# In Reaper: Actions → Show action list → Search "OSC"

# Restart OSC in Reaper
# Preferences → Control/OSC/web → Disable/Enable device
```

## Architecture 🏗️

```
reaper-mcp/
├── reaper_mcp/
│   ├── __init__.py           # Package constants
│   ├── osc_client.py         # OSC communication layer
│   ├── transport.py          # Transport control tools
│   ├── tracks.py             # Track management tools
│   └── project.py            # Project automation tools
├── server.py                 # FastMCP 2.1 main server
├── dev_test.py               # Development testing
├── requirements.txt          # Dependencies
├── .env.template             # Configuration template
└── README.md                 # This documentation
```

## Austrian Context 🇦🇹

**Sandra's Audio Setup**:

- Windows-based Reaper installation
- Standard OSC configuration (localhost:8000)
- Professional audio production workflow
- German language support in messages
- Budget-conscious efficiency (~€100/month constraint)

## Dependencies 📦

- **FastMCP 2.1+** - Modern MCP server framework
- **python-osc** - OSC protocol communication
- **mido** - MIDI support (future expansion)
- **aiofiles** - Async file operations
- **pydantic** - Data validation

## Development 👩‍💻

```bash
# Install development dependencies
pip install -r requirements.txt

# Test OSC functionality
python dev_test.py

# Run server locally
python server.py

# Check connections
python -c "import asyncio; from reaper_mcp.osc_client import ReaperOSCClient; asyncio.run(ReaperOSCClient().connect())"
```

## License ⚖️

MIT License - Austrian engineering quality with international compatibility.

## Author 🎼

**Sandra's Austrian Audio Automation 🇦🇹**

*"Sin temor y sin esperanza" - Practical audio automation without hype.*

---

**Ready for professional audio automation in Vienna! 🎵🇦🇹**
