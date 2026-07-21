"""
reaper_mcp - Reaper MCP Server Package
FastMCP 2.1 compliant audio workstation automation for Reaper DAW
"""

__version__ = "1.0.0"
__author__ = "Sandra's Austrian Audio Automation 🇦🇹"
__description__ = "Reaper DAW automation with OSC control and Austrian engineering quality"

# Default Reaper configuration
DEFAULT_OSC_HOST = "127.0.0.1"
DEFAULT_OSC_PORT = 8000
DEFAULT_REAPER_PATH = "C:\\Program Files\\REAPER\\reaper.exe"
DEFAULT_PROJECT_PATH = "D:\\Music\\Projects"

# Audio defaults
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_BIT_DEPTH = 24
DEFAULT_AUTO_SAVE_INTERVAL = 300

# OSC message patterns
OSC_PATTERNS = {
    "transport": {
        "play": "/play",
        "stop": "/stop",
        "pause": "/pause",
        "record": "/record",
        "position": "/position",
    },
    "tracks": {
        "count": "/track/count",
        "name": "/track/{}/name",
        "mute": "/track/{}/mute",
        "solo": "/track/{}/solo",
        "arm": "/track/{}/recarm",
        "volume": "/track/{}/volume",
        "pan": "/track/{}/pan",
    },
    "project": {
        "name": "/project/name",
        "sample_rate": "/project/samplerate",
        "length": "/project/length",
        "save": "/project/save",
    },
    "markers": {"add": "/marker/add", "delete": "/marker/{}", "list": "/marker/list"},
}
