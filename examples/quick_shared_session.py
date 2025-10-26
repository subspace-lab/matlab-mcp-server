#!/usr/bin/env python3
"""
Quick example: Start MATLAB with GUI and control it from Python.

This is the simplest way to see MATLAB GUI while running Python code.
"""

import matlab.engine
import time

print("Starting MATLAB with GUI...")
print("(This will open the MATLAB desktop)")

# Start MATLAB with desktop/GUI visible
eng = matlab.engine.start_matlab("-desktop")

# Make it a shared session so we can reconnect if needed
eng.eval("matlab.engine.shareEngine('PythonControlled')", nargout=0)

print("\n✓ MATLAB GUI is now open!")
print("✓ Session name: 'PythonControlled'")
print("\nYou should see the MATLAB desktop window.")

# Now control MATLAB from Python while seeing the GUI
print("\n" + "=" * 60)
print("Controlling MATLAB from Python...")
print("=" * 60)

print("\n1. Setting variables (check MATLAB workspace)...")
eng.workspace["x"] = 10.0
eng.workspace["y"] = 20.0
eng.eval("z = x + y", nargout=0)
print("   Created variables x=10, y=20, z=30")

print("\n2. Displaying message in MATLAB command window...")
eng.eval("disp('Hello from Python! Check the command window.')", nargout=0)

print("\n3. Creating a plot (will appear in MATLAB)...")
eng.eval(
    """
    figure('Name', 'Plot from Python');
    x_plot = linspace(0, 2*pi, 100);
    y_plot = sin(x_plot);
    plot(x_plot, y_plot, 'b-', 'LineWidth', 2);
    title('Sine Wave - Created from Python');
    xlabel('x');
    ylabel('sin(x)');
    grid on;
""",
    nargout=0,
)

print("\n4. Creating a 3D surface plot...")
time.sleep(1)
eng.eval(
    """
    figure('Name', '3D Surface from Python');
    [X, Y] = meshgrid(-5:0.5:5);
    Z = sin(sqrt(X.^2 + Y.^2));
    surf(X, Y, Z);
    title('3D Surface - Created from Python');
    colorbar;
""",
    nargout=0,
)

print("\n" + "=" * 60)
print("Interactive Control")
print("=" * 60)
print("\nNow you can:")
print("  • See all variables in the MATLAB Workspace browser")
print("  • Type commands in the MATLAB Command Window")
print("  • Modify variables - they'll be visible to Python")
print("  • View and interact with the plots")
print()

# Let user interact
try:
    print("Try typing these in the MATLAB Command Window:")
    print("  >> who           % List all variables")
    print("  >> z             % See the value")
    print("  >> z = 100       % Change it")
    print()

    input("Press Enter to continue the demo...")

    # Read back any changes
    print("\n5. Reading variables back from MATLAB...")
    z_value = eng.workspace["z"]
    print(f"   z = {z_value} (Python read this from MATLAB)")

    print("\n6. Creating a data analysis example...")
    eng.eval(
        """
        % Generate random data
        data = randn(100, 1);

        % Display statistics
        fprintf('\\nData Statistics:\\n');
        fprintf('  Mean: %.4f\\n', mean(data));
        fprintf('  Std:  %.4f\\n', std(data));
        fprintf('  Min:  %.4f\\n', min(data));
        fprintf('  Max:  %.4f\\n', max(data));

        % Create histogram
        figure('Name', 'Data Analysis from Python');
        histogram(data, 20);
        title('Random Data Distribution');
        xlabel('Value');
        ylabel('Frequency');
    """,
        nargout=0,
    )

    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nThe MATLAB GUI will remain open.")
    print("You can:")
    print("  • Continue using MATLAB GUI normally")
    print("  • Python script will now disconnect")
    print("  • Close MATLAB GUI manually when done")
    print()

    input("Press Enter to disconnect Python (MATLAB stays open)...")

    # Don't quit - just disconnect
    print("\n✓ Python disconnected")
    print("✓ MATLAB GUI is still running")
    print("✓ You can close it manually or reconnect later with:")
    print("    eng = matlab.engine.connect_matlab('PythonControlled')")

except KeyboardInterrupt:
    print("\n\nInterrupted. MATLAB GUI will stay open.")
    print("Close it manually if needed.")
