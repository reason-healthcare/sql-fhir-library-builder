# Test & Demo Scripts Reference

This document listTests the core SQL annotation parsing functionality including multiple annotation formats, type conversion, and batch processing.

### FHIR Integration Testing  
```bash
python tests/test_fhir_integration.py
```
Tests FHIR Library resource generation, base64 encoding of SQL content, and proper FHIR structure compliance.vailable test and demo scripts for the SQL FHIR Library Generator project.

## 🧪 Test Scripts

### Comprehensive Test Suite
```bash
python run_all_tests.py
```
- **Purpose**: Complete test suite with detailed reporting
- **Features**: 
  - Runs all 6 test modules
  - Comprehensive error reporting  
  - Execution timing
  - Output file verification
  - Cleanup of previous test outputs
- **Output**: Detailed test results with success/failure summary

### Quick Test Runner
```bash
python quick_test.py
```
- **Purpose**: Fast validation of all functionality
- **Features**:
  - Minimal output for speed
  - All tests in under 30 seconds
  - Simple pass/fail reporting
- **Use Case**: Continuous integration, quick validation

### Test Commands (Make-style)
```bash
python test_commands.py [command]
```

**Available Commands:**
- `test` - Run comprehensive test suite
- `test-quick` - Run quick tests
- `test-parser` - Test only SQL annotation parser
- `test-fhir` - Test only FHIR integration  
- `test-dialect` - Test only SQL dialect support
- `clean` - Clean output directories
- `demo` - Run integration demo
- `check` - Health check of project files

## 🎯 Individual Test Files

### Core Parser Testing
```bash
python test_parser.py
```
Tests the core SQL annotation parsing functionality including multiple annotation formats, type conversion, and batch processing.

### FHIR Integration Testing  
```bash
python test_fhir_integration.py
```
Tests FHIR Library resource generation, base64 encoding of SQL content, and proper FHIR structure compliance.

### SQL Dialect Testing
```bash
python test_sql_dialect.py
```
Tests the `@sqlDialect` annotation feature that modifies content types (e.g., `application/sql; dialect=hive`).

### Dialect Version Testing
```bash
python test_dialect_version.py
```
Tests the `@dialectVersion` annotation feature that adds version parameters to MIME types (e.g., `application/sql; dialect=hive; version=3.1.2`).

### Multiple Dependencies Testing
```bash
python test_multiple_dependencies.py
```
Tests support for multiple `@relatedDependency` annotations and their conversion to FHIR `relatedArtifact` entries.

### Name Generation Testing
```bash
python test_name_generation.py
```
Tests automatic PascalCase name generation from titles when `@name` annotation is not provided.

### Empty Properties Testing
```bash
python test_empty_properties.py
```
Tests the removal of empty properties from generated FHIR resources for cleaner output.

## 🚀 Demo Scripts

### Comprehensive Feature Demo
```bash
python demo.py
```
- **Purpose**: Complete demonstration of all features
- **Features**:
  - SQL annotation parsing examples
  - FHIR Library generation
  - SQL dialect support demonstration
  - Batch processing example
  - Advanced features showcase
  - Output file analysis
- **Output**: Creates `demo_output/` with sample FHIR Libraries

## 📊 Test Coverage

The test suite covers:

| Feature | Test File | Coverage |
|---------|-----------|----------|
| Core Parsing | `test_parser.py` | ✅ All annotation formats, type conversion |
| FHIR Integration | `test_fhir_integration.py` | ✅ Library generation, base64 encoding |
| SQL Dialects | `test_sql_dialect.py` | ✅ Content type modification |
| Multiple Dependencies | `test_multiple_dependencies.py` | ✅ Related artifacts |
| Name Generation | `test_name_generation.py` | ✅ PascalCase conversion |
| Empty Properties | `test_empty_properties.py` | ✅ Property cleanup |

## 🎛️ Usage Examples

### Development Workflow
```bash
# Quick validation during development
python quick_test.py

# Comprehensive testing before commit
python run_all_tests.py

# Test specific feature
python test_commands.py test-dialect
```

### CI/CD Integration
```bash
# Health check
python test_commands.py check

# Full test suite with exit codes
python run_all_tests.py
echo $?  # 0 = success, 1 = failure
```

### Demo & Documentation
```bash
# Show all features to stakeholders
python demo.py

# Clean up outputs
python test_commands.py clean
```

## 📁 Output Directories

Tests and demos create organized output directories:
- `test_output/` - Individual test outputs
- `fhir_libraries/` - Main FHIR Library outputs  
- `demo_output/` - Demo script outputs
- `output/` - Legacy output directory (cleaned automatically)

## 🔧 Troubleshooting

### All Tests Failing
1. Check project health: `python test_commands.py check`
2. Verify required files exist in `examples/` directory
3. Ensure Python 3.6+ is being used

### Individual Test Failures  
1. Run test in isolation: `python test_[name].py`
2. Check error output for specific issues
3. Verify input files haven't been modified

### Permission Issues
```bash
# Make scripts executable (Unix/Mac)
chmod +x *.py

# Clean up locked files
python test_commands.py clean
```

---

*This reference covers all testing and demo capabilities of the SQL FHIR Library Generator project.*
