#!/usr/bin/env python3
"""
Replace Article Title Script

This script replaces the title (first H1 heading) in a markdown article file
with a new title. It preserves all other content in the file.

Usage:
    python replace_title.py <article_path> "<new_title>"

Example:
    python replace_title.py ./my-article.md "New Title: Exciting Subtitle"
"""

import sys
import re
from pathlib import Path


def replace_article_title(article_path: str, new_title: str) -> bool:
    """
    Replace the first H1 heading in a markdown file with a new title.

    Args:
        article_path: Path to the markdown file
        new_title: The new title to use (without the # prefix)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert to Path object for better path handling
        file_path = Path(article_path)

        # Verify file exists
        if not file_path.exists():
            print(f"Error: File not found: {article_path}", file=sys.stderr)
            return False

        # Verify it's a markdown file
        if file_path.suffix.lower() not in ['.md', '.markdown']:
            print(f"Warning: File does not have .md or .markdown extension: {article_path}", file=sys.stderr)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match the first H1 heading
        # This matches both "# Title" and "#Title" (with or without space)
        # It captures everything from start of line to the newline after the title
        h1_pattern = re.compile(r'^#\s+.*?$', re.MULTILINE)

        # Check if there's an H1 heading
        match = h1_pattern.search(content)
        if not match:
            print(f"Warning: No H1 heading found in {article_path}", file=sys.stderr)
            print("Adding new title at the beginning of the file...", file=sys.stderr)
            # If no H1 exists, add the new title at the beginning
            new_content = f"# {new_title}\n\n{content}"
        else:
            # Replace only the first H1 heading
            new_content = h1_pattern.sub(f"# {new_title}", content, count=1)

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ Successfully replaced title in: {article_path}")
        print(f"  New title: {new_title}")
        return True

    except PermissionError:
        print(f"Error: Permission denied when trying to access: {article_path}", file=sys.stderr)
        return False
    except UnicodeDecodeError:
        print(f"Error: File encoding issue. Expected UTF-8: {article_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: python replace_title.py <article_path> \"<new_title>\"", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print('  python replace_title.py ./my-article.md "New Title: Exciting Subtitle"', file=sys.stderr)
        sys.exit(1)

    article_path = sys.argv[1]
    new_title = sys.argv[2]

    # Validate that new title is not empty
    if not new_title.strip():
        print("Error: New title cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Replace the title
    success = replace_article_title(article_path, new_title)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
