# Code Style and Formatting

This project uses modern Python formatting tools to ensure consistent, high-quality code.

## Tools

### Black - Code Formatter
- **Purpose**: Automatic code formatting
- **Configuration**: `pyproject.toml` - `[tool.black]` section
- **Line length**: 88 characters (Black's default)
- **Target**: Python 3.6+

### isort - Import Sorting
- **Purpose**: Automatically sort and organize imports
- **Configuration**: `pyproject.toml` - `[tool.isort]` section
- **Profile**: Black-compatible
- **First party**: `sql_fhir_library_generator`

### flake8 - Code Linting
- **Purpose**: Code quality checks (PEP 8 compliance, unused imports, etc.)
- **Max line length**: 88 characters (to match Black)
- **Ignored**: E203, W503 (Black compatibility)

## Quick Start

### Install Development Tools
```bash
# Install all development dependencies
pip install -e .[dev]

# Or install individually
pip install black isort flake8
```

### Format Code
```bash
# Format all code
make format

# Check formatting without changes
make format-check
```

### Run Quality Checks
```bash
# Run linting
make lint

# Run complete quality pipeline (format + lint + test)
make quality
```

## Makefile Commands

| Command | Purpose |
|---------|---------|
| `make format` | Run isort + Black to format code |
| `make format-check` | Check formatting without making changes |
| `make lint` | Run flake8 linting |
| `make quality` | Complete quality pipeline: format → lint → test |

## IDE Integration

### VS Code
Add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.sortImports.path": "isort",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### PyCharm
1. Install the Black plugin
2. Configure Black as the formatter: Settings → Tools → Black
3. Enable format on save: Settings → Tools → Actions on Save

## Configuration Details

### pyproject.toml - Black Configuration
```toml
[tool.black]
line-length = 88
target-version = ['py36']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs | \.git | \.hg | \.mypy_cache | \.tox | \.venv
  | build | dist
)/
'''
```

### pyproject.toml - isort Configuration
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["sql_fhir_library_generator"]
```

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Check code formatting
  run: make format-check

- name: Run linting
  run: make lint

- name: Run tests
  run: make test-quick
```

## Why These Tools?

1. **Black**: Uncompromising formatter that eliminates code style debates
2. **isort**: Keeps imports organized and consistent
3. **flake8**: Catches common code quality issues
4. **88-character limit**: Black's default, slightly more than PEP 8's 79

## Workflow

The recommended development workflow:
1. Write code
2. Run `make quality` before committing
3. All formatting and linting issues are resolved automatically
4. Tests pass, ensuring functionality is preserved

This ensures consistent, high-quality code across all contributors.
