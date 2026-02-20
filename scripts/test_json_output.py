import requests
import json

URL = "http://localhost:10793/tools/call"


def test_json_output():
    print("Testing JSON output from ReaScript...")

    code = """
_result = {
    "project_name": "Test Project",
    "tracks": [
        {"name": "Track 1", "id": 1},
        {"name": "Track 2", "id": 2}
    ],
    "tempo": 120
}
"""

    payload = {
        "name": "reaper_reascript",
        "arguments": {"operation": "run", "code": code},
    }

    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        data = response.json()

        content = data.get("content", [{}])[0].get("text", "")
        print(f"Raw response: {content}")

        # Verify it's valid JSON
        parsed = json.loads(content)
        print("\n✅ Valid JSON received!")
        print(json.dumps(parsed, indent=2))

        if parsed["project_name"] == "Test Project":
            print("\n✅ Content matches expected output.")
        else:
            print("\n❌ Content mismatch.")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_json_output()
