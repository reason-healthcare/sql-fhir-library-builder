#!/usr/bin/env python3
"""
Test script for empty property removal in FHIR Library generation

This script demonstrates how the FHIR Library Builder removes empty properties
from the generated FHIR Library resources.
"""

import json

from sql_fhir_library_generator import FHIRLibraryBuilder


def test_empty_property_removal():
    """Test removal of empty properties from FHIR Library resources."""

    builder = FHIRLibraryBuilder(output_dir="test_output")

    # Test SQL with various empty and non-empty annotations
    test_sql = """
    -- @title: Comprehensive Empty Property Test
    -- @description: Testing removal of empty properties
    -- @version: 1.0.0
    -- @status: active
    -- @author: Test Author
    -- @publisher:
    -- @copyright:
    -- @purpose: Demonstrate empty property handling
    -- @usage:
    -- @url:
    -- @contact:
    -- @tags:
    -- @relatedDependency: Library/test-dependency
    -- @relatedDependency:

    /*
    @experimental: true
    @jurisdiction:
    @approvalDate:
    @lastReviewDate: 2024-07-21
    @effectivePeriod:
    @identifier:
    @subject:
    @database: test_db
    @schema:
    @tables: patients, observations
    @parameters:
    */

    SELECT p.id, p.name, o.value
    FROM patients p
    JOIN observations o ON p.id = o.patient_id;
    """

    print("Testing Empty Property Removal")
    print("=" * 40)

    # Generate the library
    library = builder.build_library_from_content(
        sql_content=test_sql,
        library_id="empty-property-test",
        filename="test_empty_properties.sql",
    )

    # Show the cleaned result
    print("\n1. Generated FHIR Library (cleaned):")
    print("-" * 35)
    print(json.dumps(library, indent=2))

    # Manually verify what was removed vs kept
    print("\1")
    print("-" * 20)

    kept_properties = []
    for key in library.keys():
        if key not in ["resourceType", "id", "type", "content"]:
            kept_properties.append(key)

    print(f"Properties kept: {', '.join(kept_properties)}")

    # Check author object
    author = library.get("author", [])
    if author:
        author_props = (
            list(author[0].keys()) if isinstance(author, list) else list(author.keys())
        )
        print(f"Author properties: {', '.join(author_props)}")

    # Check related artifacts
    related_artifacts = library.get("relatedArtifact", [])
    print(f"Related artifacts count: {len(related_artifacts)}")

    # Check extensions (should contain non-empty custom annotations)
    extensions = library.get("extension", [])
    print(f"Extensions count: {len(extensions)}")

    if extensions:
        print("Extension URLs:")
        for ext in extensions:
            url = ext.get("url", "").split("/")[-1]
            print(f"  - {url}")

    # Export for inspection
    output_file = builder.export_library(library, "empty_property_test_library.json")
    print(f"\n3. Library exported to: {output_file}")

    # Compare with a version that has all properties (for demonstration)
    print("\1")
    print("-" * 45)

    potentially_empty = [
        "publisher",
        "copyright",
        "usage",
        "url",
        "contact",
        "jurisdiction",
        "approvalDate",
        "effectivePeriod",
        "identifier",
        "subject",
    ]

    for prop in potentially_empty:
        status = "✅ Removed" if prop not in library else f"❌ Kept: {library[prop]}"
        print(f"  {prop}: {status}")

    print("\1")
    print(f"📄 Check {output_file} for the complete cleaned FHIR Library resource.")


if __name__ == "__main__":
    test_empty_property_removal()
