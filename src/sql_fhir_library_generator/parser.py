"""
SQL Annotation Parser

A parser that extracts @annotations from SQL file comments and returns
them as key-value pairs.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Union


class SQLAnnotationParser:
    """
    Parses SQL files to extract @annotations from comments.

    Supports both single-line (--) and multi-line (/* */) comments.
    Annotations can be in formats:
    - @key value
    - @key: value
    - @key = value
    """

    def __init__(self):
        # Regex patterns for different comment styles and annotation formats
        self.single_line_comment_pattern = re.compile(r"--\s*(.+)", re.IGNORECASE)
        self.multi_line_comment_pattern = re.compile(
            r"/\*\s*(.*?)\s*\*/", re.DOTALL | re.IGNORECASE
        )

        # Pattern to match annotations within comments
        # Supports: @key value, @key: value, @key = value
        self.annotation_pattern = re.compile(
            r"@(\w+)(?:\s*[:=]\s*|\s+)([^@\n\r]+?)(?=@|\s*(?:--|\*/|$))",
            re.IGNORECASE | re.MULTILINE,
        )

    def parse_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Parse a SQL file and extract all annotations from comments.

        Args:
            file_path: Path to the SQL file

        Returns:
            Dictionary containing extracted annotations as key-value pairs
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")

        if not file_path.suffix.lower() in [".sql", ".ddl"]:
            raise ValueError(f"Expected SQL file, got: {file_path.suffix}")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return self.parse_content(content)

    def parse_content(self, sql_content: str) -> Dict[str, Any]:
        """
        Parse SQL content string and extract annotations from comments.

        Args:
            sql_content: SQL content as string

        Returns:
            Dictionary containing extracted annotations as key-value pairs
        """
        annotations = {}

        # Extract comments from SQL content
        comments = self._extract_comments(sql_content)

        # Parse annotations from each comment and merge them
        for comment in comments:
            comment_annotations = self._parse_annotations_from_text(comment)

            # Merge annotations, handling multiple values for same key
            for key, value in comment_annotations.items():
                if key in annotations:
                    # If key already exists, merge the values
                    existing_value = annotations[key]

                    # Convert both to lists if they aren't already
                    if not isinstance(existing_value, list):
                        existing_value = [existing_value]
                    if not isinstance(value, list):
                        value = [value]

                    # Combine the lists
                    annotations[key] = existing_value + value
                else:
                    annotations[key] = value

        return annotations

    def _extract_comments(self, sql_content: str) -> List[str]:
        """Extract all comments from SQL content."""
        comments = []

        # Find single-line comments (-- comment)
        for match in self.single_line_comment_pattern.finditer(sql_content):
            comments.append(match.group(1).strip())

        # Find multi-line comments (/* comment */)
        for match in self.multi_line_comment_pattern.finditer(sql_content):
            comments.append(match.group(1).strip())

        return comments

    def _parse_annotations_from_text(self, comment_text: str) -> Dict[str, Any]:
        """Parse annotations from a single comment text."""
        annotations = {}

        # Find all annotations in the comment
        for match in self.annotation_pattern.finditer(comment_text):
            key = match.group(1).strip()
            value = match.group(2).strip()

            # Try to convert value to appropriate type
            converted_value = self._convert_value(value)

            # Handle multiple annotations with the same key
            if key in annotations:
                # If we already have this key, convert to list
                if not isinstance(annotations[key], list):
                    annotations[key] = [annotations[key]]
                annotations[key].append(converted_value)
            else:
                annotations[key] = converted_value

        return annotations

    def _convert_value(self, value: str) -> Any:
        """
        Convert string value to appropriate Python type.

        Attempts to convert to:
        1. Boolean (true/false)
        2. Integer
        3. Float
        4. List (comma-separated values)
        5. String (default)
        """
        value = value.strip()

        # Handle boolean values
        if value.lower() in ["true", "yes", "on", "1"]:
            return True
        elif value.lower() in ["false", "no", "off", "0"]:
            return False

        # Handle numeric values
        try:
            # Try integer first
            if "." not in value and "e" not in value.lower():
                return int(value)
            else:
                return float(value)
        except ValueError:
            pass

        # Handle comma-separated lists
        if "," in value:
            items = [item.strip() for item in value.split(",")]
            # Try to convert each item
            converted_items = []
            for item in items:
                converted_items.append(self._convert_value(item))
            return converted_items

        # Handle quoted strings (remove quotes)
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]

        # Default to string
        return value

    def parse_multiple_files(
        self, file_paths: List[Union[str, Path]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Parse multiple SQL files and return annotations for each file.

        Args:
            file_paths: List of paths to SQL files

        Returns:
            Dictionary with file paths as keys and their annotations as values
        """
        results = {}

        for file_path in file_paths:
            try:
                annotations = self.parse_file(file_path)
                results[str(file_path)] = annotations
            except Exception as e:
                results[str(file_path)] = {"error": str(e)}

        return results


def main():
    """Example usage of the SQL annotation parser."""
    parser = SQLAnnotationParser()

    # Example SQL content with annotations
    example_sql = """
    -- @author: John Doe
    -- @version: 1.0
    -- @description: User table creation script
    -- @tags: users, authentication, core

    CREATE TABLE users (
        id INT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) NOT NULL
    );

    /*
    @table: users
    @created: 2024-01-15
    @last_updated: 2024-07-21
    @performance_critical: true
    @indexes: id, username, email
    */

    CREATE INDEX idx_username ON users(username);

    -- @query_type: maintenance
    -- @frequency: daily
    ANALYZE TABLE users;
    """

    # Parse the example content
    annotations = parser.parse_content(example_sql)

    print("Extracted Annotations:")
    print("=" * 40)
    for key, value in annotations.items():
        print(f"{key}: {value} (type: {type(value).__name__})")


if __name__ == "__main__":
    main()
