.PHONY: help test test-unit test-integration test-e2e test-all test-coverage clean

help:
	@echo "MATLAB MCP Server - Development Commands"
	@echo ""
	@echo "Testing:"
	@echo "  make test              - Run unit and integration tests"
	@echo "  make test-unit         - Run unit tests only"
	@echo "  make test-integration  - Run integration tests only"
	@echo "  make test-e2e          - Run end-to-end tests only"
	@echo "  make test-all          - Run all tests (including E2E)"
	@echo "  make test-coverage     - Run tests with coverage report"
	@echo ""
	@echo "Development:"
	@echo "  make install           - Install dependencies"
	@echo "  make install-dev       - Install dev dependencies"
	@echo "  make clean             - Clean temporary files"
	@echo ""

# Installation
install:
	uv sync

install-dev:
	uv sync --dev

# Testing
test:
	uv run pytest tests/ -v

test-unit:
	uv run pytest tests/test_engine.py -v

test-integration:
	uv run pytest tests/test_server.py -v

test-e2e:
	uv run python examples/real_world_tests.py

test-all: test test-e2e

test-coverage:
	uv run pytest tests/ --cov=src/matlab_mcp_server --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated. Open htmlcov/index.html to view."

# Cleanup
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf src/matlab_mcp_server/__pycache__
	rm -rf temp/*.png temp/*.csv temp/*.mat
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned temporary files."
