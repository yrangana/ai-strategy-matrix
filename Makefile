# AI Strategy Matrix Builder Makefile

.PHONY: setup setup-dev run lint format format-black format-autopep8 clean test test-verbose coverage help sync-deps

# Default target
.DEFAULT_GOAL := help

# Python interpreter and package managers
PYTHON = python
PKG_MANAGER = uv

# Application settings
APP_FILE = main.py

help:
	@echo "AI Strategy Matrix Builder"
	@echo ""
	@echo "Usage:"
	@echo "  make setup         Install production dependencies"
	@echo "  make setup-dev      Install development dependencies"
	@echo "  make run           Run the Streamlit application"
	@echo "  make lint          Run pylint to check code quality"
	@echo "  make format        Format code with Black (default)"
	@echo "  make format-black   Format code with Black"
	@echo "  make format-autopep8 Format code with autopep8"
	@echo "  make test          Run tests"
	@echo "  make test-verbose  Run tests with verbose output"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make clean         Remove cache files and directories"
	@echo "  make help          Show this help message"

setup:
	$(PKG_MANAGER) pip install -e .

sync-deps:
	@echo "Syncing dependencies from pyproject.toml to requirements.txt..."
	$(PKG_MANAGER) pip freeze > requirements.txt

setup-dev:
	$(PKG_MANAGER) pip install -e ".[dev]"

run:
	streamlit run $(APP_FILE)

lint:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	pylint *.py tests/*.py

format: format-black

format-black:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	@echo "Formatting code with Black..."
	black *.py tests/*.py

format-autopep8:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	autopep8 --in-place --aggressive --aggressive *.py tests/*.py

test:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	pytest -xvs tests/

test-verbose:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	pytest -xvs tests/ -v

coverage:
	@echo "Ensuring development dependencies are installed..."
	$(PKG_MANAGER) pip install -e ".[dev]"
	pytest --cov=. tests/ --cov-report=term-missing

clean:
	@echo "Cleaning cache files and directories..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .streamlit/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type f -name "*.bak" -delete
	@echo "Cleaned!"
