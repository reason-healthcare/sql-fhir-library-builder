from sql_fhir_library_generator import FHIRLibraryBuilder

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

print(f"Parameter count: {len(library.get('parameter', []))}")
for p in library.get("parameter", []):
    print(f"  {p['name']}: {p['type']}")
