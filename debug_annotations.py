from sql_fhir_library_generator import SQLAnnotationParser

sql_with_mixed = """
-- @title: Mixed Parameters
-- @parameters: legacy_param
-- @param: new_param integer
"""

parser = SQLAnnotationParser()
annotations = parser.parse_content(sql_with_mixed)

print("Annotations:")
for key, value in annotations.items():
    print(f"  {key}: {value} (type: {type(value)})")
