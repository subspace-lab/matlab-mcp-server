#!/usr/bin/env python3
"""
Demonstration of MATLAB MCP Server Essential Tools
Shows how to use all the essential tools via the MCP protocol
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from matlab_mcp_server.engine import MatlabEngine
import json

def demo_execute_matlab():
    """Demo: execute_matlab tool"""
    print("\n" + "="*60)
    print("DEMO: execute_matlab")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Execute some MATLAB code
    result = engine.execute("""
        % Create some data
        x = linspace(0, 2*pi, 100);
        y = sin(x);
        fprintf('Computed sin(x) for %d points\\n', length(x));
    """)

    print(result['output'])
    engine.stop()

def demo_workspace():
    """Demo: workspace tool"""
    print("\n" + "="*60)
    print("DEMO: workspace tool")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Set some variables
    print("Setting variables...")
    engine.set_variable("my_array", [1, 2, 3, 4, 5])
    engine.set_variable("my_string", "Hello MATLAB")
    engine.set_variable("my_number", 42)

    # List workspace
    print("\nWorkspace contents:")
    ws = engine.list_workspace(detailed=True)
    print(json.dumps(ws, indent=2))

    # Get a variable
    print("\nGetting 'my_array':")
    value = engine.get_variable("my_array")
    print(f"Value: {value}")

    # Clear variables
    print("\nClearing workspace...")
    engine.clear_workspace()

    engine.stop()

def demo_figure():
    """Demo: figure tool"""
    print("\n" + "="*60)
    print("DEMO: figure tool")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Create a plot
    print("Creating plot...")
    engine.execute("""
        x = linspace(0, 4*pi, 200);
        y1 = sin(x);
        y2 = cos(x);
        figure(1);
        plot(x, y1, 'b-', x, y2, 'r--');
        title('Sine and Cosine');
        xlabel('x');
        ylabel('y');
        legend('sin(x)', 'cos(x)');
        grid on;
    """)

    # Save figure
    print("\nSaving figure...")
    result = engine.save_figure(fig_num=1, fmt="png", dpi=150)
    if result['success']:
        print(f"Figure saved to: {result['path']}")
    else:
        print(f"Error: {result['error']}")

    # Close figures
    print("\nClosing figures...")
    engine.close_figures()

    engine.stop()

def demo_data_io():
    """Demo: data_io tool"""
    print("\n" + "="*60)
    print("DEMO: data_io tool")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Create and save some data to MAT file
    print("Creating data and saving to MAT file...")
    import tempfile
    mat_file = os.path.join(tempfile.gettempdir(), "demo_data.mat")

    engine.execute("""
        data1 = rand(10, 5);
        data2 = magic(5);
        label = 'Demo Data';
    """)

    result = engine.save_mat_file(mat_file, variables=["data1", "data2", "label"])
    if result['success']:
        print(f"Saved to: {result['path']}")

    # Clear and reload
    print("\nClearing workspace and reloading...")
    engine.clear_workspace()

    result = engine.load_mat_file(mat_file)
    if result['success']:
        print(result['message'])

    # Verify loaded
    ws = engine.list_workspace()
    print(f"Loaded variables: {ws['variables']}")

    # Export to CSV (if we have a table)
    print("\nCreating and exporting table to CSV...")
    csv_file = os.path.join(tempfile.gettempdir(), "demo_table.csv")

    engine.execute("""
        T = table([1;2;3], [4;5;6], [7;8;9], ...
                  'VariableNames', {'A', 'B', 'C'});
    """)

    result = engine.export_data("T", csv_file, fmt="csv")
    if result['success']:
        print(f"Exported to: {result['path']}")

    engine.stop()

def demo_env():
    """Demo: env tool"""
    print("\n" + "="*60)
    print("DEMO: env tool")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Get version
    print("MATLAB Version:")
    result = engine.get_version()
    print(result['output'])

    # List toolboxes (first 5)
    print("\nInstalled Toolboxes (showing first 5):")
    result = engine.list_toolboxes()
    lines = result['output'].strip().split('\n')
    for line in lines[:5]:
        print(f"  {line}")
    print(f"  ... and {len(lines) - 5} more")

    # Check specific toolbox
    print("\nChecking for Signal Processing Toolbox:")
    result = engine.check_toolbox("Signal Processing Toolbox")
    print(f"  Installed: {result['installed']}")
    if result['installed']:
        print(f"  {result['output'].strip()}")

    engine.stop()

def demo_get_help():
    """Demo: get_help tool"""
    print("\n" + "="*60)
    print("DEMO: get_help tool")
    print("="*60)

    engine = MatlabEngine()
    engine.start()

    # Get help for a function
    print("Help for 'fft':")
    result = engine.get_help("fft", op="help")
    if result['success']:
        # Print first 300 chars
        output = result['output']
        print(output[:300] + "..." if len(output) > 300 else output)

    # Which command
    print("\n'which' for 'plot':")
    result = engine.get_help("plot", op="which")
    if result['success']:
        print(result['output'])

    # Lookfor
    print("\nSearching for 'fourier transform':")
    result = engine.get_help("fourier transform", op="lookfor")
    if result['success']:
        lines = result['output'].strip().split('\n')
        for line in lines[:5]:
            print(f"  {line}")
        if len(lines) > 5:
            print(f"  ... and {len(lines) - 5} more results")

    engine.stop()

def demo_all():
    """Run all demos"""
    print("\n" + "="*60)
    print("MATLAB MCP SERVER - ESSENTIAL TOOLS DEMO")
    print("="*60)

    demo_execute_matlab()
    demo_workspace()
    demo_figure()
    demo_data_io()
    demo_env()
    demo_get_help()

    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    try:
        demo_all()
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
