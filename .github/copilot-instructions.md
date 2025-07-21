<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# SQL FHIR Library Generator Project

This project is a Python-based SQL parser that extracts @annotations from SQL comments and generates FHIR Library resources. It supports multiple SQL dialects with version specifications and provides a comprehensive test suite to ensure functionality. 

## Context
- The main parser is in `sql_fhir_library_generator/parser.py` 
- Example SQL files with various annotation patterns are in the `examples/` directory
- The parser supports both single-line (`--`) and multi-line (`/* */`) SQL comments
- Annotations can be in formats: `@key value`, `@key: value`, `@key = value`
- Values are automatically converted to appropriate Python types (boolean, int, float, list, string)
- SQL dialect support: `@sqlDialect` and `@dialectVersion` create MIME types like `application/sql; dialect=hive; version=3.1.2`

## Code Style Guidelines
- Use clear, descriptive variable and function names
- Include comprehensive docstrings for all classes and methods
- Handle errors gracefully with try-catch blocks
- Use type hints for function parameters and return values
- Follow PEP 8 style guidelines

## Testing Approach
- Test with various SQL comment formats and annotation syntaxes
- Include edge cases like empty files, malformed annotations, and special characters
- Verify type conversion works correctly for all supported types
- Test both single-file and batch processing functionality
