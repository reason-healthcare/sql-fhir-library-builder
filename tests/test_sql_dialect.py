#!/usr/bin/env python3
"""
Test script for SQL Dialect functionality.

This script demonstrates the sqlDialect annotation feature that allows
specifying the SQL dialect to modify the FHIR Library content type.
"""

import json

from sql_fhir_library_generator import FHIRLibraryBuilder


def test_sql_dialect():
    """Test the sqlDialect annotation functionality."""

    builder = FHIRLibraryBuilder(output_dir="test_output")

    # Test cases with different SQL dialects
    test_files = [
        ("examples/hive_example.sql", "application/sql; dialect=hive", "Hive"),
        ("examples/spark_example.sql", "application/sql; dialect=spark", "Spark"),
        (
            "examples/sql_on_fhir_example.sql",
            "application/sql",
            "Standard SQL (no dialect)",
        ),
    ]

    print("=" * 80)
    print("SQL DIALECT ANNOTATION TEST")
    print("=" * 80)
    print()

    for sql_file, expected_content_type, description in test_files:
        print(f"Testing {description}:")
        print(f"  File: {sql_file}")

        try:
            # Build library from SQL file
            library = builder.build_library_from_file(sql_file)

            # Get actual content type
            actual_content_type = library["content"][0]["contentType"]

            print(f"  Expected Content Type: {expected_content_type}")
            print(f"  Actual Content Type:   {actual_content_type}")

            # Verify content type matches expectation
            if actual_content_type == expected_content_type:
                print("  ✅ PASS - Content type matches expectation")
            else:
                print("  ❌ FAIL - Content type does not match expectation")

            # Export library
            output_path = builder.export_library(library)
            print(f"  Exported to: {output_path}")

            # Show other details
            if "title" in library:
                print(f"  Title: {library['title']}")
            if "status" in library:
                print(f"  Status: {library['status']}")

        except Exception as e:
            print(f"  ❌ ERROR: {e}")

        print()

    print("=" * 80)
    print("SUPPORTED SQL DIALECTS DEMO")
    print("=" * 80)
    print()
    print("The sqlDialect annotation supports any SQL dialect name.")
    print("Examples of content types that can be generated:")
    print("  @sqlDialect: hive     → application/sql; dialect=hive")
    print("  @sqlDialect: spark    → application/sql; dialect=spark")
    print("  @sqlDialect: mysql    → application/sql; dialect=mysql")
    print("  @sqlDialect: postgres → application/sql; dialect=postgres")
    print("  @sqlDialect: oracle   → application/sql; dialect=oracle")
    print("  @sqlDialect: snowflake → application/sql; dialect=snowflake")
    print("  (no annotation)       → application/sql")
    print()


if __name__ == "__main__":
    test_sql_dialect()
