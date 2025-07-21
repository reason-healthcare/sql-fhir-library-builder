# CI/CD Workflows

This project uses GitHub Actions for continuous integration, code quality assurance, and automated publishing.

## Workflows Overview

### 🧪 Tests (`test.yml`)
**Trigger**: Push to `main`, Pull Requests  
**Purpose**: Quick test validation for status badges
- Runs on Python 3.11
- Executes `make test-quick`
- Provides test status badge

### 🔍 Code Quality (`quality.yml`)
**Trigger**: Push to `main`, Pull Requests  
**Purpose**: Comprehensive code quality checks
- Tests multiple Python versions (3.8-3.12)
- Runs formatting checks (`make format-check`)
- Runs linting (`make lint`)
- Runs tests (`make test-quick`)
- Uploads test artifacts

**Matrix Strategy**: Tests across Python 3.8, 3.9, 3.10, 3.11, and 3.12

### 🚀 Demo & Examples (`demo.yml`)
**Trigger**: Push to `main`, Pull Requests, Weekly schedule  
**Purpose**: Validates examples and demo functionality
- Runs the complete demo (`python scripts/demo.py`)
- Validates demo outputs are generated
- Runs comprehensive test suite
- Uploads demo artifacts (retained for 30 days)

### 🔄 CI (`ci.yml`)
**Trigger**: Push to `main`/`develop`, Pull Requests  
**Purpose**: Basic continuous integration
- Tests on Python 3.8 and 3.11
- Validates package installation
- Ensures imports work correctly

### 📦 Publish (`publish.yml`)
**Trigger**: Release creation, Manual dispatch  
**Purpose**: Automated package publishing
- Builds distribution packages
- Publishes to Test PyPI (manual trigger)
- Publishes to PyPI (on release)
- Requires `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN` secrets

## Status Badges

The README includes badges for:
- [![Tests](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/test.yml/badge.svg)](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/test.yml) Test status
- [![Code Quality](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/quality.yml/badge.svg)](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/quality.yml) Code quality
- [![Demo](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/demo.yml/badge.svg)](https://github.com/reason-healthcare/sql-fhir-library-builder/actions/workflows/demo.yml) Demo functionality
- ![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg) Python compatibility
- [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) Code formatting

## Workflow Details

### Quality Pipeline
The quality workflow runs the complete development pipeline:

```yaml
steps:
  - Check code formatting (isort + Black)
  - Run linting (flake8)
  - Run tests (pytest)
  - Upload test results
```

### Artifact Retention
- **Test Results**: 7 days
- **Demo Outputs**: 30 days

### Branch Protection
Recommended branch protection rules for `main`:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Required checks:
  - `Test Python 3.11` (from ci.yml)
  - `Quick Validation` (from quality.yml)

## Local Development

Run the same checks locally:

```bash
# Complete quality pipeline
make quality

# Individual checks
make format-check  # Check formatting
make lint         # Run linting
make test-quick   # Run tests
```

## Secrets Required

For the publish workflow to work, add these secrets to your repository:
- `PYPI_API_TOKEN`: PyPI API token for production releases
- `TEST_PYPI_API_TOKEN`: Test PyPI API token for testing

## Manual Workflows

Some workflows can be triggered manually:

### Publish Workflow
- Go to Actions → Publish to PyPI → Run workflow
- This publishes to Test PyPI for validation

### Weekly Demo Run
- Scheduled to run weekly on Sundays
- Catches any drift in dependencies or examples

## Performance

Typical workflow runtimes:
- **Tests**: ~2-3 minutes
- **Quality (single Python version)**: ~3-4 minutes  
- **Quality (full matrix)**: ~15-20 minutes
- **Demo**: ~4-5 minutes
- **CI**: ~2-3 minutes

## Maintenance

### Dependency Updates
- Python version matrix should be updated as new Python versions are released
- GitHub Actions versions should be kept up to date
- Consider using Dependabot for automated updates

### Workflow Optimization
- Caching is configured for pip dependencies
- Matrix builds run in parallel
- Artifacts are automatically cleaned up per retention policy
