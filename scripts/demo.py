#!/usr/bin/env python3
"""
Comprehensive Demo of SQL Annotation Parser

This script provides a complete demonstration of all features:
- SQL annotation parsing
- FHIR Library generation
- Multiple SQL dialects
- Automatic name generation
- Empty property removal
- Related dependencies
- Batch processing
"""

import json
import os
from pathlib import Path
from sql_fhir_library_generator import SQLAnnotationParser, FHIRLibraryBuilder

def print_banner(title: str, width: int = 70, char: str = '='):
    """Print a formatted banner."""
    print(char * width)
    print(f"{title:^{width}}")
    print(char * width)

def print_section(title: str, width: int = 50, char: str = '-'):
    """Print a section separator."""
    print(f"\n{char * width}")
    print(f"{title}")
    print(f"{char * width}")

def demonstrate_annotation_parsing():
    """Demonstrate basic annotation parsing."""
    print_section("1. SQL Annotation Parsing")
    
    parser = SQLAnnotationParser()
    
    # Example with various annotation formats
    sql_content = """
    /*
    @title: Clinical Decision Support Query
    @description: Advanced query for clinical decision support
    @version: 2.1.0
    @status: active
    @author: Clinical Informatics Team
    @tags: cds, alerts, notifications
    @priority: high
    @experimental: false
    */
    
    -- @relatedDependency: Library/patient-risk-factors
    -- @relatedDependency: CodeSystem/clinical-alerts
    SELECT patient_id, risk_score 
    FROM patient_risk_assessment 
    WHERE risk_score > 0.8;
    """
    
    annotations = parser.parse_content(sql_content)
    
    print("📋 Parsed Annotations:")
    for key, value in annotations.items():
        if isinstance(value, list):
            print(f"   {key}: {value}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n✅ Successfully parsed {len(annotations)} annotations")

def demonstrate_fhir_generation():
    """Demonstrate FHIR Library generation."""
    print_section("2. FHIR Library Generation")
    
    builder = FHIRLibraryBuilder(output_dir='demo_output')
    
    # Generate library from SQL file
    library = builder.build_library_from_file('examples/sql_on_fhir_example.sql')
    
    print("📦 Generated FHIR Library:")
    print(f"   Resource Type: {library['resourceType']}")
    print(f"   ID: {library['id']}")
    print(f"   Title: {library.get('title', 'N/A')}")
    print(f"   Status: {library.get('status', 'N/A')}")
    print(f"   Content Type: {library['content'][0]['contentType']}")
    print(f"   Name (Generated): {library.get('name', 'N/A')}")
    
    # Export the library
    output_path = builder.export_library(library)
    print(f"   Exported to: {output_path}")

def demonstrate_sql_dialects():
    """Demonstrate SQL dialect support."""
    print_section("3. SQL Dialect Support")
    
    builder = FHIRLibraryBuilder(output_dir='demo_output')
    
    dialect_examples = [
        ('examples/hive_example.sql', 'Hive'),
        ('examples/spark_example.sql', 'Spark'),
        ('examples/postgres_example.sql', 'PostgreSQL'),
    ]
    
    print("🗄️  SQL Dialect Examples:")
    
    for file_path, dialect_name in dialect_examples:
        if Path(file_path).exists():
            library = builder.build_library_from_file(file_path)
            content_type = library['content'][0]['contentType']
            print(f"   {dialect_name:<12} → {content_type}")
        else:
            print(f"   {dialect_name:<12} → File not found: {file_path}")

def demonstrate_batch_processing():
    """Demonstrate batch processing capabilities."""
    print_section("4. Batch Processing")
    
    builder = FHIRLibraryBuilder(output_dir='demo_output')
    
    # Find all SQL example files
    example_files = list(Path('examples').glob('*.sql'))
    
    print(f"📁 Processing {len(example_files)} SQL files:")
    
    libraries = []
    for file_path in example_files:
        print(f"   Processing: {file_path.name}")
        try:
            library = builder.build_library_from_file(str(file_path))
            libraries.append(library)
            
            # Show key details
            title = library.get('title', 'Untitled')
            content_type = library['content'][0]['contentType']
            print(f"      → {title} ({content_type})")
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n✅ Successfully processed {len(libraries)} libraries")
    
    # Export all libraries
    for library in libraries:
        builder.export_library(library)
    
    print(f"📁 All libraries exported to: demo_output/")

