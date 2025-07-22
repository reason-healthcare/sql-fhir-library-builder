#!/usr/bin/env python3
"""
Test script for automatic name generation from titles

This script demonstrates how the FHIR Library Builder automatically generates
camelCase names from titles when @name annotation is not provided.
"""

from sql_fhir_library_generator import FHIRLibraryBuilder


def test_name_generation():
    """Test PascalCase name generation from various title formats."""

    builder = FHIRLibraryBuilder(output_dir="test_output")

    test_cases = [
        {"title": "Patient Demographics Query", "expected": "PatientDemographicsQuery"},
        {
            "title": "Advanced Clinical Decision Support",
            "expected": "AdvancedClinicalDecisionSupport",
        },
        {
            "title": "SQL-on-FHIR Integration Library",
            "expected": "SqlOnFhirIntegrationLibrary",
        },
        {
            "title": "User Management & Authentication",
            "expected": "UserManagementAuthentication",
        },
        {
            "title": "COVID-19 Vaccination Status Report",
            "expected": "Covid19VaccinationStatusReport",
        },
        {
            "title": "Multi_Word_Title_With_Underscores",
            "expected": "MultiWordTitleWithUnderscores",
        },
        {"title": "Simple Title", "expected": "SimpleTitle"},
        {"title": "OneWord", "expected": "Oneword"},
        {"title": "Title123WithNumbers456", "expected": "Title123withnumbers456"},
    ]

    print("Testing Automatic Name Generation from Titles (PascalCase)")
    print("=" * 60)

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        title = test_case["title"]
        expected = test_case["expected"]

        # Create a simple SQL content with just the title
        sql_content = f"""
        -- @title: {title}
        -- @status: active

        SELECT 1 as test;
        """

        # Build the library
        library = builder.build_library_from_content(
            sql_content=sql_content, library_id=f"test-{i}", filename="test.sql"
        )

        generated_name = library.get("name", "")

        # Check if the generated name matches expected
        passed = generated_name == expected
        status = "✅ PASS" if passed else "❌ FAIL"

        print(f"{i:2d}. {status} | '{title}'")
        print(f"     Expected: {expected}")
        print(f"     Got:      {generated_name}")

        if not passed:
            all_passed = False

        print()

    # Test case where @name is explicitly provided (should not be overridden)
    print("Testing Explicit @name Annotation (should not be overridden):")
    print("-" * 55)

    explicit_name_sql = """
    -- @title: Some Complex Title Here
    -- @name: explicitCustomName
    -- @status: active

    SELECT 1;
    """

    explicit_library = builder.build_library_from_content(
        sql_content=explicit_name_sql,
        library_id="explicit-test",
        filename="explicit.sql",
    )

    explicit_name = explicit_library.get("name", "")
    expected_explicit = "explicitCustomName"

    explicit_passed = explicit_name == expected_explicit
    status = "✅ PASS" if explicit_passed else "❌ FAIL"

    print(f"{status} | Explicit @name should be preserved")
    print("\1")
    print(f"Expected: {expected_explicit}")
    print(f"Got:      {explicit_name}")

    # Overall result
    print(f"\n{'=' * 50}")
    if all_passed and explicit_passed:
        print("🎉 All tests PASSED!")
    else:
        print("❌ Some tests FAILED!")

    return all_passed and explicit_passed


if __name__ == "__main__":
    test_name_generation()
