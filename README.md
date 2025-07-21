# SQL FHIR Library Generator

A Python library that extracts `@annotations` from SQL file comments and creates FHIR Library resources.

## Features

- **Multiple Comment Styles**: Supports both single-line (`--`) and multi-line (`/* */`) SQL comments
- **Flexible Annotation Formats**: Handles various annotation syntaxes:
  - `@key value`
  - `@key: value` 
  - `@key = value`
- **Smart Type Conversion**: Automatically converts values to appropriate Python types (boolean, integer, float, lists)
- **Multiple Annotations**: Supports multiple annotations with the same key (collected into lists)
- **Batch Processing**: Can parse multiple SQL files at once
- **FHIR Library Generation**: Creates FHIR Library resources with base64-encoded SQL content
- **SQL Dialect Support**: Supports `@sqlDialect` annotation to customize content type (e.g., `application/hive+sql`)
- **Automatic Name Generation**: Generates PascalCase `name` field from `title` when `@name` annotation is not provided
- **Related Dependencies**: Handles `@relatedDependency` annotations and converts them to FHIR `relatedArtifact` entries
- **Error Handling**: Robust error handling for file operations and parsing

## Usage

### Basic Usage

```python
from sql_fhir_library_generator import SQLAnnotationParser

parser = SQLAnnotationParser()

# Parse a SQL file
annotations = parser.parse_file('path/to/your/file.sql')
print(annotations)

# Parse SQL content directly
sql_content = """
-- @author: John Doe
-- @version: 1.0
-- @tags: users, core
SELECT * FROM users;
"""
annotations = parser.parse_content(sql_content)
print(annotations)
```

### FHIR Library Generation

```python
from sql_fhir_library_generator import FHIRLibraryBuilder

builder = FHIRLibraryBuilder()

# Build FHIR Library from SQL file
library = builder.build_library_from_file('patient_queries.sql')
print(json.dumps(library, indent=2))

# Export to JSON file
builder.export_library_to_file(library, 'fhir_library.json')
```

### Related Dependencies

Use `@relatedDependency` annotations to specify FHIR resources this library depends on:

```sql
-- @relatedDependency: Library/patient-demographics
-- @relatedDependency: Questionnaire/patient-preferences
-- @relatedDependency: ValueSet/clinical-codes

/*
@relatedDependency: CodeSystem/observation-types
@relatedDependency: Library/common-functions
*/

SELECT * FROM patients;
```

This creates FHIR `relatedArtifact` entries with type "depends-on" and the specified resource references.

### SQL Dialect Support

Use the `@sqlDialect` annotation to specify the SQL dialect, which customizes the FHIR Library content type:

```sql
/*
@title: Hive Analytics Query
@description: Advanced analytics using Hive SQL features
@sqlDialect: hive
*/

-- Using Hive-specific syntax
SELECT 
    patient_id,
    regexp_extract(phone, '\\d{3}-(\\d{3})-(\\d{4})', 0) as formatted_phone
FROM patient_demographics
DISTRIBUTE BY patient_id
SORT BY patient_id;
```

This generates a FHIR Library with content type `application/hive+sql` instead of the default `application/sql`.

**Supported Dialects:**
- `@sqlDialect: hive` → `application/hive+sql`
- `@sqlDialect: spark` → `application/spark+sql`  
- `@sqlDialect: mysql` → `application/mysql+sql`
- `@sqlDialect: postgres` → `application/postgres+sql`
- `@sqlDialect: oracle` → `application/oracle+sql`
- `@sqlDialect: snowflake` → `application/snowflake+sql`
- Any custom dialect name → `application/{dialect}+sql`
- No annotation → `application/sql` (default)

### Automatic Name Generation

When no `@name` annotation is provided, the FHIR Library Builder automatically generates a PascalCase `name` from the `title`:

```sql
-- @title: Patient Demographics Query Library
-- @status: active

SELECT * FROM patients;
```

This generates:
```json
{
  "title": "Patient Demographics Query Library",
  "name": "PatientDemographicsQueryLibrary"
}
```

If you provide an explicit `@name`, it takes precedence:
```sql
-- @title: Patient Demographics Query Library  
-- @name: customPatientLibrary
```

### Example Annotations

The parser can extract various types of annotations, including multiple annotations with the same key:

