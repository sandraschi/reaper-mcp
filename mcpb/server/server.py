'''MCP server entry point for Reaper-MCP.

This is the MCPB-compliant server wrapper that launches the Reaper-MCP server.
'''

import sys
from pathlib import Path

# Add parent directory to path to import main server
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Import and run main server
from server import main

if __name__ == '__main__':
    main()

