import subprocess
import json
import sys
import time
import os


def run_e2e_test():
    """
    Run an End-to-End test by starting the server and communicating via Stdio.
    """
    print("Starting E2E Test...")

    # Path to server
    server_path = os.path.join(
        os.path.dirname(__file__), "..", "reaper_mcp", "server.py"
    )

    # Start server process
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,  # Unbuffered
    )

    try:
        # Give it a moment to start
        time.sleep(1)

        # 1. Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "e2e-tester", "version": "1.0"},
            },
        }
        send_request(process, init_req)
        response = read_response(process)
        assert response["id"] == 1
        print("✅ Initialize successful")

        # 2. List tools
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        send_request(process, list_req)
        response = read_response(process)
        assert response["id"] == 2
        tools = response["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert "reaper_system" in tool_names
        print(f"✅ Tools listed: {tool_names}")

        # 3. Call capabilities
        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "reaper_system",
                "arguments": {"operation": "capabilities"},
            },
        }
        send_request(process, call_req)
        response = read_response(process)
        assert response["id"] == 3
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["operation"] == "capabilities"
        print("✅ Capabilities call successful")

        # 4. Shutdown? (Optional, just kill is fine)

    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        print("Server stopped.")


def send_request(process, req):
    json_str = json.dumps(req)
    # stdio transport might expect newline delimited JSON
    process.stdin.write(json_str + "\n")
    process.stdin.flush()


def read_response(process):
    # Read line-by-line
    line = process.stdout.readline()
    if not line:
        raise RuntimeError("Server closed connection")
    return json.loads(line)


if __name__ == "__main__":
    try:
        run_e2e_test()
        print("\n🎉 ALL E2E TESTS PASSED!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ E2E TEST FAILED: {e}")
        sys.exit(1)
