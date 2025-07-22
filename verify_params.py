import json
import base64

# Read the generated FHIR Library
with open('/Users/bkaney/projects/zzz/demo_output/clinical-decision-support.json', 'r') as f:
    library = json.load(f)

# Decode the SQL content
sql_content = base64.b64decode(library['content'][0]['data']).decode('utf-8')

# Look for the parameter usage
lines = sql_content.split('\n')
for i, line in enumerate(lines, 1):
    if ':min_age' in line or ':risk_threshold' in line:
        print(f"Line {i}: {line.strip()}")
