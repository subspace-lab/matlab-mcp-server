#!/usr/bin/env python3
"""
Setup script to add demo content to currently running MATLAB GUI.

Instructions:
1. Open MATLAB GUI manually
2. In MATLAB Command Window, type:
   >> matlab.engine.shareEngine('MyMATLAB')
3. Run this script
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine

print("=" * 70)
print("Setup Current MATLAB Session")
print("=" * 70)

# Find sessions
print("\n1. Searching for shared MATLAB sessions...")
sessions = MatlabEngine.find_shared_sessions()

if not sessions:
    print("\n❌ No shared MATLAB sessions found!")
    print("\nTo create one:")
    print("  1. Open MATLAB GUI")
    print("  2. In Command Window, type:")
    print("     >> matlab.engine.shareEngine('MyMATLAB')")
    print("  3. Run this script again")
    sys.exit(1)

print(f"\n✓ Found {len(sessions)} session(s):")
for i, session in enumerate(sessions, 1):
    print(f"   {i}. {session}")

# Connect to first session
session_name = sessions[0]
print(f"\n2. Connecting to: {session_name}")

try:
    engine = MatlabEngine.connect_to_shared(session_name)
    print("   ✓ Connected!")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Set up variables
print("\n3. Setting up demo variables...")
engine.workspace["demo_var"] = 42.0
engine.workspace["python_message"] = "Hello from Python!"
engine.workspace["data"] = [1.0, 4.0, 9.0, 16.0, 25.0]

print("   ✓ Variables created:")
print("      - demo_var = 42")
print("      - python_message = 'Hello from Python!'")
print("      - data = [1, 4, 9, 16, 25]")

# Display in MATLAB
print("\n4. Sending message to MATLAB Command Window...")
engine.execute(
    """
    fprintf('\\n');
    fprintf('=================================\\n');
    fprintf('  Python Connected Successfully! \\n');
    fprintf('=================================\\n');
    fprintf('\\n');
    fprintf('New variables added:\\n');
    fprintf('  demo_var = %.0f\\n', demo_var);
    fprintf('  python_message = %s\\n', python_message);
    fprintf('  data = [%.0f %.0f %.0f %.0f %.0f]\\n', data(1), data(2), data(3), data(4), data(5));
    fprintf('\\n');
    fprintf('Try these commands:\\n');
    fprintf('  >> who\\n');
    fprintf('  >> demo_var * 2\\n');
    fprintf('  >> plot(data)\\n');
    fprintf('\\n');
    fprintf('=================================\\n');
    fprintf('\\n');
""",
    nargout=0,
)

# Create a plot
print("\n5. Creating a plot in MATLAB...")
engine.execute(
    """
    figure('Name', 'Python Created This');
    subplot(2,1,1);
    plot(data, 'ro-', 'LineWidth', 2, 'MarkerSize', 10);
    title('Data from Python');
    xlabel('Index'); ylabel('Value');
    grid on;

    subplot(2,1,2);
    bar(data);
    title('Bar Chart');
    xlabel('Index'); ylabel('Value');
""",
    nargout=0,
)

print("   ✓ Plot created!")

print("\n" + "=" * 70)
print("✓ Setup Complete!")
print("=" * 70)
print("\nCheck your MATLAB GUI window:")
print("  1. Command Window - should show message")
print("  2. Workspace - should have new variables")
print("  3. Figure - should show plots")

print("\n" + "=" * 70)
print("Now you can:")
print("=" * 70)
print("\n1. In MATLAB GUI, type:")
print("   >> who")
print("   >> demo_var")
print("   >> demo_var = 100  % Change it")

print("\n2. From Python, check the change:")
print("   >>> from matlab_mcp_server.engine import MatlabEngine")
print(f"   >>> eng = MatlabEngine.connect_to_shared('{session_name}')")
print("   >>> eng.get_variable('demo_var')  # Should show 100")

print("\n3. Python can modify it back:")
print("   >>> eng.set_variable('demo_var', 999)")
print("   Then in MATLAB type: demo_var")

print("\n" + "=" * 70)
print("Session remains open - close MATLAB GUI when done")
print("=" * 70)
