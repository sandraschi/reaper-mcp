"""
Verify ReaScript integration.
This script attempts to connect to a running Reaper instance via reapy.
"""

import sys

try:
    import reapy
except ImportError:
    print("Error: reapy-boost not installed.")
    sys.exit(1)


def main():
    print("Checking reapy connection...")

    # Check if reapy thinks it's inside reaper (it shouldn't be)
    if reapy.is_inside_reaper():
        print("Weird, we are inside Reaper?")
        return

    try:
        # Try to connect to the project
        # This will fail if Reaper is not running or not configured
        print("Attempting to get current project...")
        project = reapy.Project.today()
        print(f"Success! Connected to project: {project.name}")

        # Try a simple API call
        print("sending console message...")
        reapy.print("Hello from verification script!")
        print("Message sent to Reaper console.")

    except Exception as e:
        print(f"\nConnection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Is Reaper running?")
        print("2. Is 'Enable Python for use with ReaScript' checked in Preferences?")
        print("3. Have you run 'reapy.configure_reaper()' (or the setup_reapy tool)?")
        sys.exit(1)


if __name__ == "__main__":
    main()
