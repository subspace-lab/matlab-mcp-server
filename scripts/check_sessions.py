#!/usr/bin/env python3
"""Check for MATLAB sessions and show their details."""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine

print("=" * 70)
print("MATLAB Session Checker")
print("=" * 70)

print("\nSearching for shared MATLAB sessions...")
sessions = MatlabEngine.find_shared_sessions()

if not sessions:
    print("\n❌ No shared MATLAB sessions found.")
    print("\nTo create a shared session:")
    print("\n  Option 1 - In MATLAB GUI:")
    print("    1. Open MATLAB")
    print("    2. Type: matlab.engine.shareEngine")
    print("    3. Run this script again")

    print("\n  Option 2 - Let Python start MATLAB:")
    print("    .venv/bin/python quick_gui_test.py")
else:
    print(f"\n✅ Found {len(sessions)} shared session(s):\n")

    for i, session_id in enumerate(sessions, 1):
        print(f"{i}. Session ID: {session_id}")

        # Try to connect and get details
        try:
            print(f"   Connecting...")
            eng = MatlabEngine.connect_to_shared(session_id)

            # Get session info
            print(f"   ✅ Connected successfully!")

            # Check MATLAB version
            version = eng.execute("version")
            print(f"   Version: {version['output'].strip()}")

            # Check workspace variables
            vars_info = eng.list_workspace()
            vars_list = vars_info["variables"]
            if vars_list and "Your variables are:" in vars_list:
                var_names = vars_list.replace("Your variables are:", "").strip()
                if var_names:
                    print(f"   Variables: {var_names}")
                else:
                    print(f"   Variables: (none)")
            else:
                print(f"   Variables: (empty workspace)")

            # Get current directory
            pwd_result = eng.execute("pwd")
            pwd = pwd_result["output"].strip()
            print(f"   Directory: {pwd}")

            print()

        except Exception as e:
            print(f"   ❌ Could not connect: {e}")
            print()

print("=" * 70)
print("\nTo connect to a specific session in Python:")
print("=" * 70)
if sessions:
    example_session = sessions[0]
    print(f"""
from matlab_mcp_server.engine import MatlabEngine

# Connect to session: {example_session}
eng = MatlabEngine.connect_to_shared('{example_session}')

# Now use it
eng.set_variable('my_var', 123)
value = eng.get_variable('my_var')
print(value)  # 123
""")
else:
    print("\n(No sessions available to show example)")

print("=" * 70)
