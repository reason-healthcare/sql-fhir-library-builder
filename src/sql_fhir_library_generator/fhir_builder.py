"""
FHIR Library Builder

Uses the SQL Annotation Parser to extract metadata from SQL files and creates
FHIR Library resources with the SQL content as base64-encoded attachments.
"""

import base64
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union, Optional
from .parser import SQLAnnotationParser


class FHIRLibraryBuilder:
    """
    Builds FHIR Library resources from SQL files using annotations for metadata.
    
    The SQL content is base64-encoded and included as an attachment in the Library resource.
    Annotations from SQL comments are mapped to appropriate FHIR Library properties.
    """
    
    def __init__(self, output_dir: str = "output"):
        self.parser = SQLAnnotationParser()
        self.output_dir = Path(output_dir)
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Mapping of common annotation keys to FHIR Library properties
        self.annotation_mappings = {
            'title': 'title',
            'name': 'name',
            'description': 'description',
            'version': 'version',
            'status': 'status',
            'author': 'author',
            'publisher': 'publisher',
            'contact': 'contact',
            'copyright': 'copyright',
            'purpose': 'purpose',
            'usage': 'usage',
            'url': 'url',
            'identifier': 'identifier',
            'date': 'date',
            'type': 'type',
            'subject': 'subject',
            'experimental': 'experimental',
            'jurisdiction': 'jurisdiction',
            'approvalDate': 'approvalDate',
            'lastReviewDate': 'lastReviewDate',
            'effectivePeriod': 'effectivePeriod'
        }
    
    def build_library_from_file(self, 
                               sql_file_path: Union[str, Path],
                               library_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a FHIR Library resource from a SQL file.
        
        Args:
            sql_file_path: Path to the SQL file
            library_id: Optional custom ID for the library (defaults to filename)
            
        Returns:
            FHIR Library resource as a dictionary
        """
        sql_file_path = Path(sql_file_path)
        
        # Read the SQL file content
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Parse annotations
        annotations = self.parser.parse_file(sql_file_path)
        
        # Generate library ID if not provided
        if not library_id:
            library_id = sql_file_path.stem.replace(' ', '-').replace('_', '-')
        
        return self.build_library_from_content(sql_content, annotations, library_id, sql_file_path.name)
    
    def build_library_from_content(self,
                                  sql_content: str,
                                  annotations: Optional[Dict[str, Any]] = None,
                                  library_id: str = "sql-library",
                                  filename: str = "query.sql") -> Dict[str, Any]:
        """
        Build a FHIR Library resource from SQL content and annotations.
        
        Args:
            sql_content: The SQL content as a string
            annotations: Dictionary of annotations (will be parsed if None)
            library_id: ID for the library resource
            filename: Original filename for the attachment
            
        Returns:
            FHIR Library resource as a dictionary
        """
        # Parse annotations if not provided
        if annotations is None:
            annotations = self.parser.parse_content(sql_content)
        
        # Base64 encode the SQL content
        sql_base64 = base64.b64encode(sql_content.encode('utf-8')).decode('utf-8')
        
        # Build the FHIR Library resource
        library = {
            "resourceType": "Library",
            "id": library_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": datetime.now().isoformat() + "Z"
            },
            "status": self._get_annotation_value(annotations, 'status', 'draft'),
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/library-type",
                        "code": "logic-library",
                        "display": "Logic Library"
                    }
                ]
            },
            "content": [
                {
                    "contentType": "application/sql",
                    "data": sql_base64,
                    "title": filename,
                    "creation": datetime.now().isoformat() + "Z"
                }
            ]
        }
        
        # Map annotations to FHIR properties
        self._apply_annotations_to_library(library, annotations)
        
        # Handle sqlDialect annotation to modify content type
        if 'sqlDialect' in annotations and annotations['sqlDialect']:
            dialect = annotations['sqlDialect'].strip().lower()
            library['content'][0]['contentType'] = f"application/{dialect}+sql"
        
        # Generate name from title if not provided
        if 'name' not in library and 'title' in library:
            library['name'] = self._camel_case_title(library['title'])
        
        # Remove empty properties
        library = self._remove_empty_properties(library)
        
        return library
    
    def _get_annotation_value(self, annotations: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Get annotation value with fallback to default."""
        return annotations.get(key, default)
    
    def _camel_case_title(self, title: str) -> str:
        """
        Convert a title to PascalCase format for FHIR name field.
        
        Args:
            title: The title string to convert
            
        Returns:
            PascalCase formatted string (first letter capitalized)
        """
        if not title:
            return ""
        
        # Replace special characters and underscores with spaces
        cleaned = re.sub(r'[^\w\s]', ' ', title)
        cleaned = re.sub(r'_', ' ', cleaned)
        
        # Split on whitespace and filter empty strings
        words = [word for word in cleaned.split() if word]
        
        if not words:
            return ""
        
        # Convert to PascalCase (all words capitalized)
        result_parts = []
        for word in words:
            if len(word) > 0:
                # Capitalize first letter, lowercase the rest
                result_parts.append(word[0].upper() + word[1:].lower())
            else:
                result_parts.append(word)
        
        return ''.join(result_parts)
    
    def _remove_empty_properties(self, library: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove empty properties from the FHIR Library resource.
        
        Args:
            library: The FHIR Library dictionary
            
        Returns:
            Cleaned library dictionary without empty properties
        """
        def is_empty(value):
            """Check if a value is considered empty."""
            if value is None:
                return True
            if isinstance(value, str) and value.strip() == "":
                return True
            if isinstance(value, (list, dict)) and len(value) == 0:
                return True
            if isinstance(value, list) and all(is_empty(item) for item in value):
                return True
            if isinstance(value, dict):
                # Check if dict has only empty values or structural keys with empty values
                non_empty_values = []
                for k, v in value.items():
                    if not is_empty(v):
                        non_empty_values.append(v)
                return len(non_empty_values) == 0
            return False
        
        def clean_dict(d):
            """Recursively clean a dictionary of empty values."""
            if not isinstance(d, dict):
                return d
            
            cleaned = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    cleaned_value = clean_dict(value)
                    if not is_empty(cleaned_value):
                        cleaned[key] = cleaned_value
                elif isinstance(value, list):
                    cleaned_list = []
                    for item in value:
                        if isinstance(item, dict):
                            cleaned_item = clean_dict(item)
                            if not is_empty(cleaned_item):
                                cleaned_list.append(cleaned_item)
                        elif not is_empty(item):
                            cleaned_list.append(item)
                    if cleaned_list:
                        cleaned[key] = cleaned_list
                elif not is_empty(value):
                    cleaned[key] = value
            
            return cleaned
        
        return clean_dict(library)
    
    def _apply_annotations_to_library(self, library: Dict[str, Any], annotations: Dict[str, Any]):
        """Apply parsed annotations to the FHIR Library resource."""
        
        # Basic string properties
        for annotation_key, fhir_key in self.annotation_mappings.items():
            if annotation_key in annotations:
                value = annotations[annotation_key]
                
                # Handle special cases
                if fhir_key == 'experimental' and isinstance(value, bool):
                    library[fhir_key] = value
                elif fhir_key == 'date' and isinstance(value, str):
                    # Try to format date properly
                    library[fhir_key] = self._format_date(value)
                elif fhir_key in ['author', 'contact'] and isinstance(value, str):
                    # Convert author/contact to proper FHIR format
                    library[fhir_key] = self._format_contact(value)
                elif fhir_key == 'identifier' and isinstance(value, str):
                    if value.strip():  # Only create identifier if value is not empty
                        library[fhir_key] = [self._format_identifier(value)]
                elif fhir_key == 'jurisdiction' and isinstance(value, (str, list)):
                    formatted_jurisdiction = self._format_jurisdiction(value)
                    if formatted_jurisdiction:  # Only add if not empty
                        library[fhir_key] = formatted_jurisdiction
                elif isinstance(value, str):
                    library[fhir_key] = value
        
        # Handle custom extensions for non-standard annotations
        extensions = []
        standard_keys = set(self.annotation_mappings.keys())
        # Add relatedDependency and sqlDialect to standard keys since we handle them specially
        standard_keys.add('relatedDependency')
        standard_keys.add('sqlDialect')
        
        for key, value in annotations.items():
            if key not in standard_keys and value is not None and str(value).strip():
                extension = {
                    "url": f"http://example.org/fhir/StructureDefinition/sql-{key}",
                    "valueString": str(value) if not isinstance(value, (bool, int, float)) else value
                }
                
                # Handle different value types
                if isinstance(value, bool):
                    extension["valueBoolean"] = value
                    del extension["valueString"]
                elif isinstance(value, int):
                    extension["valueInteger"] = value
                    del extension["valueString"]
                elif isinstance(value, float):
                    extension["valueDecimal"] = value
                    del extension["valueString"]
                elif isinstance(value, list):
                    if value:  # Only add if list is not empty
                        extension["valueString"] = ", ".join(map(str, value))
                    else:
                        continue  # Skip empty lists
                
                extensions.append(extension)
        
        if extensions:
            library["extension"] = extensions
        
        # Add additional metadata if available
        self._add_additional_metadata(library, annotations)
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to FHIR date format."""
        # Try common date formats
        common_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d", 
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S"
        ]
        
        for fmt in common_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If parsing fails, return as-is
        return date_str
    
    def _format_contact(self, contact_str: str) -> List[Dict[str, Any]]:
        """Format contact string to FHIR ContactDetail format."""
        return [
            {
                "name": contact_str,
                "telecom": []
            }
        ]
    
    def _format_identifier(self, identifier_str: str) -> Dict[str, Any]:
        """Format identifier string to FHIR Identifier format."""
        return {
            "value": identifier_str,
            "system": "http://example.org/sql-library-identifiers"
        }
    
    def _format_jurisdiction(self, jurisdiction: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """Format jurisdiction to FHIR CodeableConcept format."""
        if isinstance(jurisdiction, str):
            jurisdictions = [j.strip() for j in jurisdiction.split(',') if j.strip()]
        else:
            jurisdictions = [j.strip() for j in jurisdiction if j and str(j).strip()]
        
        # Filter out empty jurisdictions
        jurisdictions = [j for j in jurisdictions if j]
        
        if not jurisdictions:
            return []
        
        return [
            {
                "coding": [
                    {
                        "system": "urn:iso:std:iso:3166",
                        "code": j.upper() if len(j) <= 3 else j,
                        "display": j
                    }
                ]
            }
            for j in jurisdictions
        ]
    
    def _add_additional_metadata(self, library: Dict[str, Any], annotations: Dict[str, Any]):
        """Add additional metadata based on common SQL annotations."""
        
        # Handle @relatedDependency annotations - create proper FHIR relatedArtifact entries
        if 'relatedDependency' in annotations:
            if 'relatedArtifact' not in library:
                library['relatedArtifact'] = []
            
            dependencies = annotations['relatedDependency']
            if isinstance(dependencies, str):
                dependencies = [dependencies]
            elif not isinstance(dependencies, list):
                dependencies = [str(dependencies)]
            
            for dep in dependencies:
                related_artifact = {
                    "type": "depends-on",
                    "resource": str(dep).strip()
                }
                library['relatedArtifact'].append(related_artifact)
        
        # Handle database-specific metadata
        if 'database' in annotations or 'schema' in annotations:
            if 'relatedArtifact' not in library:
                library['relatedArtifact'] = []
            
            related_artifact = {
                "type": "depends-on",
                "display": f"Database: {annotations.get('database', 'Unknown')}"
            }
            
            if 'schema' in annotations:
                related_artifact['display'] += f", Schema: {annotations['schema']}"
            
            library['relatedArtifact'].append(related_artifact)
        
        # Handle table dependencies
        if 'tables' in annotations or 'dependencies' in annotations:
            dependencies = annotations.get('tables', annotations.get('dependencies'))
            if isinstance(dependencies, list):
                if 'relatedArtifact' not in library:
                    library['relatedArtifact'] = []
                
                for dep in dependencies:
                    library['relatedArtifact'].append({
                        "type": "depends-on",
                        "display": f"Table: {dep}"
                    })
        
        # Handle parameters
        if 'parameters' in annotations:
            params = annotations['parameters']
            if isinstance(params, list):
                library['parameter'] = []
                for param in params:
                    library['parameter'].append({
                        "name": str(param),
                        "type": "string"
                    })
    
    def build_multiple_libraries(self, sql_files: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        """
        Build FHIR Library resources from multiple SQL files.
        
        Args:
            sql_files: List of paths to SQL files
            
        Returns:
            List of FHIR Library resources
        """
        libraries = []
        
        for sql_file in sql_files:
            try:
                library = self.build_library_from_file(sql_file)
                libraries.append(library)
            except Exception as e:
                # Create an error library entry
                error_library = {
                    "resourceType": "Library",
                    "id": f"error-{Path(sql_file).stem}",
                    "status": "unknown",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/library-type",
                                "code": "logic-library"
                            }
                        ]
                    },
                    "extension": [
                        {
                            "url": "http://example.org/fhir/StructureDefinition/processing-error",
                            "valueString": str(e)
                        }
                    ]
                }
                libraries.append(error_library)
        
        return libraries
    
    def export_library_to_file(self, library: Dict[str, Any], output_path: Union[str, Path]):
        """
        Export a FHIR Library resource to a JSON file.
        
        Args:
            library: FHIR Library resource dictionary
            output_path: Path where to save the JSON file (relative to output_dir if not absolute)
        """
        output_path = Path(output_path)
        
        # If path is not absolute, make it relative to output directory
        if not output_path.is_absolute():
            output_path = self.output_dir / output_path
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(library, file, indent=2, ensure_ascii=False)
        
        return output_path
    
    def export_library(self, library: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """
        Export a FHIR Library resource to the output directory with auto-generated filename.
        
        Args:
            library: FHIR Library resource dictionary
            filename: Optional filename (defaults to library ID + .json)
            
        Returns:
            Path where the file was saved
        """
        if filename is None:
            library_id = library.get('id', 'library')
            filename = f"{library_id}.json"
        
        return self.export_library_to_file(library, filename)


def main():
    """Example usage of the FHIR Library Builder."""
    # Initialize builder with custom output directory
    builder = FHIRLibraryBuilder(output_dir="fhir_output")
    
    # Example SQL content with comprehensive annotations
    example_sql = """
    -- @title: User Management Queries
    -- @name: UserQueries
    -- @description: Core queries for user management system
    -- @version: 2.1.0
    -- @status: active
    -- @author: Database Team
    -- @publisher: Healthcare Systems Inc
    -- @copyright: 2024 Healthcare Systems Inc
    -- @purpose: Provides essential user management functionality
    -- @date: 2024-07-21
    -- @experimental: false
    -- @database: healthcare_db
    -- @schema: user_management
    -- @tables: users, user_profiles, user_sessions
    -- @parameters: user_id, start_date, end_date
    -- @relatedDependency: Library/patient-demographics
    -- @relatedDependency: Library/security-policies
    
    /*
    @usage: This library contains SQL queries for managing user accounts,
            including creation, updates, and reporting functionality.
    @jurisdiction: US
    @approvalDate: 2024-06-15
    @lastReviewDate: 2024-07-20
    @performance_critical: true
    @security_level: high
    @relatedDependency: Questionnaire/user-preferences, ValueSet/user-roles
    */
    
    -- Get user details
    SELECT u.id, u.username, u.email, 
           p.first_name, p.last_name
    FROM users u
    LEFT JOIN user_profiles p ON u.id = p.user_id
    WHERE u.id = :user_id;
    
    -- User activity report
    SELECT COUNT(*) as active_users
    FROM user_sessions 
    WHERE created_at BETWEEN :start_date AND :end_date;
    """
    
    # Build FHIR Library from content
    library = builder.build_library_from_content(
        sql_content=example_sql,
        library_id="user-management-queries",
        filename="user_queries.sql"
    )
    
    # Display the result
    print("FHIR Library Resource:")
    print("=" * 50)
    print(json.dumps(library, indent=2))
    
    # Export to output directory
    output_file = builder.export_library(library)
    print(f"\nExported to: {output_file}")
    
    # Example of building from files if they exist
    examples_dir = Path("examples")
    if examples_dir.exists():
        sql_files = list(examples_dir.glob("*.sql"))
        if sql_files:
            print(f"\n\nBuilding libraries from {len(sql_files)} SQL files:")
            print("=" * 50)
            
            libraries = builder.build_multiple_libraries(sql_files)
            
            for i, lib in enumerate(libraries, 1):
                print(f"\nLibrary {i}: {lib.get('id', 'unknown')}")
                print(f"Title: {lib.get('title', 'No title')}")
                print(f"Status: {lib.get('status', 'unknown')}")
                print(f"Extensions: {len(lib.get('extension', []))}")
                
                # Save to output directory
                output_file = builder.export_library(lib)
                print(f"Exported to: {output_file}")


if __name__ == "__main__":
    main()
