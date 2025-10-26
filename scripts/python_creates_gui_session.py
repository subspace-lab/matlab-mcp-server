#!/usr/bin/env python3
"""
Demonstrate: Python creates a MATLAB GUI session that you can interact with.
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine
import time

print("=" * 70)
print("Python Creates MATLAB GUI Session")
print("=" * 70)

print("\n1. Python starting MATLAB with GUI (desktop mode)...")
eng = MatlabEngine()
eng.start(desktop=True)
print("   ✓ MATLAB GUI should be opening now!")

time.sleep(2)  # Give MATLAB time to fully open

print("\n2. Making it a shared session...")
session_name = eng.make_shared("PythonCreated")
print(f"   ✓ Session name: {session_name}")

print("\n3. Python adding variables...")
eng.workspace["from_python"] = 123.0
eng.workspace["message"] = "This session was created by Python!"
print("   ✓ Variables created: from_python, message")

print("\n4. Displaying info in MATLAB GUI...")
eng.execute("""
clc;
fprintf('\\n');
fprintf('================================================\\n');
fprintf('  This MATLAB GUI Was Started by Python!       \\n');
fprintf('================================================\\n');
fprintf('\\n');
fprintf('Session: %s\\n', matlab.engine.engineName);
fprintf('\\n');
fprintf('Python created these variables:\\n');
fprintf('  from_python = %.0f\\n', from_python);
fprintf('  message = %s\\n', message);
fprintf('\\n');
fprintf('Now YOU can interact with MATLAB:\\n');
fprintf('  >> from_python\\n');
fprintf('  >> from_python = 999\\n');
fprintf('  >> plot(1:10, (1:10).^2)\\n');
fprintf('\\n');
fprintf('================================================\\n');
fprintf('\\n');
""")

print("\n5. Creating a demo plot...")
eng.execute("""
figure('Name', 'Python Created This Session');
t = 0:0.01:2*pi;
plot(t, sin(2*t), 'b-', t, cos(3*t), 'r-', 'LineWidth', 2);
title('MATLAB GUI Started by Python!');
legend('sin(2t)', 'cos(3t)');
xlabel('t'); ylabel('Amplitude');
grid on;
""")

print("\n" + "=" * 70)
print("✓ MATLAB GUI is now fully operational!")
print("=" * 70)
print(f"\nSession ID: {session_name}")
print("\nThe MATLAB GUI window is open and you can:")
print("  • See variables in Workspace browser")
print("  • Type commands in Command Window")
print("  • View/interact with the plot")
print("  • Modify variables - Python will see changes!")

print("\n" + "=" * 70)
print("Bidirectional Test:")
print("=" * 70)
print("\n1. In MATLAB GUI, type:")
print("   >> from_python = 999")
print("\n2. Press Enter here to see Python read the change...")

input("\nPress Enter after you've changed 'from_python' in MATLAB...")

# Read back the value
value = eng.workspace["from_python"]
print(f"\n✓ Python reads: from_python = {value}")

if value == 999.0:
    print("✓ SUCCESS! Python saw your change in MATLAB!")
else:
    print(f"  (You set it to {value})")

print("\n3. Now Python will change it back to 456...")
eng.workspace["from_python"] = 456.0
print("✓ Done! Check MATLAB Workspace - it should show 456 now!")

print("\n" + "=" * 70)
print("Session Information:")
print("=" * 70)
print(f"  Session Name: {session_name}")
print(f"  Created by: Python")
print(f"  Status: Running with GUI")
print(f"  Shared: Yes")

print("\n" + "=" * 70)
print("Keep Running or Close?")
print("=" * 70)
print("\n  Press Enter - MATLAB GUI stays open (Python disconnects)")
print("  Type 'close' - Close MATLAB GUI completely")

choice = input("\nYour choice: ").strip().lower()

if choice == "close":
    print("\nClosing MATLAB GUI...")
    eng.stop()
    print("✓ MATLAB closed")
else:
    print("\n✓ MATLAB GUI remains open!")
    print(f"\nTo reconnect from Python later:")
    print(f"  from matlab_mcp_server.engine import MatlabEngine")
    print(f"  eng = MatlabEngine.connect_to_shared('{session_name}')")
    print("\nOr use CLI:")
    print(f"  .venv/bin/matlab-cli -c \"disp('Still connected!')\"")
    print("\nClose MATLAB GUI manually when you're done.")

print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
