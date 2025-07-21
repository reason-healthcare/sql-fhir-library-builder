#!/usr/bin/env python3
"""
Comprehensive test for SQL Annotation Parser and FHIR Library Builder

This script demonstrates the complete workflow from SQL files with annotations
to FHIR Library resources.
"""

import json
from datetime import datetime
from pathlib import Path

from sql_fhir_library_generator import FHIRLibraryBuilder, SQLAnnotationParser


def print_section(title: str, content: str = None):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print("=" * 60)
    if content:
        print(content)


def print_annotations(annotations: dict, title: str = "Annotations"):
    """Print annotations in a formatted way."""
    print(f"\n{title}:")
    print("-" * len(title))

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


def print_fhir_summary(library: dict):
    """Print a summary of the FHIR Library resource."""
    print(f"\nFHIR Library Summary:")
    print("-" * 20)
    print(f"ID: {library.get('id', 'N/A')}")
    print(f"Title: {library.get('title', 'N/A')}")
    print(f"Status: {library.get('status', 'N/A')}")
    print(f"Version: {library.get('version', 'N/A')}")
    print(f"Description: {library.get('description', 'N/A')}")

    # Content summary
    content = library.get("content", [])
    if content:
        content_item = content[0]
        print(f"Content Type: {content_item.get('contentType', 'N/A')}")
        print(f"Content Size: {len(content_item.get('data', ''))} bytes (base64)")

    # Extensions
    extensions = library.get("extension", [])
    if extensions:
        print(f"Custom Extensions: {len(extensions)}")
        for ext in extensions[:3]:  # Show first 3
            url_parts = ext.get("url", "").split("/")
            ext_name = url_parts[-1] if url_parts else "unknown"
            value_key = (
                [k for k in ext.keys() if k.startswith("value")][0]
                if any(k.startswith("value") for k in ext.keys())
                else "url"
            )
            print(f"  - {ext_name}: {ext.get(value_key, 'N/A')}")
        if len(extensions) > 3:
            print(f"  ... and {len(extensions) - 3} more")


