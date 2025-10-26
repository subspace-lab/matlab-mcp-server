#!/usr/bin/env python3
"""
Demonstration of connecting to and using shared MATLAB sessions.

A shared session allows you to:
1. See the MATLAB GUI while Python controls it
2. Connect Python to an already-running MATLAB GUI
3. Share variables between GUI and Python
"""

import matlab.engine
import sys
import time


def demo_start_shared_session():
    """Start a new MATLAB session that is shared (allows GUI visibility)."""
    print("=" * 70)
    print("Demo 1: Starting a Shared MATLAB Session")
    print("=" * 70)

    print("\n1. Starting a shared MATLAB session...")
    print("   This will open MATLAB GUI if not already running.")

    # Start MATLAB with desktop (GUI)
    eng = matlab.engine.start_matlab("-desktop")

    print("\n2. Making the session shared...")
    # Convert to shared session with a custom name
    eng.eval("matlab.engine.shareEngine('MyPythonSession')", nargout=0)

    print("   ✓ Session is now shared with name: 'MyPythonSession'")
    print("\n3. You should now see the MATLAB GUI window!")
    print("   The command window will show this is a shared session.")

    print("\n4. Executing code from Python...")
    eng.workspace["x"] = 42.0
    eng.eval("fprintf('Hello from Python! x = %d\\n', x)", nargout=0)
    eng.eval("disp('You should see this in the MATLAB GUI command window!')", nargout=0)

    print("\n5. Creating a plot (will appear in MATLAB GUI)...")
    eng.eval("figure; plot(1:10, (1:10).^2); title('Plot from Python')", nargout=0)

    print("\n6. Try interacting with MATLAB GUI:")
    print("   - Type 'who' in the command window to see variable 'x'")
    print("   - Type 'x' to see its value (42)")
    print("   - The plot window should be visible")

    input("\nPress Enter to continue...")

    print("\n7. Closing shared session...")
    eng.quit()
    print("   ✓ Session closed")
    print()


def demo_connect_to_running_gui():
    """Connect to a MATLAB GUI that's already running."""
    print("=" * 70)
    print("Demo 2: Connecting to a Running MATLAB GUI")
    print("=" * 70)

    print("\nBefore running this demo:")
    print("1. Open MATLAB GUI manually")
    print("2. In the MATLAB command window, type:")
    print("   >> matlab.engine.shareEngine('MyGUI')")
    print("3. Then run this Python script")

    input("\nPress Enter when you've done the above...")

    print("\nSearching for shared MATLAB sessions...")
    sessions = matlab.engine.find_matlab()

    if not sessions:
        print("❌ No shared sessions found!")
        print("\nDid you run 'matlab.engine.shareEngine' in MATLAB?")
        return

    print(f"✓ Found {len(sessions)} shared session(s):")
    for i, session in enumerate(sessions, 1):
        print(f"  {i}. {session}")

    print(f"\nConnecting to: {sessions[0]}")
    eng = matlab.engine.connect_matlab(sessions[0])

    print("✓ Connected to MATLAB GUI session!")

    print("\nSending commands to the GUI from Python...")
    eng.workspace["python_var"] = 100.0
    eng.eval("disp('Message from Python!')", nargout=0)
    eng.eval("fprintf('Python set python_var = %d\\n', python_var)", nargout=0)

    print("\nCheck your MATLAB GUI - you should see these messages!")
    print("Also try typing 'python_var' in the MATLAB command window")

    input("\nPress Enter to disconnect (MATLAB will stay open)...")

    # Note: We don't call quit() because we want to leave the GUI open
    print("Disconnected. MATLAB GUI is still running!")
    print()


