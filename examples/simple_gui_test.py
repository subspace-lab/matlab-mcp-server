#!/usr/bin/env python3
"""
Simplest possible test: Start MATLAB with GUI and run a command.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from matlab_mcp_server.engine import MatlabEngine

print("Starting MATLAB with GUI...")
engine = MatlabEngine()
engine.start(desktop=True)

print("\n✓ MATLAB GUI should now be visible!")
print("\nExecuting: disp('Hello from Python!')")

engine.execute("disp('Hello from Python!')")
print("\n✓ Check the MATLAB Command Window - you should see the message!")

print("\nCreating shared session...")
session_name = engine.make_shared("SimpleTest")
print(f"✓ Session name: {session_name}")

print("\nFinding all shared sessions...")
sessions = MatlabEngine.find_shared_sessions()
print(f"✓ Found: {sessions}")

print("\nCreating a simple plot...")
engine.execute("""
    figure('Name', 'Test Plot from Python');
    x = 1:10;
    y = x.^2;
    plot(x, y, 'bo-', 'LineWidth', 2, 'MarkerSize', 8);
    title('Test Plot: y = x^2');
    xlabel('x'); ylabel('y');
    grid on;
""")

print("\n✓ Plot should appear in MATLAB!")
print("\nPress Ctrl+C to exit (or close MATLAB manually)")

try:
    input("\nPress Enter to close MATLAB...")
    engine.stop()
    print("✓ MATLAB closed")
except KeyboardInterrupt:
    print("\n\nExiting... MATLAB will stay open.")