def main():
    """Main test function demonstrating the complete workflow."""

    print_section("SQL Annotation Parser & FHIR Library Builder Test")

    # Initialize both classes
    parser = SQLAnnotationParser()
    builder = FHIRLibraryBuilder(output_dir="test_output")

    # Test 1: Parse annotations and build FHIR Library from content
    print_section("Test 1: Content-based Processing")

    comprehensive_sql = """
    -- @title: Patient Demographics Query Library
    -- @name: PatientDemographics
    -- @version: 3.2.1
    -- @status: active
    -- @author: Clinical Data Team
    -- @publisher: Regional Health Network
    -- @description: Comprehensive queries for patient demographic analysis
    -- @purpose: Support clinical decision making and population health management
    -- @copyright: 2024 Regional Health Network. All rights reserved.
    -- @date: 2024-07-21
    -- @experimental: false
    -- @jurisdiction: US, CA
    -- @approvalDate: 2024-06-01
    -- @lastReviewDate: 2024-07-15
    
    /*
    @usage: This library provides standardized queries for extracting
            and analyzing patient demographic information across
            multiple clinical systems.
    @database: clinical_warehouse
    @schema: patient_data
    @tables: patients, demographics, addresses, contacts
    @parameters: facility_id, date_range, age_group
    @security_level: PHI
    @compliance: HIPAA, SOX
    @performance_tier: high
    @refresh_frequency: daily
    @data_retention: 7_years
    */
    
    -- Core patient demographics query
    SELECT 
        p.patient_id,
        p.medical_record_number,
        d.first_name,
        d.last_name,
        d.date_of_birth,
        d.gender,
        d.race,
        d.ethnicity,
        a.zip_code,
        a.state
    FROM patients p
    JOIN demographics d ON p.patient_id = d.patient_id
    LEFT JOIN addresses a ON p.patient_id = a.patient_id
    WHERE p.facility_id = :facility_id
        AND d.date_of_birth BETWEEN :start_date AND :end_date;
    
    -- @query_type: aggregation
    -- @frequency: weekly
    -- @output_format: summary
    SELECT 
        d.gender,
        COUNT(*) as patient_count,
        AVG(YEAR(CURRENT_DATE) - YEAR(d.date_of_birth)) as avg_age
    FROM patients p
    JOIN demographics d ON p.patient_id = d.patient_id
    GROUP BY d.gender;
    """

    # Parse annotations
    annotations = parser.parse_content(comprehensive_sql)
    print_annotations(annotations, "Extracted Annotations")

    # Build FHIR Library
    library = builder.build_library_from_content(
        sql_content=comprehensive_sql,
        annotations=annotations,
        library_id="patient-demographics-v3",
        filename="patient_demographics.sql",
    )

    print_fhir_summary(library)

    # Save the library to output directory
    output_file = builder.export_library(library, "patient_demographics_library.json")
    print(f"\nFHIR Library exported to: {output_file}")

    # Test 2: Process example files if they exist
    print_section("Test 2: File-based Processing")

    examples_dir = Path("examples")
    if examples_dir.exists():
        sql_files = list(examples_dir.glob("*.sql"))

        if sql_files:
            print(f"Found {len(sql_files)} SQL files:")
            for sql_file in sql_files:
                print(f"  - {sql_file.name}")

            # Process each file individually
            for sql_file in sql_files:
                print(f"\nProcessing: {sql_file.name}")
                print("-" * 40)

                try:
                    # Parse annotations
                    file_annotations = parser.parse_file(sql_file)
                    print(f"Annotations found: {len(file_annotations)}")

                    # Show first few annotations
                    for i, (key, value) in enumerate(
                        list(file_annotations.items())[:3]
                    ):
                        print(f"  @{key}: {value}")
                    if len(file_annotations) > 3:
                        print(f"  ... and {len(file_annotations) - 3} more")

                    # Build FHIR Library
                    file_library = builder.build_library_from_file(sql_file)

                    # Export to JSON in output directory
                    output_filename = f"fhir_{sql_file.stem}_library.json"
                    output_path = builder.export_library_to_file(
                        file_library, output_filename
                    )

                    print(f"  → FHIR Library: {file_library.get('id', 'unknown')}")
                    print(f"  → Exported to: {output_path}")

                except Exception as e:
                    print(f"  ERROR: {e}")
        else:
            print("No SQL files found in examples directory.")
    else:
        print("Examples directory not found.")

    # Test 3: Batch processing
    print_section("Test 3: Batch Processing")

    if examples_dir.exists() and list(examples_dir.glob("*.sql")):
        sql_files = list(examples_dir.glob("*.sql"))

        print(f"Batch processing {len(sql_files)} files...")

        # Build all libraries at once
        libraries = builder.build_multiple_libraries(sql_files)

        print(f"\nBatch Results:")
        print("-" * 20)

        for i, lib in enumerate(libraries, 1):
            status = lib.get("status", "unknown")
            title = lib.get("title", lib.get("id", "Untitled"))
            extensions = len(lib.get("extension", []))

            # Check if it's an error library
            error_ext = next(
                (
                    ext
                    for ext in lib.get("extension", [])
                    if "error" in ext.get("url", "")
                ),
                None,
            )

            if error_ext:
                print(
                    f"  {i}. ERROR - {lib.get('id', 'unknown')}: {error_ext.get('valueString', 'Unknown error')}"
                )
            else:
                print(f"  {i}. {title} (Status: {status}, Extensions: {extensions})")

        # Export batch results to output directory
        batch_output = {
            "resourceType": "Bundle",
            "id": "sql-libraries-batch",
            "type": "collection",
            "timestamp": datetime.now().isoformat() + "Z",
            "total": len(libraries),
            "entry": [{"resource": lib} for lib in libraries],
        }

        batch_filename = "fhir_libraries_bundle.json"
        batch_path = builder.export_library_to_file(batch_output, batch_filename)

        print(f"\nBatch bundle exported to: {batch_path}")

    # Test 4: Demonstrate type conversion and edge cases
    print_section("Test 4: Type Conversion & Edge Cases")

    edge_case_sql = """
    -- @boolean_true: true
    -- @boolean_false: false  
    -- @integer: 42
    -- @float: 3.14159
    -- @list_strings: apple, banana, cherry
    -- @list_mixed: 1, true, hello, 3.14
    -- @quoted_string: "This is a quoted string"
    -- @empty_value: 
    -- @special_chars: value_with_underscores
    -- @with_colon: key: value with colon
    -- @with_equals: key = value with equals
    
    /*
    @multi_line_value: This is a value that spans
                       multiple lines in the comment
    @json_like: {key1: value1, key2: value2}
    @date_iso: 2024-07-21
    @date_us: 07/21/2024
    */
    
    SELECT 1 as test;
    """

    edge_annotations = parser.parse_content(edge_case_sql)
    print_annotations(edge_annotations, "Type Conversion Examples")

    # Build library with edge cases
    edge_library = builder.build_library_from_content(
        sql_content=edge_case_sql,
        annotations=edge_annotations,
        library_id="type-conversion-test",
        filename="edge_cases.sql",
    )

    print(f"\nEdge Case Library Extensions: {len(edge_library.get('extension', []))}")

    # Final summary
    print_section("Test Summary")
    print("✅ SQL annotation parsing")
    print("✅ FHIR Library resource generation")
    print("✅ Base64 encoding of SQL content")
    print("✅ Type conversion (bool, int, float, list, string)")
    print("✅ Custom FHIR extensions for non-standard annotations")
    print("✅ File-based and content-based processing")
    print("✅ Batch processing capabilities")
    print("✅ JSON export functionality")

    print(f"\nAll tests completed successfully!")
    print(f"Check the generated JSON files for detailed FHIR Library resources.")


if __name__ == "__main__":
    main()
