#!/usr/bin/env python3
"""
Command-line interface for converting Markdown files to JSON format.

Usage:
    python convert_markdown.py input.md [output.json] [options]

Example:
    python convert_markdown.py document.md output.json --lines-per-page 50
    python convert_markdown.py document.md --lines-per-page 40 --pretty
"""

import argparse
import json
import sys
import os
from pathlib import Path
from markdown_parser import MarkdownParser, parse_markdown_to_json


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to JSON format with document outline extraction.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md
  %(prog)s document.md output.json
  %(prog)s document.md output.json --lines-per-page 50
  %(prog)s document.md --pretty --lines-per-page 40
  %(prog)s document.md --stdout
        """
    )

    # Positional arguments
    parser.add_argument(
        'input_file',
        help='Input Markdown file path'
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output JSON file path (optional, defaults to input_file.json)'
    )

    # Optional arguments
    parser.add_argument(
        '--lines-per-page',
        type=int,
        default=50,
        help='Estimated lines per page for page number calculation (default: 50)'
    )

    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output with indentation'
    )

    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Output JSON to stdout instead of file'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate output against schema and show validation results'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Error: '{args.input_file}' is not a file.", file=sys.stderr)
        sys.exit(1)

    # Determine output file
    if args.output_file is None and not args.stdout:
        input_path = Path(args.input_file)
        args.output_file = str(input_path.with_suffix('.json'))

    if args.verbose:
        print(f"Input file: {args.input_file}")
        if not args.stdout:
            print(f"Output file: {args.output_file}")
        print(f"Lines per page: {args.lines_per_page}")
        print(f"Encoding: {args.encoding}")

    try:
        # Parse the markdown file
        if args.verbose:
            print("Parsing markdown file...")

        markdown_parser = MarkdownParser()

        # Read the file with specified encoding
        with open(args.input_file, 'r', encoding=args.encoding) as file:
            content = file.read()

        # Parse with page estimation
        result = markdown_parser.parse_with_page_estimation(content, args.lines_per_page)

        # If no headers found, try basic parsing
        if not result["outline"]:
            if args.verbose:
                print("No headers found with page estimation, trying basic parsing...")
            result = markdown_parser.parse_markdown_content(content)

        if args.verbose:
            print(f"Found {len(result['outline'])} headers")
            print(f"Document title: {result['title']}")

        # Validate if requested
        if args.validate:
            print("\n=== Validation Results ===")
            is_valid = validate_result(result)
            if not is_valid:
                print("Warning: Output does not fully conform to expected schema.")
            else:
                print("✅ Output validates successfully!")

        # Prepare JSON output
        if args.pretty:
            json_output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            json_output = json.dumps(result, ensure_ascii=False)

        # Output results
        if args.stdout:
            print(json_output)
        else:
            with open(args.output_file, 'w', encoding=args.encoding) as file:
                file.write(json_output)

            if args.verbose:
                print(f"Output written to: {args.output_file}")
                file_size = os.path.getsize(args.output_file)
                print(f"Output file size: {file_size} bytes")

    except FileNotFoundError:
        print(f"Error: Cannot access file '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: Cannot decode file with encoding '{args.encoding}': {e}", file=sys.stderr)
        print("Try specifying a different encoding with --encoding", file=sys.stderr)
        sys.exit(1)
    except json.JSONEncodeError as e:
        print(f"Error: Cannot encode result as JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def validate_result(result):
    """
    Validate the parsing result against the expected schema.

    Args:
        result (dict): The parsed result to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Check required fields
    if "title" not in result:
        print("❌ Missing 'title' field")
        return False

    if "outline" not in result:
        print("❌ Missing 'outline' field")
        return False

    if not isinstance(result["title"], str):
        print("❌ 'title' should be a string")
        return False

    if not isinstance(result["outline"], list):
        print("❌ 'outline' should be a list")
        return False

    # Check outline items
    for i, item in enumerate(result["outline"]):
        if not isinstance(item, dict):
            print(f"❌ Outline item {i} should be a dict")
            return False

        required_fields = ["level", "text", "page"]
        for field in required_fields:
            if field not in item:
                print(f"❌ Outline item {i} missing '{field}' field")
                return False

        if not isinstance(item["level"], str):
            print(f"❌ Outline item {i} 'level' should be a string")
            return False

        if not isinstance(item["text"], str):
            print(f"❌ Outline item {i} 'text' should be a string")
            return False

        if not isinstance(item["page"], int):
            print(f"❌ Outline item {i} 'page' should be an integer")
            return False

        if not item["level"].startswith("H"):
            print(f"❌ Outline item {i} 'level' should start with 'H' (got: {item['level']})")
            return False

        # Validate header level range
        valid_levels = ["H1", "H2", "H3", "H4", "H5", "H6"]
        if item["level"] not in valid_levels:
            print(f"❌ Outline item {i} invalid level '{item['level']}' (should be H1-H6)")
            return False

    return True


if __name__ == "__main__":
    main()
