#!/usr/bin/env python3
"""Start MATLAB with GUI and keep it running."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from matlab_mcp_server.engine import MatlabEngine

print("=" * 70)
print("Starting MATLAB with GUI...")
print("=" * 70)

engine = MatlabEngine()
engine.start(desktop=True)

print("\n✓ MATLAB GUI is starting/started!")
print("\nMaking it a shared session...")

session_name = engine.make_shared("PythonSession")
print(f"✓ Shared session created: {session_name}")

print("\n" + "=" * 70)
print("MATLAB GUI is now running!")
print("=" * 70)

print("\nSetting up some demo content...")

# Set some variables
engine.set_variable("demo_var", 42.0)
engine.set_variable("message", "Hello from Python!")

# Display message in MATLAB
engine.execute("""
    clc;  % Clear command window
    fprintf('\\n');
    fprintf('======================================\\n');
    fprintf('  MATLAB Session Started from Python  \\n');
    fprintf('======================================\\n');
    fprintf('\\n');
    fprintf('Session Name: %s\\n', matlab.engine.engineName);
    fprintf('Demo Variable: %.0f\\n', demo_var);
    fprintf('Message: %s\\n', message);
    fprintf('\\n');
    fprintf('You can now:\\n');
    fprintf('  • Type commands in this window\\n');
    fprintf('  • View variables in Workspace browser\\n');
    fprintf('  • Create plots and figures\\n');
    fprintf('  • Python can still control this session\\n');
    fprintf('\\n');
    fprintf('======================================\\n');
    fprintf('\\n');
""")

# Create a demo plot
engine.execute("""
    figure('Name', 'Demo Plot from Python', 'Position', [100, 100, 800, 600]);

    % Create subplots
    subplot(2, 2, 1);
    x = linspace(0, 2*pi, 100);
    plot(x, sin(x), 'b-', 'LineWidth', 2);
    title('Sine Wave');
    xlabel('x'); ylabel('sin(x)');
    grid on;

    subplot(2, 2, 2);
    plot(x, cos(x), 'r-', 'LineWidth', 2);
    title('Cosine Wave');
    xlabel('x'); ylabel('cos(x)');
    grid on;

    subplot(2, 2, 3);
    bar(1:5, [10, 25, 17, 30, 22]);
    title('Bar Chart');
    xlabel('Category'); ylabel('Value');

    subplot(2, 2, 4);
    data = randn(100, 1);
    histogram(data, 20);
    title('Random Data Distribution');
    xlabel('Value'); ylabel('Frequency');

    % Add overall title
    sgtitle('Demo Plots Created from Python', 'FontSize', 14, 'FontWeight', 'bold');
""")

print("\n✓ Demo content created!")
print("\n" + "=" * 70)
print("What you should see in MATLAB:")
print("=" * 70)
print("  1. Command Window - with welcome message")
print("  2. Workspace - variables: demo_var, message, x, data")
print("  3. Figure Window - with 4 demo plots")
print("\n" + "=" * 70)
print("Session Information")
print("=" * 70)
print(f"  Session Name: {session_name}")
print(f"  Status: Running")
print("\n" + "=" * 70)
print("What You Can Do Now")
print("=" * 70)
print("\n1. In MATLAB GUI:")
print("   • Type: who                    (list variables)")
print("   • Type: demo_var               (see value)")
print("   • Type: plot(x, tan(x))       (create new plot)")
print("   • Use GUI normally - it's fully functional!")
print("\n2. From Python (in another terminal):")
print("   • Connect with: engine = MatlabEngine.connect_to_shared('PythonSession')")
print("   • Run: .venv/bin/matlab-cli -c \"disp('Hi from CLI!')\"")
print("\n3. To keep MATLAB running:")
print("   • Just press Ctrl+C here - MATLAB will stay open")
print("   • Or press Enter to close MATLAB")

print("\n" + "=" * 70)

try:
    input("\nPress Enter to close MATLAB (or Ctrl+C to keep it open)...")
    print("\nClosing MATLAB...")
    engine.stop()
    print("✓ MATLAB closed")
except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("MATLAB GUI will remain open!")
    print("=" * 70)
    print(f"\nSession '{session_name}' is still running.")
    print("\nTo reconnect later from Python:")
    print(f"  from matlab_mcp_server.engine import MatlabEngine")
    print(f"  engine = MatlabEngine.connect_to_shared('{session_name}')")
    print("\nTo close MATLAB: Close the GUI window manually")
    print("=" * 70 + "\n")