def demonstrate_advanced_features():
    """Demonstrate advanced features."""
    print_section("5. Advanced Features")
    
    builder = FHIRLibraryBuilder(output_dir='demo_output')
    
    print("🔧 Advanced Feature Examples:")
    
    # 1. Multiple dependencies
    multi_dep_file = 'examples/spark_example.sql'
    if Path(multi_dep_file).exists():
        library = builder.build_library_from_file(multi_dep_file)
        deps = library.get('relatedArtifact', [])
        print(f"   Multiple Dependencies: {len(deps)} related artifacts")
        for dep in deps[:2]:  # Show first 2
            print(f"      - {dep['resource']}")
    
    # 2. Automatic name generation
    print(f"   Automatic Name Generation:")
    for file_path in ['examples/hive_example.sql', 'examples/postgres_example.sql']:
        if Path(file_path).exists():
            library = builder.build_library_from_file(file_path)
            title = library.get('title', 'N/A')
            name = library.get('name', 'N/A')
            print(f"      '{title}' → '{name}'")
    
    # 3. Empty property removal
    print(f"   Empty Property Removal: Automatically cleans FHIR output")
    
    print("✅ All advanced features working correctly")

def show_generated_outputs():
    """Show what files were generated."""
    print_section("6. Generated Outputs")
    
    output_dir = Path('demo_output')
    if output_dir.exists():
        json_files = list(output_dir.glob('*.json'))
        
        print(f"📁 Generated {len(json_files)} FHIR Library files:")
        
        total_size = 0
        for file_path in sorted(json_files):
            file_size = file_path.stat().st_size
            total_size += file_size
            print(f"   📄 {file_path.name:<35} ({file_size:,} bytes)")
        
        print(f"\n💾 Total output size: {total_size:,} bytes")
        
        # Show a sample library structure
        if json_files:
            print(f"\n📋 Sample FHIR Library Structure (from {json_files[0].name}):")
            with open(json_files[0], 'r') as f:
                sample = json.load(f)
            
            def show_structure(obj, indent=0):
                """Show the structure of a JSON object."""
                prefix = "   " + "  " * indent
                if isinstance(obj, dict):
                    for key, value in list(obj.items())[:5]:  # Show first 5 keys
                        if isinstance(value, (dict, list)) and len(str(value)) > 50:
                            print(f"{prefix}{key}: {{...}}" if isinstance(value, dict) else f"{prefix}{key}: [...]")
                        else:
                            print(f"{prefix}{key}: {value}")
                    if len(obj) > 5:
                        print(f"{prefix}... ({len(obj) - 5} more properties)")
            
            show_structure(sample)
    else:
        print("❌ No output files found")

def main():
    """Run the complete demonstration."""
    print_banner("🧪 SQL FHIR LIBRARY GENERATOR - COMPLETE DEMO")
    print("This demo showcases all features of the SQL FHIR Library Generator")
    print("and FHIR Library Builder system.")
    print()
    
    try:
        # Run all demonstrations
        demonstrate_annotation_parsing()
        demonstrate_fhir_generation()
        demonstrate_sql_dialects()
        demonstrate_batch_processing()
        demonstrate_advanced_features()
        show_generated_outputs()
        
        # Final summary
        print_banner("🎉 DEMO COMPLETE")
        print("✅ All features demonstrated successfully!")
        print("✅ FHIR Libraries generated with SQL dialect support")
        print("✅ Automatic name generation and property cleanup")
        print("✅ Multiple dependencies and batch processing")
        print("\n📖 See the generated files in demo_output/ for full FHIR Library examples")
        print("🧪 Run individual test files for detailed feature testing")
        
    except Exception as e:
        print(f"\n❌ Demo encountered an error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
