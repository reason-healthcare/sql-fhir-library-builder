# Makefile for SQL FHIR Library Generator

.PHONY: help install test test-quick clean build check lint format format-check quality docs dev-install

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package"
	@echo "  dev-install  Install in development mode"
	@echo "  test         Run all tests"
	@echo "  test-quick   Run quick tests"
	@echo "  check        Check project health"
	@echo "  clean        Clean build artifacts and outputs"
	@echo "  build        Build distribution packages"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with isort and black"
	@echo "  format-check Check code formatting without changes"
	@echo "  quality      Run format + lint + test in sequence"
	@echo "  demo         Run feature demo"
	@echo ""
	@echo "Development workflow:"
	@echo "  make dev-install  # Set up development environment"
	@echo "  make test         # Run all tests"
	@echo "  make clean        # Clean up generated files"

# Installation
install:
	pip install .

dev-install:
	pip install -e .

# Testing
test:
	python scripts/run_all_tests.py

test-quick:
	python scripts/quick_test.py

# Individual test categories  
test-parser:
	python tests/test_parser.py

test-fhir:
	python tests/test_fhir_integration.py

test-dialect:
	python tests/test_sql_dialect.py

# Project health
check:
	@echo "🔍 Checking project structure..."
	@test -f src/sql_fhir_library_generator/__init__.py || (echo "❌ Package __init__.py missing" && exit 1)
	@test -f src/sql_fhir_library_generator/parser.py || (echo "❌ Parser module missing" && exit 1)
	@test -f src/sql_fhir_library_generator/fhir_builder.py || (echo "❌ FHIR builder module missing" && exit 1)
	@test -d tests || (echo "❌ Tests directory missing" && exit 1)
	@test -d examples || (echo "❌ Examples directory missing" && exit 1)
	@echo "✅ Project structure looks good"

# Code quality
lint:
	@echo "🔍 Running flake8..."
	@python -m flake8 src/sql_fhir_library_generator tests --max-line-length=88 --ignore=E203,W503 || echo "⚠️  Install flake8: pip install flake8"

format:
	@echo "🔧 Sorting imports with isort..."
	@python -m isort src/sql_fhir_library_generator tests scripts || echo "⚠️  Install isort: pip install isort"
	@echo "🎨 Formatting code with black..."
	@python -m black src/sql_fhir_library_generator tests scripts --line-length=88 || echo "⚠️  Install black: pip install black"

format-check:
	@echo "🔍 Checking import sorting..."
	@python -m isort src/sql_fhir_library_generator tests scripts --check-only --diff || echo "⚠️  Install isort: pip install isort"
	@echo "🔍 Checking code formatting..."
	@python -m black src/sql_fhir_library_generator tests scripts --line-length=88 --check --diff || echo "⚠️  Install black: pip install black"

# Cleaning
clean:
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf src/**/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf scripts/__pycache__/
	rm -rf .pytest_cache/
	rm -rf test_output/
	rm -rf fhir_libraries/
	rm -rf demo_output/
	rm -rf output/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*~" -delete
	@echo "✅ Cleanup complete"

# Building
build: clean
	@echo "📦 Building distribution packages..."
	python -m build
	@echo "✅ Build complete - check dist/ directory"

# Demo and documentation
demo:
	python scripts/demo.py

docs:
	@echo "📖 Documentation available in:"
	@echo "  - README.md"
	@echo "  - TESTING.md"
	@echo "  - examples/ directory"

# Development helpers
dev-setup: dev-install
	@echo "🛠️  Development setup complete!"
	@echo "💡 Try: make test"

# Package info
info:
	@echo "📊 Package Information:"
	@echo "  Name: sql-fhir-library-generator"
	@echo "  Version: 1.0.0"
	@echo "  Source: src/sql_fhir_library_generator/"
	@echo "  Tests: tests/"
	@echo "  Scripts: scripts/"
	@echo "  Examples: examples/"

# Quality assurance pipeline
quality: format lint test-quick
	@echo "✅ Quality pipeline complete!"
