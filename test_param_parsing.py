#!/usr/bin/env python3
"""
Test script to debug parameter parsing
"""

from src.sql_fhir_library_generator import SQLAnnotationParser, FHIRLibraryBuilder

# Test SQL with @param annotations
test_sql = """
-- @title: Test Parameters
-- @param: user_id string
-- @param: age integer
-- @param: include_inactive boolean

SELECT * FROM users WHERE user_id = :user_id AND age > :age;
"""

# Parse annotations
parser = SQLAnnotationParser()
annotations = parser.parse_content(test_sql)

print("Parsed annotations:")
for key, value in annotations.items():
    print(f"  {key}: {value}")

# Build FHIR Library
builder = FHIRLibraryBuilder()
library = builder.build_library_from_content(
    sql_content=test_sql,
    annotations=annotations,
    library_id="test-params"
)

print("\nFHIR Library parameters:")
if "parameter" in library:
    for param in library["parameter"]:
        print(f"  - {param['name']} ({param['type']}) use: {param['use']}")
else:
    print("  No parameters found!")

# Check if any param keys exist
print(f"\nAll annotation keys: {list(annotations.keys())}")
param_keys = [k for k in annotations.keys() if k == "param" or k.startswith("param")]
print(f"Parameter keys found: {param_keys}")
