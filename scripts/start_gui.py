#!/usr/bin/env python3
"""Start MATLAB with visible GUI - run this in your terminal."""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine

print("Starting MATLAB with GUI...")
print("(This will open a MATLAB window)\n")

eng = MatlabEngine()
eng.start(desktop=True)

print("✓ MATLAB GUI should be opening!")
print("\nCreating shared session...")
session_name = eng.make_shared("MyGUI")
print(f"✓ Session: {session_name}")

print("\nAdding demo variables...")
eng.workspace["demo"] = 42.0
eng.workspace["text"] = "Hello!"

eng.execute("""
fprintf('\\nPython connected!\\n');
fprintf('Session: %s\\n', matlab.engine.engineName);
fprintf('Type: demo\\n\\n');
""")

print("\n" + "=" * 60)
print("MATLAB GUI is running!")
print("=" * 60)
print(f"Session: {session_name}")
print("\nIn MATLAB, type: demo")
print("You should see: 42")
print("\nPress Ctrl+C when done (MATLAB will close)")
print("=" * 60)

try:
    import time

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nClosing MATLAB...")
    eng.stop()
    print("✓ Done")
