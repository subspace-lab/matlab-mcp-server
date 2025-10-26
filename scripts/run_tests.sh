#!/bin/bash
# Quick test runner for MATLAB MCP Server
# Usage: ./scripts/run_tests.sh [options]

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default options
RUN_UNIT=true
RUN_INTEGRATION=true
RUN_E2E=false
COVERAGE=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit-only)
            RUN_INTEGRATION=false
            RUN_E2E=false
            shift
            ;;
        --integration-only)
            RUN_UNIT=false
            RUN_E2E=false
            shift
            ;;
        --e2e-only)
            RUN_UNIT=false
            RUN_INTEGRATION=false
            RUN_E2E=true
            shift
            ;;
        --all)
            RUN_UNIT=true
            RUN_INTEGRATION=true
            RUN_E2E=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --unit-only         Run only unit tests"
            echo "  --integration-only  Run only integration tests"
            echo "  --e2e-only         Run only end-to-end tests"
            echo "  --all              Run all tests including E2E"
            echo "  --coverage         Generate coverage report"
            echo "  -v, --verbose      Verbose output"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run unit and integration tests"
            echo "  $0 --all --coverage   # Run all tests with coverage"
            echo "  $0 --unit-only -v     # Run unit tests with verbose output"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="uv run pytest"
if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src/matlab_mcp_server --cov-report=term-missing --cov-report=html"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MATLAB MCP Server - Test Runner${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Track overall success
OVERALL_SUCCESS=true

# Run unit tests
if [ "$RUN_UNIT" = true ]; then
    echo -e "${YELLOW}Running Unit Tests...${NC}"
    if $PYTEST_CMD tests/test_engine.py; then
        echo -e "${GREEN}✓ Unit tests passed${NC}"
        echo ""
    else
        echo -e "${RED}✗ Unit tests failed${NC}"
        echo ""
        OVERALL_SUCCESS=false
    fi
fi

# Run integration tests
if [ "$RUN_INTEGRATION" = true ]; then
    echo -e "${YELLOW}Running Integration Tests...${NC}"
    if $PYTEST_CMD tests/test_server.py; then
        echo -e "${GREEN}✓ Integration tests passed${NC}"
        echo ""
    else
        echo -e "${RED}✗ Integration tests failed${NC}"
        echo ""
        OVERALL_SUCCESS=false
    fi
fi

# Run end-to-end tests
if [ "$RUN_E2E" = true ]; then
    echo -e "${YELLOW}Running End-to-End Tests...${NC}"
    if uv run python examples/real_world_tests.py; then
        echo -e "${GREEN}✓ End-to-end tests passed${NC}"
        echo ""
    else
        echo -e "${RED}✗ End-to-end tests failed${NC}"
        echo ""
        OVERALL_SUCCESS=false
    fi
fi

# Coverage report message
if [ "$COVERAGE" = true ]; then
    echo -e "${YELLOW}Coverage report generated:${NC}"
    echo "  Terminal: See output above"
    echo "  HTML: Open htmlcov/index.html in your browser"
    echo ""
fi

# Final summary
echo -e "${GREEN}========================================${NC}"
if [ "$OVERALL_SUCCESS" = true ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
