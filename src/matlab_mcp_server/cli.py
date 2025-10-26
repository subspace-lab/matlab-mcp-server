"""Command-line interface for MATLAB MCP server."""

import argparse
import sys
from pathlib import Path
from .engine import MatlabEngine


def execute_command(engine: MatlabEngine, code: str, verbose: bool = False) -> int:
    """
    Execute a MATLAB command and display results.

    Args:
        engine: MATLAB engine instance
        code: MATLAB code to execute
        verbose: Whether to show verbose output

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if verbose:
        print(f"Executing: {code}")
        print("-" * 60)

    result = engine.execute(code)

    if result["error"]:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1
    else:
        if result["output"]:
            print(result["output"])
        return 0


def execute_file(engine: MatlabEngine, filepath: Path, verbose: bool = False) -> int:
    """
    Execute a MATLAB script file.

    Args:
        engine: MATLAB engine instance
        filepath: Path to MATLAB script
        verbose: Whether to show verbose output

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1

    if verbose:
        print(f"Executing file: {filepath}")
        print("-" * 60)

    try:
        code = filepath.read_text()
        return execute_command(engine, code, verbose=False)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1


def interactive_mode(engine: MatlabEngine):
    """
    Start an interactive REPL for MATLAB commands.

    Args:
        engine: MATLAB engine instance
    """
    print("MATLAB Interactive Mode")
    print("Type 'exit' or 'quit' to exit, 'help' for help")
    print("-" * 60)

    while True:
        try:
            # Read input
            code = input("matlab> ").strip()

            # Handle special commands
            if code.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            if code.lower() == "help":
                print("""
Available commands:
  exit, quit  - Exit interactive mode
  help        - Show this help message

Type any MATLAB code to execute it.
""")
                continue

            if not code:
                continue

            # Execute the code
            result = engine.execute(code)

            if result["error"]:
                print(f"Error: {result['error']}")
            elif result["output"]:
                print(result["output"])

        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
            continue
        except EOFError:
            print("\nExiting...")
            break


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MATLAB MCP Server CLI - Execute MATLAB code from command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a command
  matlab-cli -c "disp('Hello, MATLAB!')"

  # Execute a script file
  matlab-cli -f script.m

  # Interactive mode
  matlab-cli -i

  # Verbose output
  matlab-cli -c "x = 1:10; mean(x)" -v
""",
    )

    parser.add_argument("-c", "--command", type=str, help="MATLAB command to execute")

    parser.add_argument("-f", "--file", type=Path, help="MATLAB script file to execute")

    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive REPL mode"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Check for at least one mode
    if not any([args.command, args.file, args.interactive]):
        parser.print_help()
        return 1

    # Initialize MATLAB engine
    if args.verbose:
        print("Starting MATLAB engine...")

    try:
        with MatlabEngine() as engine:
            if args.verbose:
                print("MATLAB engine started successfully\n")

            # Execute based on mode
            if args.command:
                return execute_command(engine, args.command, args.verbose)

            elif args.file:
                return execute_file(engine, args.file, args.verbose)

            elif args.interactive:
                interactive_mode(engine)
                return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
