#!/usr/bin/env python3
"""
Test parameter functionality in FHIR Library Builder

Tests the @param annotation feature for specifying query parameters
with optional data types.
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from sql_fhir_library_generator import FHIRLibraryBuilder


def test_param_with_types():
    """Test @param annotations with various data types."""

    sql_with_params = """
    -- @title: Parameter Types Test
    -- @param: user_id string
    -- @param: age integer
    -- @param: salary decimal
    -- @param: is_active boolean
    -- @param: birth_date date
    -- @param: created_at dateTime
    
    SELECT * FROM users WHERE user_id = :user_id;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_params, library_id="test-param-types"
    )

    assert "parameter" in library
    assert len(library["parameter"]) == 6

    # Check parameter types
    params = {p["name"]: p["type"] for p in library["parameter"]}
    expected_types = {
        "user_id": "string",
        "age": "integer",
        "salary": "decimal",
        "is_active": "boolean",
        "birth_date": "date",
        "created_at": "dateTime",
    }

    assert params == expected_types

    # Check all parameters have use="in"
    for param in library["parameter"]:
        assert param["use"] == "in"

    print("✅ Parameter types test passed")


def test_param_defaults_to_string():
    """Test @param annotations without types default to string."""

    sql_with_default_params = """
    -- @title: Default Parameter Types
    -- @param: param1
    -- @param: param2
    
    SELECT * FROM table WHERE col1 = :param1 AND col2 = :param2;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_default_params, library_id="test-default-params"
    )

    assert "parameter" in library
    assert len(library["parameter"]) == 2

    for param in library["parameter"]:
        assert param["type"] == "string"
        assert param["use"] == "in"

    print("✅ Default string type test passed")


def test_legacy_parameters():
    """Test backward compatibility with @parameters annotation."""

    sql_with_legacy = """
    -- @title: Legacy Parameters
    -- @parameters: param1, param2, param3
    
    SELECT * FROM table;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_legacy, library_id="test-legacy"
    )

    assert "parameter" in library
    assert len(library["parameter"]) == 3

    param_names = {p["name"] for p in library["parameter"]}
    assert param_names == {"param1", "param2", "param3"}

    # All legacy parameters should be strings
    for param in library["parameter"]:
        assert param["type"] == "string"
        assert param["use"] == "in"

    print("✅ Legacy parameters test passed")


def test_mixed_parameters():
    """Test mixing @param and @parameters annotations."""

    sql_with_mixed = """
    -- @title: Mixed Parameters
    -- @parameters: legacy_param
    -- @param: new_param integer
    
    SELECT * FROM table;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_mixed, library_id="test-mixed"
    )

    assert "parameter" in library
    assert len(library["parameter"]) == 2

    params = {p["name"]: p["type"] for p in library["parameter"]}
    expected = {"legacy_param": "string", "new_param": "integer"}
    assert params == expected

    print("✅ Mixed parameters test passed")


def test_type_mapping():
    """Test data type mapping to FHIR types."""

    sql_with_type_variants = """
    -- @title: Type Mapping Test
    -- @param: str_param str
    -- @param: int_param int
    -- @param: float_param float
    -- @param: bool_param bool
    -- @param: url_param url
    -- @param: id_param id
    
    SELECT * FROM table;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_type_variants, library_id="test-type-mapping"
    )

    assert "parameter" in library

    params = {p["name"]: p["type"] for p in library["parameter"]}
    expected = {
        "str_param": "string",
        "int_param": "integer",
        "float_param": "decimal",
        "bool_param": "boolean",
        "url_param": "url",
        "id_param": "id",
    }
    assert params == expected

    print("✅ Type mapping test passed")


def test_no_parameters():
    """Test SQL without parameters doesn't create parameter field."""

    sql_no_params = """
    -- @title: No Parameters
    
    SELECT * FROM table;
    """

    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_no_params, library_id="test-no-params"
    )

    assert "parameter" not in library

    print("✅ No parameters test passed")


if __name__ == "__main__":
    print("🧪 Testing @param functionality...")
    print("=" * 50)

    test_param_with_types()
    test_param_defaults_to_string()
    test_legacy_parameters()
    test_mixed_parameters()
    test_type_mapping()
    test_no_parameters()

    print("=" * 50)
    print("🎉 All parameter tests passed!")
