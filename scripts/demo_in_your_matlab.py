#!/usr/bin/env python3
"""Demo: Add content to your running MATLAB session."""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine

# Connect to your session
print("Connecting to MATLAB_98037...")
eng = MatlabEngine.connect_to_shared("MATLAB_98037")
print("✅ Connected!\n")

# Add a variable you can see
print("Setting demo_var = 42...")
eng.workspace["demo_var"] = 42.0
print("✅ Done - type 'demo_var' in MATLAB to see it\n")

# Add more variables
print("Adding more variables...")
eng.workspace["python_msg"] = "Hello from Python!"
eng.workspace["numbers"] = [1.0, 2.0, 3.0, 4.0, 5.0]
print("✅ Added: python_msg, numbers\n")

# Send a message to MATLAB Command Window
print("Sending message to MATLAB Command Window...")
eng.execute("""
fprintf('\\n');
fprintf('========================================\\n');
fprintf('   Python Just Connected to MATLAB!    \\n');
fprintf('========================================\\n');
fprintf('\\n');
fprintf('New variables added:\\n');
fprintf('  demo_var = %.0f\\n', demo_var);
fprintf('  python_msg = %s\\n', python_msg);
fprintf('  numbers = [%.0f %.0f %.0f %.0f %.0f]\\n', numbers(1), numbers(2), numbers(3), numbers(4), numbers(5));
fprintf('\\n');
fprintf('Try these commands:\\n');
fprintf('  >> who\\n');
fprintf('  >> demo_var\\n');
fprintf('  >> demo_var = 999  %% Change it!\\n');
fprintf('  >> plot(numbers)\\n');
fprintf('\\n');
fprintf('========================================\\n');
fprintf('\\n');
""")
print("✅ Check your MATLAB Command Window!\n")

# Create a plot
print("Creating a plot in your MATLAB...")
eng.execute("""
figure('Name', 'Demo from Python', 'NumberTitle', 'off');
x = 0:0.1:10;
y = sin(x);
plot(x, y, 'b-', 'LineWidth', 2);
title('Sine Wave - Created by Python!');
xlabel('x'); ylabel('sin(x)');
grid on;
""")
print("✅ Plot window should appear!\n")

print("=" * 60)
print("✅ Demo Complete!")
print("=" * 60)
print("\nCheck your MATLAB GUI:")
print("  1. Command Window - see the message")
print("  2. Workspace - see: demo_var, python_msg, numbers")
print("  3. Figure window - see the sine wave plot")
print("\nNow try in MATLAB:")
print("  >> demo_var")
print("  >> demo_var = 100")
print("\nYour MATLAB session (MATLAB_98037) is still running!")
