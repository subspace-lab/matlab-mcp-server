#!/usr/bin/env python3
"""
Test the enhanced MatlabEngine with shared session support.

This demonstrates:
1. Starting MATLAB with GUI visible
2. Making sessions shared
3. Finding and connecting to shared sessions
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from matlab_mcp_server.engine import MatlabEngine


def test_start_with_gui():
    """Test starting MATLAB with GUI visible."""
    print("=" * 70)
    print("Test 1: Start MATLAB with GUI")
    print("=" * 70)

    print("\n1. Starting MATLAB with desktop GUI...")
    engine = MatlabEngine()
    engine.start(desktop=True)
    print("   ✓ MATLAB GUI should now be visible")

    print("\n2. Making it a shared session...")
    session_name = engine.make_shared("TestGUI")
    print(f"   ✓ Shared session name: {session_name}")

    print("\n3. Setting variables (check MATLAB workspace browser)...")
    engine.set_variable("test_var", 42.0)
    engine.set_variable("message", "Hello from Python!")
    print("   ✓ Variables set: test_var=42, message='Hello from Python!'")

    print("\n4. Executing code (check MATLAB command window)...")
    result = engine.execute("""
        fprintf('\\n=== Message from Python ===\\n');
        fprintf('test_var = %d\\n', test_var);
        fprintf('message = %s\\n', message);
        fprintf('===========================\\n\\n');
    """)

    print("\n5. Creating a plot (will appear in MATLAB)...")
    engine.execute("""
        figure('Name', 'Plot from Python');
        x = 0:0.1:10;
        y = sin(x);
        plot(x, y, 'b-', 'LineWidth', 2);
        title('Sine Wave - Created from Python');
        xlabel('x'); ylabel('sin(x)'); grid on;
    """)
    print("   ✓ Plot created")

    print("\n" + "=" * 70)
    print("Check your MATLAB GUI!")
    print("=" * 70)
    print("You should see:")
    print("  • Variables in the Workspace browser")
    print("  • Messages in the Command Window")
    print("  • A plot window with a sine wave")

    input("\nPress Enter to continue...")

    print("\nClosing MATLAB...")
    engine.stop()
    print("✓ Done\n")


def test_find_sessions():
    """Test finding shared sessions."""
    print("=" * 70)
    print("Test 2: Find Shared Sessions")
    print("=" * 70)

    print("\n1. Searching for shared MATLAB sessions...")
    sessions = MatlabEngine.find_shared_sessions()

    if sessions:
        print(f"   ✓ Found {len(sessions)} session(s):")
        for i, session in enumerate(sessions, 1):
            print(f"      {i}. {session}")
    else:
        print("   ℹ No shared sessions found")
        print("\n   To create one, run this in MATLAB:")
        print("      >> matlab.engine.shareEngine('MySession')")

    print()


def test_connect_to_shared():
    """Test connecting to a shared session."""
    print("=" * 70)
    print("Test 3: Connect to Shared Session")
    print("=" * 70)

    # First create a shared session
    print("\n1. Creating a shared session...")
    engine1 = MatlabEngine()
    engine1.start(desktop=True)
    session_name = engine1.make_shared("ConnectTest")
    print(f"   ✓ Created session: {session_name}")

    # Set some variables
    print("\n2. Setting variables in the session...")
    engine1.set_variable("shared_data", 100.0)
    print("   ✓ Set shared_data = 100")

    print("\n3. Connecting to the shared session from another instance...")
    engine2 = MatlabEngine.connect_to_shared("ConnectTest")
    print("   ✓ Connected!")

    print("\n4. Reading variable from the shared session...")
    value = engine2.get_variable("shared_data")
    print(f"   ✓ Read shared_data = {value}")

    print("\n5. Modifying variable from second connection...")
    engine2.set_variable("shared_data", 200.0)
    print("   ✓ Set shared_data = 200")

    print("\n6. Reading modified value from first connection...")
    value = engine1.get_variable("shared_data")
    print(f"   ✓ Read shared_data = {value}")

    print("\n✓ Both connections share the same workspace!")

    print("\nNote: MATLAB GUI is still open. Check the workspace!")
    input("Press Enter to close...")

    engine1.stop()
    print("\n✓ Done\n")


def test_bidirectional():
    """Test bidirectional Python-MATLAB interaction."""
    print("=" * 70)
    print("Test 4: Bidirectional Interaction")
    print("=" * 70)

    print("\n1. Starting MATLAB with GUI...")
    engine = MatlabEngine()
    engine.start(desktop=True)
    engine.make_shared("BiDirectional")

    print("\n2. Python sets initial values...")
    engine.set_variable("counter", 0.0)
    print("   ✓ Set counter = 0")

    print("\n" + "=" * 70)
    print("INTERACTIVE DEMO")
    print("=" * 70)
    print("\nNow do this:")
    print("1. In MATLAB GUI, type: counter = counter + 10")
    print("2. Press Enter in MATLAB")
    print("3. Then come back here and press Enter")

    input("\nPress Enter after you've modified 'counter' in MATLAB...")

    print("\n3. Reading value back from MATLAB...")
    value = engine.get_variable("counter")
    print(f"   ✓ Python sees counter = {value}")

    print("\n4. Python increments it again...")
    engine.set_variable("counter", value + 5)
    print(f"   ✓ Python set counter = {value + 5}")

    print("\n5. Check MATLAB workspace - counter should be updated!")
    print("   Type 'counter' in MATLAB command window to verify.")

    input("\nPress Enter to close...")
    engine.stop()
    print("\n✓ Done\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("MATLAB Shared Session Tests")
    print("=" * 70)

    tests = [
        ("Start MATLAB with GUI", test_start_with_gui),
        ("Find shared sessions", test_find_sessions),
        ("Connect to shared session", test_connect_to_shared),
        ("Bidirectional interaction", test_bidirectional),
    ]

    print("\nAvailable tests:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"  {i}. {name}")
    print("  5. Run all tests")
    print("  0. Exit")

    while True:
        choice = input("\nChoose a test (0-5): ").strip()

        if choice == "0":
            break
        elif choice == "5":
            for name, test_func in tests:
                print(f"\n\nRunning: {name}")
                try:
                    test_func()
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    import traceback

                    traceback.print_exc()
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(tests):
            name, test_func = tests[int(choice) - 1]
            try:
                test_func()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback

                traceback.print_exc()
        else:
            print("❌ Invalid choice")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
