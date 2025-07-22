#!/usr/bin/env python3
"""
Test script for @param annotation functionality
"""

import json
from src.sql_fhir_library_generator import FHIRLibraryBuilder

def test_param_annotations():
    """Test @param annotations with various data types"""
    
    sql_with_params = """
    -- @title: Parameter Test Query
    -- @description: Testing parameter parsing with different data types
    -- @param: user_id string
    -- @param: age integer
    -- @param: salary decimal
    -- @param: is_active boolean
    -- @param: birth_date date
    -- @param: created_at dateTime
    
    SELECT user_id, age, salary, is_active 
    FROM users 
    WHERE user_id = :user_id 
    AND age > :age 
    AND salary > :salary
    AND is_active = :is_active
    AND birth_date > :birth_date
    AND created_at > :created_at;
    """
    
    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_params,
        library_id="test-param-types",
        filename="test_params.sql"
    )
    
    print("✅ Parameter Type Test")
    print("=" * 50)
    
    if "parameter" in library:
        print(f"Found {len(library['parameter'])} parameters:")
        for param in library["parameter"]:
            print(f"  • {param['name']}: {param['type']} (use: {param['use']})")
    else:
        print("❌ No parameters found!")
        return False
    
    # Verify expected parameters
    expected_params = {
        "user_id": "string",
        "age": "integer", 
        "salary": "decimal",
        "is_active": "boolean",
        "birth_date": "date",
        "created_at": "dateTime"
    }
    
    actual_params = {p["name"]: p["type"] for p in library["parameter"]}
    
    if actual_params == expected_params:
        print("✅ All parameter types correctly parsed!")
        return True
    else:
        print("❌ Parameter mismatch!")
        print(f"Expected: {expected_params}")
        print(f"Actual: {actual_params}")
        return False

def test_legacy_parameters():
    """Test backward compatibility with legacy @parameters annotation"""
    
    sql_with_legacy_params = """
    -- @title: Legacy Parameters Test
    -- @parameters: user_id, start_date, end_date
    
    SELECT * FROM logs WHERE user_id = :user_id 
    AND created_at BETWEEN :start_date AND :end_date;
    """
    
    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_legacy_params,
        library_id="test-legacy-params",
        filename="legacy_params.sql"
    )
    
    print("\n✅ Legacy Parameters Test")
    print("=" * 50)
    
    if "parameter" in library:
        print(f"Found {len(library['parameter'])} legacy parameters:")
        for param in library["parameter"]:
            print(f"  • {param['name']}: {param['type']} (use: {param['use']})")
        
        # Verify all parameters are strings with 'in' use
        all_correct = all(
            p["type"] == "string" and p["use"] == "in" 
            for p in library["parameter"]
        )
        
        if all_correct and len(library["parameter"]) == 3:
            print("✅ Legacy parameters correctly parsed!")
            return True
        else:
            print("❌ Legacy parameter parsing failed!")
            return False
    else:
        print("❌ No legacy parameters found!")
        return False

def test_mixed_parameters():
    """Test mixing @param and @parameters in same query"""
    
    sql_with_mixed = """
    -- @title: Mixed Parameters Test
    -- @parameters: legacy_param1, legacy_param2
    -- @param: new_param integer
    -- @param: another_param boolean
    
    SELECT * FROM table WHERE col1 = :legacy_param1;
    """
    
    builder = FHIRLibraryBuilder()
    library = builder.build_library_from_content(
        sql_content=sql_with_mixed,
        library_id="test-mixed-params",
        filename="mixed_params.sql"
    )
    
    print("\n✅ Mixed Parameters Test")
    print("=" * 50)
    
    if "parameter" in library:
        print(f"Found {len(library['parameter'])} mixed parameters:")
        for param in library["parameter"]:
            print(f"  • {param['name']}: {param['type']} (use: {param['use']})")
        
        if len(library["parameter"]) == 4:
            print("✅ Mixed parameters correctly parsed!")
            return True
        else:
            print(f"❌ Expected 4 parameters, got {len(library['parameter'])}")
            return False
    else:
        print("❌ No mixed parameters found!")
        return False

if __name__ == "__main__":
    print("🧪 Testing @param annotation functionality...")
    print("=" * 60)
    
    test1_passed = test_param_annotations()
    test2_passed = test_legacy_parameters() 
    test3_passed = test_mixed_parameters()
    
    print("\n" + "=" * 60)
    
    if test1_passed and test2_passed and test3_passed:
        print("🎉 All parameter tests PASSED!")
        exit(0)
    else:
        print("❌ Some parameter tests FAILED!")
        exit(1)
