.PHONY: help test test-unit test-integration test-e2e test-all test-coverage clean build publish-test publish release version-patch version-minor version-major

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
	@echo "Release:"
	@echo "  make version-patch     - Bump patch version (0.2.1 -> 0.2.2)"
	@echo "  make version-minor     - Bump minor version (0.2.1 -> 0.3.0)"
	@echo "  make version-major     - Bump major version (0.2.1 -> 1.0.0)"
	@echo "  make build             - Build distribution packages"
	@echo "  make publish-test      - Publish to TestPyPI"
	@echo "  make publish           - Publish to PyPI"
	@echo "  make release           - Full release: clean, test, build, publish"
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
	uv run --env-file .env python examples/essentials_demo.py

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
	rm -rf dist/
	rm -rf build/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned temporary files."

# Version management
version-patch:
	@echo "Bumping patch version..."
	@python -c "import re; \
	content = open('pyproject.toml').read(); \
	match = re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', content); \
	major, minor, patch = match.groups(); \
	new_version = f'{major}.{minor}.{int(patch)+1}'; \
	new_content = re.sub(r'version = \"\d+\.\d+\.\d+\"', f'version = \"{new_version}\"', content); \
	open('pyproject.toml', 'w').write(new_content); \
	print(f'Version bumped to {new_version}')"
	@uv lock
	@echo "Don't forget to commit the changes: git add pyproject.toml uv.lock && git commit -m 'Bump version'"

version-minor:
	@echo "Bumping minor version..."
	@python -c "import re; \
	content = open('pyproject.toml').read(); \
	match = re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', content); \
	major, minor, patch = match.groups(); \
	new_version = f'{major}.{int(minor)+1}.0'; \
	new_content = re.sub(r'version = \"\d+\.\d+\.\d+\"', f'version = \"{new_version}\"', content); \
	open('pyproject.toml', 'w').write(new_content); \
	print(f'Version bumped to {new_version}')"
	@uv lock
	@echo "Don't forget to commit the changes: git add pyproject.toml uv.lock && git commit -m 'Bump version'"

version-major:
	@echo "Bumping major version..."
	@python -c "import re; \
	content = open('pyproject.toml').read(); \
	match = re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', content); \
	major, minor, patch = match.groups(); \
	new_version = f'{int(major)+1}.0.0'; \
	new_content = re.sub(r'version = \"\d+\.\d+\.\d+\"', f'version = \"{new_version}\"', content); \
	open('pyproject.toml', 'w').write(new_content); \
	print(f'Version bumped to {new_version}')"
	@uv lock
	@echo "Don't forget to commit the changes: git add pyproject.toml uv.lock && git commit -m 'Bump version'"

# Build & Publish
build:
	@echo "Cleaning dist directory..."
	rm -rf dist/
	@echo "Building distribution packages..."
	uv build
	@echo "Build complete. Packages in dist/"

release: clean test-all build publish
	@echo ""
	@echo "=========================================="
	@echo "  Release Complete!"
	@echo "=========================================="
	@echo ""
	@VERSION=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	echo "Next steps:"; \
	echo "1. Create a git tag: git tag v$$VERSION"; \
	echo "2. Push the tag: git push origin v$$VERSION"; \
	echo "3. Create a GitHub release"; \
	echo ""
