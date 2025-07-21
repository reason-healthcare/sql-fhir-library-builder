#!/usr/bin/env python3
"""
Test Runner for SQL FHIR Library Generator Project

This script runs all tests for the SQL FHIR Library Generator and FHIR library builder,
providing a comprehensive test suite with organized output and error handling.
"""

import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class TestRunner:
    """Runs all tests and provides consolidated reporting."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.results = []
        self.start_time = None
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

        # Define test files in order of execution
        self.test_files = [
            ("tests/test_parser.py", "Core SQL Annotation Parser Tests"),
            ("tests/test_fhir_integration.py", "FHIR Library Integration Tests"),
            (
                "tests/test_multiple_dependencies.py",
                "Multiple Dependencies Support Tests",
            ),
            ("tests/test_name_generation.py", "Automatic Name Generation Tests"),
            ("tests/test_empty_properties.py", "Empty Property Removal Tests"),
            ("tests/test_sql_dialect.py", "SQL Dialect Annotation Tests"),
            ("tests/test_dialect_version.py", "Dialect Version Annotation Tests"),
        ]

    def print_banner(self, title: str, width: int = 80, char: str = "="):
        """Print a formatted banner."""
        print(char * width)
        print(f"{title:^{width}}")
        print(char * width)

    def print_section(self, title: str, width: int = 60, char: str = "-"):
        """Print a section separator."""
        print(f"\n{char * width}")
        print(f"{title}")
        print(f"{char * width}")

    def run_test_file(self, test_file: str, description: str) -> bool:
        """Run a single test file and capture results."""
        test_path = self.project_root / test_file

        if not test_path.exists():
            print(f"❌ Test file not found: {test_file}")
            self.results.append(
                {
                    "file": test_file,
                    "description": description,
                    "status": "MISSING",
                    "execution_time": 0,
                    "output": f"Test file {test_file} not found",
                    "error": None,
                }
            )
            return False

        print(f"🧪 Running: {description}")
        print(f"   File: {test_file}")

        start_time = time.time()

        try:
            # Run the test file
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout per test
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                print(f"   ✅ PASSED ({execution_time:.2f}s)")
                status = "PASSED"
                self.passed_tests += 1
            else:
                print(f"   ❌ FAILED ({execution_time:.2f}s)")
                status = "FAILED"
                self.failed_tests += 1
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")

            self.results.append(
                {
                    "file": test_file,
                    "description": description,
                    "status": status,
                    "execution_time": execution_time,
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None,
                }
            )

            return status == "PASSED"

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"   ⏰ TIMEOUT ({execution_time:.2f}s)")
            self.results.append(
                {
                    "file": test_file,
                    "description": description,
                    "status": "TIMEOUT",
                    "execution_time": execution_time,
                    "output": "Test timed out after 60 seconds",
                    "error": "Timeout",
                }
            )
            self.failed_tests += 1
            return False

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"   💥 ERROR ({execution_time:.2f}s): {e}")
            self.results.append(
                {
                    "file": test_file,
                    "description": description,
                    "status": "ERROR",
                    "execution_time": execution_time,
                    "output": str(e),
                    "error": str(e),
                }
            )
            self.failed_tests += 1
            return False

    def cleanup_test_outputs(self):
        """Clean up test output directories before running tests."""
        print("🧹 Cleaning up previous test outputs...")

        cleanup_dirs = ["test_output", "fhir_libraries", "output"]
        for dir_name in cleanup_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"   Removed: {dir_name}/")
                except Exception as e:
                    print(f"   Warning: Could not remove {dir_name}/: {e}")

    def check_dependencies(self):
        """Check if all required files and dependencies exist."""
        print("🔍 Checking project dependencies...")

        required_files = [
            "src/sql_fhir_library_generator/__init__.py",
            "src/sql_fhir_library_generator/parser.py",
            "src/sql_fhir_library_generator/fhir_builder.py",
            "examples/sql_on_fhir_example.sql",
            "examples/hive_example.sql",
            "examples/spark_example.sql",
            "examples/postgres_example.sql",
            "examples/hive_with_version.sql",
            "examples/postgres_with_version.sql",
        ]

        missing_files = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            print("   ❌ Missing required files:")
            for file_path in missing_files:
                print(f"      - {file_path}")
            return False
        else:
            print("   ✅ All required files present")
            return True

    def run_all_tests(self):
        """Run all tests in sequence."""
        self.start_time = time.time()

        self.print_banner("SQL FHIR LIBRARY GENERATOR - TEST SUITE")
        print(f"Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working directory: {self.project_root}")
        print()

        # Check dependencies
        if not self.check_dependencies():
            print("\n❌ Dependency check failed. Cannot proceed with tests.")
            return False

        # Cleanup previous test outputs
        self.cleanup_test_outputs()

        # Run all tests
        self.print_section("RUNNING TESTS")

        for test_file, description in self.test_files:
            self.total_tests += 1
            self.run_test_file(test_file, description)

        # Generate summary report
        self.generate_summary_report()

        return self.failed_tests == 0

    def generate_summary_report(self):
        """Generate a comprehensive test summary report."""
        total_time = time.time() - self.start_time

        self.print_banner("TEST RESULTS SUMMARY")

        print(f"📊 Test Execution Summary:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.failed_tests}")
        print(
            f"   Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%"
            if self.total_tests > 0
            else "   Success Rate: N/A"
        )
        print(f"   Total Execution Time: {total_time:.2f}s")
        print()

        # Detailed results
        print("📋 Detailed Results:")
        for result in self.results:
            status_emoji = {
                "PASSED": "✅",
                "FAILED": "❌",
                "TIMEOUT": "⏰",
                "ERROR": "💥",
                "MISSING": "❓",
            }.get(result["status"], "❔")

            print(
                f"   {status_emoji} {result['file']:<30} {result['status']:<8} ({result['execution_time']:.2f}s)"
            )
            if result["status"] != "PASSED" and result["error"]:
                print(
                    f"      Error: {result['error'][:100]}{'...' if len(result['error']) > 100 else ''}"
                )

        print()

        # Final status
        if self.failed_tests == 0:
            print(
                "🎉 ALL TESTS PASSED! The SQL FHIR Library Generator is working correctly."
            )
        else:
            print(
                f"❌ {self.failed_tests} test(s) failed. Please review the output above."
            )

        # Show generated outputs
        self.show_generated_outputs()

    def show_generated_outputs(self):
        """Show what outputs were generated during testing."""
        print("\n📁 Generated Test Outputs:")

        output_dirs = ["test_output", "fhir_libraries", "output"]
        found_outputs = False

        for dir_name in output_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and any(dir_path.iterdir()):
                found_outputs = True
                print(f"\n   {dir_name}/")
                try:
                    for file_path in sorted(dir_path.glob("*.json")):
                        file_size = file_path.stat().st_size
                        print(f"      - {file_path.name} ({file_size} bytes)")
                except Exception as e:
                    print(f"      Error reading directory: {e}")

        if not found_outputs:
            print("   No output files generated (this may indicate test failures)")


def main():
    """Main entry point for the test runner."""
    runner = TestRunner()

    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Test run interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n\n💥 Test runner encountered an error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
