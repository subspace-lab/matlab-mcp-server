#!/usr/bin/env python3
"""
Quick test runner for MATLAB MCP Server
Cross-platform Python version
"""

import argparse
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

    @classmethod
    def green(cls, text):
        return f"{cls.GREEN}{text}{cls.NC}"

    @classmethod
    def yellow(cls, text):
        return f"{cls.YELLOW}{text}{cls.NC}"

    @classmethod
    def red(cls, text):
        return f"{cls.RED}{text}{cls.NC}"


def run_command(cmd, description):
    """Run a command and return success status."""
    print(Colors.yellow(f"\n{description}..."))
    try:
        result = subprocess.run(cmd, check=True, shell=isinstance(cmd, str))
        print(Colors.green(f"✓ {description} passed"))
        return True
    except subprocess.CalledProcessError:
        print(Colors.red(f"✗ {description} failed"))
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test runner for MATLAB MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run unit and integration tests
  %(prog)s --all --coverage   # Run all tests with coverage
  %(prog)s --unit-only -v     # Run unit tests with verbose output
        """
    )

    parser.add_argument(
        '--unit-only',
        action='store_true',
        help='Run only unit tests'
    )
    parser.add_argument(
        '--integration-only',
        action='store_true',
        help='Run only integration tests'
    )
    parser.add_argument(
        '--e2e-only',
        action='store_true',
        help='Run only end-to-end tests'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all tests including E2E'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Determine which tests to run
    if args.unit_only:
        run_unit, run_integration, run_e2e = True, False, False
    elif args.integration_only:
        run_unit, run_integration, run_e2e = False, True, False
    elif args.e2e_only:
        run_unit, run_integration, run_e2e = False, False, True
    elif args.all:
        run_unit, run_integration, run_e2e = True, True, True
    else:
        # Default: unit and integration
        run_unit, run_integration, run_e2e = True, True, False

    # Build pytest command
    pytest_cmd = ["uv", "run", "pytest"]
    if args.verbose:
        pytest_cmd.append("-v")
    if args.coverage:
        pytest_cmd.extend([
            "--cov=src/matlab_mcp_server",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])

    # Print header
    print(Colors.green("=" * 60))
    print(Colors.green("MATLAB MCP Server - Test Runner"))
    print(Colors.green("=" * 60))

    # Track overall success
    overall_success = True

    # Run tests
    if run_unit:
        cmd = pytest_cmd + ["tests/test_engine.py"]
        if not run_command(cmd, "Running Unit Tests"):
            overall_success = False

    if run_integration:
        cmd = pytest_cmd + ["tests/test_server.py"]
        if not run_command(cmd, "Running Integration Tests"):
            overall_success = False

    if run_e2e:
        cmd = ["uv", "run", "python", "examples/real_world_tests.py"]
        if not run_command(cmd, "Running End-to-End Tests"):
            overall_success = False

    # Coverage report message
    if args.coverage:
        print(Colors.yellow("\nCoverage report generated:"))
        print("  Terminal: See output above")
        print("  HTML: Open htmlcov/index.html in your browser")

    # Final summary
    print(Colors.green("\n" + "=" * 60))
    if overall_success:
        print(Colors.green("All tests passed! 🎉"))
        return 0
    else:
        print(Colors.red("Some tests failed. Please review the output above."))
        return 1


if __name__ == "__main__":
    sys.exit(main())
