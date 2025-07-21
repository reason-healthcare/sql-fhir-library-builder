#!/usr/bin/env python3
"""
SQL Dialect Version Feature Test

This script demonstrates the sqlDialectVersion annotation feature that allows
specifying version parameters in MIME types for SQL dialects.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sql_fhir_library_generator import FHIRLibraryBuilder


def test_dialect_version():
    """Test the sqlDialectVersion annotation functionality."""

    builder = FHIRLibraryBuilder(output_dir="test_output")

    # Test cases with different SQL dialects and versions
    test_files = [
        (
            "examples/hive_with_version.sql",
            "application/sql; dialect=hive; version=3.1.2",
            "Hive 3.1.2",
        ),
        (
            "examples/postgres_with_version.sql",
            "application/sql; dialect=postgres; version=15.4",
            "PostgreSQL 15.4",
        ),
        (
            "examples/hive_example.sql",
            "application/sql; dialect=hive",
            "Hive (no version)",
        ),
        (
            "examples/sql_on_fhir_example.sql",
            "application/sql",
            "Standard SQL (no dialect or version)",
        ),
    ]

    print("=" * 80)
    print("SQL DIALECT VERSION ANNOTATION TEST")
    print("=" * 80)

    for sql_file, expected_content_type, description in test_files:
        if not os.path.exists(sql_file):
            print(f"❌ SKIP - File not found: {sql_file}")
            continue

        print(f"\nTesting {description}:")
        print(f"  File: {sql_file}")
        print(f"  Expected Content Type: {expected_content_type}")

        try:
            library = builder.build_library_from_file(sql_file)
            actual_content_type = library["content"][0]["contentType"]
            print(f"  Actual Content Type:   {actual_content_type}")

            if actual_content_type == expected_content_type:
                print(f"  ✅ PASS - Content type matches expectation")
            else:
                print(f"  ❌ FAIL - Content type mismatch")

            # Show additional details
            output_file = library.get("id", "unknown") + ".json"
            print(f"  Exported to: test_output/{output_file}")
            print(f"  Title: {library.get('title', 'N/A')}")
            print(f"  Status: {library.get('status', 'N/A')}")

        except Exception as e:
            print(f"  ❌ ERROR - {str(e)}")

    print("\n" + "=" * 80)
    print("SUPPORTED DIALECT VERSION COMBINATIONS")
    print("=" * 80)
    print()
    print("The sqlDialectVersion annotation works with any SQL dialect.")
    print("Examples of content types that can be generated:")
    print(
        "  @sqlDialect: hive, @sqlDialectVersion: 3.1.2     → application/sql; dialect=hive; version=3.1.2"
    )
    print(
        "  @sqlDialect: spark, @sqlDialectVersion: 3.4.0    → application/sql; dialect=spark; version=3.4.0"
    )
    print(
        "  @sqlDialect: postgres, @sqlDialectVersion: 15.4  → application/sql; dialect=postgres; version=15.4"
    )
    print(
        "  @sqlDialect: mysql, @sqlDialectVersion: 8.0.33   → application/sql; dialect=mysql; version=8.0.33"
    )
    print(
        "  @sqlDialect: oracle, @sqlDialectVersion: 19c     → application/sql; dialect=oracle; version=19c"
    )
    print(
        "  @sqlDialect: snowflake, @sqlDialectVersion: 7.x  → application/sql; dialect=snowflake; version=7.x"
    )
    print(
        "  @sqlDialect: hive (no version)                   → application/sql; dialect=hive"
    )
    print("  (no annotations)                                 → application/sql")
    print()


if __name__ == "__main__":
    test_dialect_version()
