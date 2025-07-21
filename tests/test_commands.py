#!/usr/bin/env python3
"""
Test Commands for SQL Annotation Parser Project

Provides different test execution options similar to make commands.
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command with description."""
    print(f"🔨 {description}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Test commands for SQL Annotation Parser')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test commands
    subparsers.add_parser('test', help='Run all tests (comprehensive)')
    subparsers.add_parser('test-quick', help='Run quick tests')
    subparsers.add_parser('test-parser', help='Test only the parser')
    subparsers.add_parser('test-fhir', help='Test only FHIR integration')
    subparsers.add_parser('test-dialect', help='Test only SQL dialect support')
    
    # Utility commands
    subparsers.add_parser('clean', help='Clean output directories')
    subparsers.add_parser('demo', help='Run a demo of the functionality')
    subparsers.add_parser('check', help='Check project health')
    
    args = parser.parse_args()
    
    if args.command == 'test':
        return run_command('python run_all_tests.py', 'Running comprehensive test suite')
        
    elif args.command == 'test-quick':
        return run_command('python quick_test.py', 'Running quick tests')
        
    elif args.command == 'test-parser':
        return run_command('python test_parser.py', 'Testing SQL annotation parser')
        
    elif args.command == 'test-fhir':
        return run_command('python test_fhir_integration.py', 'Testing FHIR integration')
        
    elif args.command == 'test-dialect':
        return run_command('python test_sql_dialect.py', 'Testing SQL dialect support')
        
    elif args.command == 'clean':
        success = True
        for dir_name in ['test_output', 'fhir_libraries', 'output']:
            success &= run_command(f'rm -rf {dir_name}', f'Cleaning {dir_name}/')
        return success
        
    elif args.command == 'demo':
        return run_command('python test_fhir_integration.py', 'Running integration demo')
        
    elif args.command == 'check':
        print("🔍 Project Health Check")
        print("=" * 30)
        
        # Check required files
        required_files = [
            'sql_annotation_parser.py',
            'fhir_library_builder.py',
            'examples/sql_on_fhir_example.sql'
        ]
        
        all_good = True
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} (missing)")
                all_good = False
                
        if all_good:
            print("\n🎉 Project is healthy!")
        else:
            print("\n❌ Project has issues")
            
        return all_good
        
    else:
        parser.print_help()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
