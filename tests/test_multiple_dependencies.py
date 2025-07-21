#!/usr/bin/env python3
"""
Test script for multiple @relatedDependency annotations

This script demonstrates how the SQL parser handles multiple annotations
with the same key and how they are converted to FHIR relatedArtifact entries.
"""

import json
from pathlib import Path

from sql_fhir_library_generator import FHIRLibraryBuilder, SQLAnnotationParser


def main():
    """Test multiple @relatedDependency annotations."""

    parser = SQLAnnotationParser()
    builder = FHIRLibraryBuilder(output_dir="test_output")

    # Test SQL with multiple @relatedDependency annotations
    test_sql = """
    -- @title: Patient Care Coordination Queries
    -- @version: 1.0.0
    -- @status: active
    -- @description: Queries for coordinating patient care across multiple systems
    -- @author: Clinical Integration Team
    -- @relatedDependency: Library/patient-demographics
    -- @relatedDependency: Library/clinical-observations
    -- @relatedDependency: Library/medication-orders
    
    /*
    @purpose: Support care coordination workflows by providing
             standardized queries across clinical systems
    @relatedDependency: Questionnaire/patient-preferences
    @relatedDependency: ValueSet/care-team-roles
    @relatedDependency: CodeSystem/clinical-priorities
    @database: clinical_warehouse
    @tables: patients, observations, medications, care_teams
    */
    
    -- Main care coordination query
    SELECT 
        p.patient_id,
        p.name,
        o.observation_date,
        o.value,
        m.medication_name,
        ct.role
    FROM patients p
    JOIN observations o ON p.patient_id = o.patient_id
    LEFT JOIN medications m ON p.patient_id = m.patient_id
    LEFT JOIN care_teams ct ON p.patient_id = ct.patient_id
    WHERE p.active = 1;
    
    -- @relatedDependency: Library/audit-logging
    -- Log access for compliance
    INSERT INTO access_log (user_id, resource_type, timestamp)
    VALUES (:current_user_id, 'patient_care_data', NOW());
    """

    print("Testing Multiple @relatedDependency Annotations")
    print("=" * 60)

    # Parse annotations
    annotations = parser.parse_content(test_sql)

    print("\nParsed Annotations:")
    print("-" * 20)
    for key, value in annotations.items():
        if isinstance(value, list):
            print(f"@{key}: {value} (list with {len(value)} items)")
        else:
            print(f"@{key}: {value}")

    # Build FHIR Library
    library = builder.build_library_from_content(
        sql_content=test_sql,
        annotations=annotations,
        library_id="patient-care-coordination",
        filename="care_coordination.sql",
    )

    print(f"\nFHIR Library Generated:")
    print("-" * 25)
    print(f"ID: {library['id']}")
    print(f"Title: {library.get('title', 'N/A')}")
    print(f"Status: {library['status']}")

    # Show related artifacts
    related_artifacts = library.get("relatedArtifact", [])
    print(f"\nRelated Artifacts ({len(related_artifacts)} total):")
    print("-" * 30)

    for i, artifact in enumerate(related_artifacts, 1):
        artifact_type = artifact.get("type", "unknown")
        resource = artifact.get("resource", artifact.get("display", "N/A"))
        print(f"  {i}. Type: {artifact_type}")
        print(f"     Resource: {resource}")

    # Export the library
    output_file = builder.export_library(library, "multiple_dependencies_library.json")
    print(f"\nLibrary exported to: {output_file}")

    # Show a portion of the JSON for verification
    print(f"\nSample of relatedArtifact section:")
    print("-" * 35)
    if related_artifacts:
        print(json.dumps(related_artifacts[:3], indent=2))
        if len(related_artifacts) > 3:
            print(f"... and {len(related_artifacts) - 3} more")

    # Test edge cases
    print(f"\n\nTesting Edge Cases:")
    print("-" * 20)

    edge_case_sql = """
    -- @title: Edge Case Test
    -- @relatedDependency: single-dependency
    -- @relatedDependency: Library/dep-1, Library/dep-2, Library/dep-3
    -- @other: value1
    -- @other: value2
    
    SELECT 1;
    """

    edge_annotations = parser.parse_content(edge_case_sql)
    edge_library = builder.build_library_from_content(
        sql_content=edge_case_sql,
        annotations=edge_annotations,
        library_id="edge-case-test",
        filename="edge_case.sql",
    )

    print("Edge case annotations:")
    for key, value in edge_annotations.items():
        print(f"  @{key}: {value} ({type(value).__name__})")

    edge_artifacts = edge_library.get("relatedArtifact", [])
    print(f"\nEdge case related artifacts ({len(edge_artifacts)} total):")
    for artifact in edge_artifacts:
        print(f"  - {artifact.get('resource', artifact.get('display', 'N/A'))}")


if __name__ == "__main__":
    main()
