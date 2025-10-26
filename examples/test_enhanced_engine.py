#!/usr/bin/env python3
"""Test the enhanced MatlabEngine with workspace methods."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from matlab_mcp_server.engine import MatlabEngine
from matlab import double as matlab_double


def main():
    print("=" * 60)
    print("Testing Enhanced MatlabEngine")
    print("=" * 60)

    with MatlabEngine() as engine:
        # Test 1: Set and get variables
        print("\n1. Testing set_variable() and get_variable():")
        engine.set_variable("x", 42.0)
        engine.set_variable("y", 8.0)
        print(f"   Set x = 42, y = 8")
        print(f"   Get x = {engine.get_variable('x')}")
        print(f"   Get y = {engine.get_variable('y')}")

        # Test 2: Call function
        print("\n2. Testing call_function():")
        result = engine.call_function("sqrt", 16.0)
        print(f"   sqrt(16) = {result}")

        data = matlab_double([1.0, 5.0, 3.0, 9.0, 2.0])
        result = engine.call_function("max", data, nargout=2)
        print(f"   max([1,5,3,9,2]) = {result}")

        # Test 3: List workspace
        print("\n3. Testing list_workspace():")
        workspace_info = engine.list_workspace()
        print(f"   Variables: {workspace_info['variables']}")

        # Test 4: Direct workspace access
        print("\n4. Testing workspace property:")
        engine.workspace["z"] = 100.0
        print(f"   Set z = 100 via workspace property")
        print(f"   Get z = {engine.workspace['z']}")

        # Test 5: Clear specific variables
        print("\n5. Testing clear_workspace() with specific variables:")
        print("   Before clear:")
        print(f"   {engine.list_workspace()['variables']}")
        engine.clear_workspace("x", "y")
        print("   After clearing x and y:")
        print(f"   {engine.list_workspace()['variables']}")

        # Test 6: Execute code
        print("\n6. Testing execute() method:")
        result = engine.execute("a = magic(3); disp(a)")
        print(f"   Output:\n{result['output']}")

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
