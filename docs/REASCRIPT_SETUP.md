# ReaScript Setup Guide for Reaper MCP

This guide explains how to set up Reaper to allow the `reaper-mcp` server to execute Python scripts directly within the DAW using `reapy-boost`.

## Prerequisites

1.  **Reaper**: Installed and running.
2.  **Python**: Installed (which you obviously have).
3.  **Enable Python in Reaper**:
    - Open Reaper.
    - Go to **Options > Preferences > Plug-ins > ReaScript**.
    - Ensure "Enable Python for use with ReaScript" is checked.
    - Point it to your Python DLL or executable directory if not auto-detected.

## Installation

The `reaper-mcp` server now includes `reapy-boost`.

## Configuration (One-Time Setup)

To allow external Python scripts (like this MCP server) to control Reaper, you need to configure the `reapy` server extension within Reaper.

### Method 1: Using the MCP Tool (Recommended)

1.  Start the `reaper-mcp` server.
2.  Access the `setup_reapy` tool via your MCP client.
3.  Execute the tool.
4.  Restart Reaper.

### Method 2: Manual Setup

If Method 1 fails, you can run this python command in your environment:

```bash
python -c "import reapy; reapy.configure_reaper()"
```

Then restart Reaper.

## Verification

To verify that ReaScript automation is working:

1.  Open Reaper.
2.  Use the `run_reascript` tool with the following code:
    ```python
    RPR_ShowConsoleMsg("Hello from MCP!")
    ```
3.  You should see "Hello from MCP!" appear in the Reaper console window.

## Usage

You can now use the `run_reascript` tool to execute any valid ReaScript Python code.

- **Variables available**:
    - `reapy`: The `reapy` module.
    - `RPR`: The raw Reaper API module (also available as `RPR_*` functions directly).

### Example: Create a track

```python
project = reapy.Project.today()
project.add_track(name="MCP Created Track")
```
