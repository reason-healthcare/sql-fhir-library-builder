#!/usr/bin/env python3
"""
Test script for SQL Annotation Parser

This script demonstrates how to use the SQL annotation parser to extract
annotations from SQL files and display the results.
"""

from pathlib import Path

from sql_fhir_library_generator import SQLAnnotationParser


def print_annotations(annotations: dict, title: str):
    """Print annotations in a formatted way."""
    print(f"\n{title}")
    print("=" * len(title))

    if not annotations:
        print("No annotations found.")
        return

    for key, value in annotations.items():
        value_type = type(value).__name__
        if isinstance(value, list):
            formatted_value = f"[{', '.join(map(str, value))}]"
        else:
            formatted_value = str(value)

        print(f"  @{key}: {formatted_value} ({value_type})")


def main():
    """Main test function."""
    parser = SQLAnnotationParser()

    # Test 1: Parse example SQL content directly
    print("SQL Annotation Parser - Test Results")
    print("====================================")

    example_sql = """
    -- @author: Test User
    -- @version: 1.0
    -- @tags: test, example, demo
    -- @active: true
    -- @priority: 5
    -- @confidence: 0.95

    SELECT * FROM test_table;

    /*
    @description: This is a multi-line comment
                  with an annotation that spans multiple lines
    @complex_config: {setting1: true, setting2: false}
    @list_items: apple, banana, cherry
    @date_created: 2024-07-21
    */

    CREATE TABLE test (id INT);
    """

    annotations = parser.parse_content(example_sql)
    print_annotations(annotations, "Test 1: Direct Content Parsing")

    # Test 2: Parse files from examples directory
    examples_dir = Path("examples")
    if examples_dir.exists():
        print("\1")
        print("=" * 30)

        sql_files = list(examples_dir.glob("*.sql"))

        if sql_files:
            for sql_file in sql_files:
                try:
                    file_annotations = parser.parse_file(sql_file)
                    print_annotations(file_annotations, f"File: {sql_file.name}")
                except Exception as e:
                    print(f"\nError parsing {sql_file.name}: {e}")
        else:
            print("No SQL files found in examples directory.")
    else:
        print("\1")

    # Test 3: Parse multiple files at once
    if examples_dir.exists():
        sql_files = list(examples_dir.glob("*.sql"))
        if sql_files:
            print("\1")
            print("=" * 30)

            batch_results = parser.parse_multiple_files(sql_files)

            for file_path, file_annotations in batch_results.items():
                filename = Path(file_path).name
                if "error" in file_annotations:
                    print(f"\n{filename}: ERROR - {file_annotations['error']}")
                else:
                    print(f"\n{filename}: {len(file_annotations)} annotations found")
                    for key, value in list(file_annotations.items())[
                        :3
                    ]:  # Show first 3
                        print(f"  @{key}: {value}")
                    if len(file_annotations) > 3:
                        print(f"  ... and {len(file_annotations) - 3} more")

    print("")
    print(
        "For more detailed examples, check the SQL files in the 'examples' directory."
    )


if __name__ == "__main__":
    main()