def demo_bidirectional_interaction():
    """Show bidirectional interaction between Python and MATLAB GUI."""
    print("=" * 70)
    print("Demo 3: Bidirectional Interaction")
    print("=" * 70)

    print("\n1. Starting shared MATLAB session...")
    eng = matlab.engine.start_matlab("-desktop")
    eng.eval("matlab.engine.shareEngine('BiDirectional')", nargout=0)

    print("\n2. Python sets initial values...")
    eng.workspace["counter"] = 0.0
    eng.workspace["data"] = matlab.double([1, 2, 3, 4, 5])

    print("\n3. Now you can:")
    print("   a) In Python: we'll increment the counter")
    print("   b) In MATLAB GUI: you can modify variables")
    print()

    for i in range(5):
        # Python increments counter
        current = eng.workspace["counter"]
        eng.workspace["counter"] = current + 1

        print(f"   Python: Incremented counter to {eng.workspace['counter']}")
        print(f"   Python: data = {eng.workspace['data']}")
        print("   (You can modify 'data' in MATLAB GUI during this time)")
        time.sleep(2)

    print("\n4. Final values:")
    print(f"   counter = {eng.workspace['counter']}")
    print(f"   data = {eng.workspace['data']}")

    print("\n5. Creating a visualization in MATLAB GUI...")
    eng.eval(
        """
        figure;
        subplot(2,1,1);
        bar(data);
        title('Data Array');

        subplot(2,1,2);
        plot(1:counter, 1:counter, 'o-');
        title(sprintf('Counter Progression (n=%d)', counter));
    """,
        nargout=0,
    )

    input("\nPress Enter to close...")
    eng.quit()
    print()


def demo_find_and_list_sessions():
    """Utility to find and list all shared MATLAB sessions."""
    print("=" * 70)
    print("Utility: Find All Shared MATLAB Sessions")
    print("=" * 70)

    print("\nSearching for shared MATLAB sessions...")
    sessions = matlab.engine.find_matlab()

    if not sessions:
        print("No shared MATLAB sessions found.")
        print("\nTo create a shared session:")
        print("  Option 1: In MATLAB GUI, run: matlab.engine.shareEngine")
        print("  Option 2: In Python: eng = matlab.engine.start_matlab('-desktop')")
        print("           then: eng.eval('matlab.engine.shareEngine', nargout=0)")
    else:
        print(f"\nFound {len(sessions)} shared session(s):\n")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")

            try:
                # Try to connect and get info
                eng = matlab.engine.connect_matlab(session)

                # Check if we can get workspace info
                import io

                out = io.StringIO()
                eng.who(nargout=0, stdout=out)
                vars_list = out.getvalue().strip()

                if vars_list:
                    print(f"     Variables: {vars_list}")
                else:
                    print(f"     Workspace: Empty")

                # Get MATLAB version
                version = eng.version()
                print(f"     Version: {version}")
                print()

            except Exception as e:
                print(f"     (Could not connect: {e})")
                print()

    print()


def main():
    """Main menu for shared session demos."""
    while True:
        print("\n" + "=" * 70)
        print("MATLAB Shared Session Demos")
        print("=" * 70)
        print("\n1. Start a new shared MATLAB session (with GUI)")
        print("2. Connect to a running MATLAB GUI")
        print("3. Bidirectional interaction demo")
        print("4. Find and list all shared sessions")
        print("5. Quick info about shared sessions")
        print("0. Exit")

        choice = input("\nChoose an option (0-5): ").strip()

        if choice == "1":
            demo_start_shared_session()
        elif choice == "2":
            demo_connect_to_running_gui()
        elif choice == "3":
            demo_bidirectional_interaction()
        elif choice == "4":
            demo_find_and_list_sessions()
        elif choice == "5":
            print("\n" + "=" * 70)
            print("Quick Info: MATLAB Shared Sessions")
            print("=" * 70)
            print("""
How to create a shared session:

1. From MATLAB GUI:
   >> matlab.engine.shareEngine
   >> matlab.engine.shareEngine('MySessionName')

2. From Python:
   import matlab.engine
   eng = matlab.engine.start_matlab('-desktop')
   eng.eval('matlab.engine.shareEngine', nargout=0)

3. Start MATLAB with sharing enabled:
   $ matlab -r "matlab.engine.shareEngine"

How to find shared sessions:

   import matlab.engine
   sessions = matlab.engine.find_matlab()
   print(sessions)  # ('MATLAB_12345', 'MySessionName', ...)

How to connect to a shared session:

   eng = matlab.engine.connect_matlab('MySessionName')
   # Or connect to first available:
   eng = matlab.engine.connect_matlab()

Benefits:
   ✓ See MATLAB GUI while Python controls it
   ✓ Manually interact with variables in GUI
   ✓ View plots and figures as they're created
   ✓ Debug MATLAB code visually
   ✓ Use MATLAB's debugging tools
            """)
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
