#!/usr/bin/env python3
"""
Quick Test Runner for SQL FHIR Library Generator Project

This is a simplified version of the test runner for quick validation.
Run this when you want a fast check of all functionality.
"""

import subprocess
import sys
from pathlib import Path


def run_quick_tests():
    """Run all tests quickly with minimal output."""

    test_files = [
        "tests/test_parser.py",
        "tests/test_fhir_integration.py",
        "tests/test_multiple_dependencies.py",
        "tests/test_name_generation.py",
        "tests/test_empty_properties.py",
        "tests/test_sql_dialect.py",
        "tests/test_dialect_version.py",
        "tests/test_parameters.py",
    ]

    print("🚀 Quick Test Run - SQL FHIR Library Generator")
    print("=" * 50)

    passed = 0
    failed = 0

    for test_file in test_files:
        if not Path(test_file).exists():
            print(f"❓ {test_file:<30} MISSING")
            failed += 1
            continue

        try:
            result = subprocess.run(
                [sys.executable, test_file], capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                print(f"✅ {test_file:<30} PASSED")
                passed += 1
            else:
                print(f"❌ {test_file:<30} FAILED")
                failed += 1

        except subprocess.TimeoutExpired:
            print(f"⏰ {test_file:<30} TIMEOUT")
            failed += 1
        except Exception as e:
            print(f"💥 {test_file:<30} ERROR: {str(e)[:30]}")
            failed += 1

    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0

    print("=" * 50)
    print(f"Results: {passed}/{total} passed ({success_rate:.0f}%)")

    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)
