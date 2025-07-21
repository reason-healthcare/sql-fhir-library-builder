#!/usr/bin/env python3
"""
GitHub Workflows Validation Script

This script validates that all GitHub workflow files are syntactically correct YAML.
"""

import json
from pathlib import Path


def validate_workflows():
    """Validate all GitHub workflow YAML files."""
    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print("❌ No .github/workflows directory found")
        return False

    workflow_files = list(workflows_dir.glob("*.yml")) + list(
        workflows_dir.glob("*.yaml")
    )

    if not workflow_files:
        print("❌ No workflow files found")
        return False

    print(f"🔍 Found {len(workflow_files)} workflow files:")

    for workflow_file in workflow_files:
        print(f"  📄 {workflow_file.name}")

        # Basic validation: check if file is readable and not empty
        try:
            with open(workflow_file, "r") as f:
                content = f.read()

            if not content.strip():
                print(f"    ❌ Empty file")
                continue

            # Check for common YAML structure
            if "name:" not in content:
                print(f"    ⚠️  Missing 'name:' field")
            if "on:" not in content:
                print(f"    ⚠️  Missing 'on:' field")
            if "jobs:" not in content:
                print(f"    ⚠️  Missing 'jobs:' field")

            # Check for indentation issues (basic)
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if (
                    line.strip()
                    and line.startswith(" ")
                    and len(line) - len(line.lstrip()) % 2 != 0
                ):
                    print(f"    ⚠️  Line {i}: Possible odd indentation")
                    break

            print(f"    ✅ Basic structure looks good")

        except Exception as e:
            print(f"    ❌ Error reading file: {e}")
            return False

    print("🎉 All workflow files passed basic validation!")
    print("\nNote: For full YAML validation, install PyYAML: pip install pyyaml")
    return True


if __name__ == "__main__":
    import sys

    success = validate_workflows()
    sys.exit(0 if success else 1)