```sql
-- @author: Database Team
-- @version: 2.1.0
-- @active: true
-- @priority: 5
-- @confidence: 0.95
-- @tags: users, authentication, core
-- @relatedDependency: Library/patient-demographics
-- @relatedDependency: Questionnaire/user-preferences

/*
@description: User authentication table with care coordination
@created: 2024-01-15
@performance_critical: true
@indexes: id, username, email
@relatedDependency: ValueSet/user-roles
@relatedDependency: CodeSystem/auth-methods
*/

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
```

This would extract:
```python
{
    'author': 'Database Team',
    'version': '2.1.0', 
    'active': True,
    'priority': 5,
    'confidence': 0.95,
    'tags': ['users', 'authentication', 'core'],
    'relatedDependency': [
        'Library/patient-demographics',
        'Questionnaire/user-preferences', 
        'ValueSet/user-roles',
        'CodeSystem/auth-methods'
    ],
    'description': 'User authentication table with care coordination',
    'created': '2024-01-15',
    'performance_critical': True,
    'indexes': ['id', 'username', 'email']
}
```

## Type Conversion

The parser automatically converts values to appropriate Python types:

- **Booleans**: `true`, `false`, `yes`, `no`, `on`, `off`, `1`, `0`
- **Numbers**: Integers and floats 
- **Lists**: Comma-separated values are converted to lists
- **Strings**: Default type, with automatic quote removal

## Project Structure

```
sql-fhir-library-generator/
├── src/
│   └── sql_fhir_library_generator/
│       ├── __init__.py          # Package initialization
│       ├── parser.py            # SQL annotation parser
│       └── fhir_builder.py      # FHIR Library builder
├── tests/                       # Test suite
│   ├── __init__.py             
│   ├── test_parser.py          # Core parser tests
│   ├── test_fhir_integration.py # FHIR integration tests
│   ├── test_sql_dialect.py     # SQL dialect tests
│   └── ...                     # Additional test modules
├── scripts/                    # Utility scripts
│   ├── demo.py                # Feature demonstration
│   ├── quick_test.py          # Quick test runner
│   └── run_all_tests.py       # Comprehensive test runner
├── examples/                  # Example SQL files
│   ├── users_schema.sql      # Database schema with annotations
│   ├── hive_example.sql      # Hive SQL dialect example
│   └── ...                   # Additional examples
├── setup.py                  # Package setup (legacy)
├── pyproject.toml           # Modern Python packaging
├── Makefile                 # Development commands
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Installation

### From Source (Development)

1. Clone this repository
2. Install in development mode:
   ```bash
   pip install -e .
   ```
   Or using make:
   ```bash
   make dev-install
   ```

### For Production Use

```bash
pip install sql-fhir-library-generator
```

### Quick Start

```bash
# Check project health
make check

# Run all tests
make test

# Quick validation
make test-quick

# Feature demonstration
make demo
```

## Testing

This project includes a comprehensive test suite with multiple ways to run tests:

### Run All Tests (Comprehensive)
```bash
make test
# or
python scripts/run_all_tests.py
```
This runs the complete test suite with detailed reporting, including:
- Core SQL annotation parser tests
- FHIR Library integration tests  
- Multiple dependencies support tests
- Automatic name generation tests
- Empty property removal tests
- SQL dialect annotation tests

### Quick Test Run
```bash
make test-quick
# or
python scripts/quick_test.py
```
Fast execution of all tests with minimal output - perfect for quick validation.

### Test Commands (Make-style)
```bash
# Run all tests
make test

# Quick tests  
make test-quick

# Test specific components
make test-parser
make test-fhir
make test-dialect

# Utility commands
make clean      # Clean output directories
make check      # Health check
make demo       # Run demo
```

### Individual Test Files
You can also run individual test files directly:
```bash
python tests/test_parser.py              # Test SQL annotation parsing
python tests/test_fhir_integration.py    # Test FHIR Library generation
python tests/test_sql_dialect.py         # Test SQL dialect support
python tests/test_multiple_dependencies.py  # Test multiple dependencies
python tests/test_name_generation.py     # Test automatic name generation
python tests/test_empty_properties.py    # Test empty property removal
```

### Test Outputs
All tests generate their outputs in organized directories:
- `test_output/` - Test-specific FHIR Library files
- `fhir_libraries/` - Main output directory for FHIR Libraries

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

MIT License
