#!/usr/bin/env python3
"""
Simple script to start MATLAB GUI and set it up for you to use.
This keeps the session alive so you can interact with it.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine
import time

print("=" * 70)
print("Starting MATLAB GUI Session")
print("=" * 70)

# Start MATLAB with GUI
print("\n1. Starting MATLAB with desktop GUI...")
engine = MatlabEngine()
engine.start(desktop=True)
print("   ✓ MATLAB GUI should be opening...")

time.sleep(2)  # Give MATLAB time to open

# Make it shared
print("\n2. Creating shared session...")
session_name = engine.make_shared("MySession")
print(f"   ✓ Session name: {session_name}")

# Set up some variables
print("\n3. Setting up demo variables...")
engine.workspace["demo_var"] = 42.0
engine.workspace["x"] = list(range(1, 11))
engine.workspace["message"] = "Hello from Python!"

# Display info in MATLAB
print("\n4. Displaying info in MATLAB Command Window...")
engine.execute(
    """
    clc;
    fprintf('\\n=== MATLAB Session Started ===\\n');
    fprintf('Session: %s\\n', matlab.engine.engineName);
    fprintf('\\nDemo variables created:\\n');
    fprintf('  demo_var = %.0f\\n', demo_var);
    fprintf('  message = %s\\n', message);
    fprintf('  x = 1:10\\n');
    fprintf('\\nTry typing:\\n');
    fprintf('  >> who\\n');
    fprintf('  >> demo_var\\n');
    fprintf('  >> plot(x, x.^2)\\n');
    fprintf('\\n==============================\\n\\n');
""",
    nargout=0,
)

# Create a simple plot
print("\n5. Creating demo plot...")
engine.execute(
    """
    figure('Name', 'Demo from Python');
    plot(x, x.^2, 'bo-', 'LineWidth', 2, 'MarkerSize', 8);
    title('Demo Plot: y = x^2');
    xlabel('x');
    ylabel('y');
    grid on;
""",
    nargout=0,
)

print("\n" + "=" * 70)
print("✓ MATLAB GUI is ready!")
print("=" * 70)
print(f"\nSession: {session_name}")
print("\nCheck your MATLAB window - you should see:")
print("  • Welcome message in Command Window")
print("  • Variables in Workspace: demo_var, x, message")
print("  • A plot window")

print("\n" + "=" * 70)
print("Session will stay open - press Ctrl+C when done")
print("=" * 70)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nClosing MATLAB...")
    engine.stop()
    print("✓ MATLAB closed")
