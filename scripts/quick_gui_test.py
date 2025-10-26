#!/usr/bin/env python3
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from matlab_mcp_server.engine import MatlabEngine

print("Starting MATLAB GUI...")
eng = MatlabEngine()
eng.start(desktop=True)

print("Setting variable...")
eng.workspace["demo_var"] = 42.0

print("Checking value...")
value = eng.workspace["demo_var"]
print(f"demo_var = {value}")

print("\nSending message to MATLAB...")
eng.execute("fprintf('\\nHello! demo_var = %.0f\\n\\n', demo_var)", nargout=0)

print("\nMATLAB GUI is open!")
print("In MATLAB, type: demo_var")
print("You should see: 42")
print("\nPress Ctrl+C to exit...")

try:
    import time

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClosing...")
    eng.stop()
