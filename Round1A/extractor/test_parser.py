#!/usr/bin/env python3
"""
Test script for the markdown parser.
Tests various markdown formats and validates output.
"""

import json
import sys
import os
from markdown_parser import MarkdownParser, parse_markdown_to_json

def test_basic_parsing():
    """Test basic markdown parsing functionality."""
    print("=== Testing Basic Parsing ===")

    markdown_content = """
# RFP: Request for Proposal
## To Present a Proposal for Developing the Business Plan for the Ontario Digital Library
### March 21, 2003

# Ontario's Digital Library
## A Critical Component for Implementing Ontario's Road Map to Prosperity Strategy

## Summary
### Timeline:

## Background
### Equitable access for all Ontarians:
### Shared decision-making and accountability:
### Shared governance structure:
### Shared funding:
"""

    parser = MarkdownParser()
    result = parser.parse_markdown_content(markdown_content)

    print(f"Title: {result['title']}")
    print(f"Number of outline items: {len(result['outline'])}")
    print("\nOutline:")
    for item in result['outline']:
        print(f"  {item['level']}: {item['text']} (Page {item['page']})")

    return result

def test_with_line_numbers():
    """Test parsing with line number annotations."""
    print("\n=== Testing with Line Numbers ===")

    markdown_content = """
#### Ontario's Libraries Working Together [L1-2]
# **RFP: Request for Proposal** [L3-4]
## To Present a Proposal for Developing the Business Plan for the Ontario Digital Library [L5-6]
### March 21, 2003 [L7-8]
### Ontario's Digital Library [L14-15]
#### A Critical Component for Implementing Ontario's Road Map to Prosperity Strategy [L16-17]
"""

    parser = MarkdownParser()
    result = parser.parse_markdown_content(markdown_content)

    print(f"Title: {result['title']}")
    print("\nOutline:")
    for item in result['outline']:
        print(f"  {item['level']}: {item['text']} (Page {item['page']})")

    return result

def test_page_estimation():
    """Test parsing with page estimation."""
    print("\n=== Testing Page Estimation ===")

    # Create content that would span multiple pages
    lines = []
    lines.extend([f"Line {i}" for i in range(1, 30)])  # 29 lines
    lines.append("# First Header")
    lines.extend([f"Content line {i}" for i in range(1, 25)])  # 24 lines
    lines.append("## Second Header")  # This should be on page 2
    lines.extend([f"More content {i}" for i in range(1, 30)])  # 29 lines
    lines.append("### Third Header")  # This should be on page 3

    markdown_content = "\n".join(lines)

    parser = MarkdownParser()
    result = parser.parse_with_page_estimation(markdown_content, lines_per_page=50)

    print(f"Title: {result['title']}")
    print("\nOutline:")
    for item in result['outline']:
        print(f"  {item['level']}: {item['text']} (Page {item['page']})")

    return result

def test_output_md_file():
    """Test parsing the actual output.md file if it exists."""
    print("\n=== Testing output.md File ===")

    output_md_path = "output.md"
    if not os.path.exists(output_md_path):
        print(f"File {output_md_path} not found. Skipping this test.")
        return None

    try:
        result = parse_markdown_to_json(output_md_path)
        print(f"Title: {result['title']}")
        print(f"Number of outline items: {len(result['outline'])}")
        print("\nOutline:")
        for item in result['outline']:
            print(f"  {item['level']}: {item['text']} (Page {item['page']})")

        return result
    except Exception as e:
        print(f"Error parsing {output_md_path}: {e}")
        return None

def validate_against_schema(result):
    """Validate the result against the expected schema."""
    print("\n=== Schema Validation ===")

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
            print(f"❌ Outline item {i} 'level' should start with 'H'")
            return False

    print("✅ All schema validations passed!")
    return True

def compare_with_expected():
    """Compare output with the expected file03.json format."""
    print("\n=== Comparing with Expected Output ===")

    expected_file = "file03.json"
    if not os.path.exists(expected_file):
        print(f"File {expected_file} not found. Skipping comparison.")
        return

    try:
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected = json.load(f)

        print("Expected structure:")
        print(f"  Title: {expected.get('title', 'N/A')}")
        print(f"  Outline items: {len(expected.get('outline', []))}")

        # Show first few outline items
        print("  First few outline items:")
        for item in expected.get('outline', [])[:5]:
            print(f"    {item.get('level')}: {item.get('text')} (Page {item.get('page')})")

    except Exception as e:
        print(f"Error reading {expected_file}: {e}")

def save_test_results():
    """Save test results to a file."""
    print("\n=== Saving Test Results ===")

    # Test with sample content similar to expected output
    test_content = """
# RFP: Request for Proposal To Present a Proposal for Developing the Business Plan for the Ontario Digital Library

# Ontario's Digital Library
# A Critical Component for Implementing Ontario's Road Map to Prosperity Strategy

## Summary
### Timeline:

## Background
### Equitable access for all Ontarians:
### Shared decision-making and accountability:
### Shared governance structure:
### Shared funding:
### Local points of entry:
### Access:
### Guidance and Advice:
### Training:
### Provincial Purchasing & Licensing:
### Technological Support:
### What could the ODL really mean?
#### For each Ontario citizen it could mean:
#### For each Ontario student it could mean:
#### For each Ontario library it could mean:
#### For the Ontario government it could mean:

## The Business Plan to be Developed
### Milestones

## Approach and Specific Proposal Requirements

## Evaluation and Awarding of Contract

## Appendix A: ODL Envisioned Phases & Funding
### Phase I: Business Planning
### Phase II: Implementing and Transitioning
### Phase III: Operating and Growing the ODL

## Appendix B: ODL Steering Committee Terms of Reference
### 1. Preamble
### 2. Terms of Reference
### 3. Membership
### 4. Appointment Criteria and Process
### 5. Term
### 6. Chair
### 7. Meetings
### 8. Lines of Accountability and Communication
### 9. Financial and Administrative Policies

## Appendix C: ODL's Envisioned Electronic Resources
"""

    parser = MarkdownParser()
    result = parser.parse_markdown_content(test_content)

    # Assign realistic page numbers
    for i, item in enumerate(result['outline']):
        if i < 5:
            item['page'] = 1
        elif i < 15:
            item['page'] = 2
        elif i < 25:
            item['page'] = 3
        else:
            item['page'] = 4 + (i - 25) // 5

    # Save result
    output_file = "test_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Test result saved to {output_file}")
    return result

def main():
    """Run all tests."""
    print("Markdown Parser Test Suite")
    print("=" * 50)

    # Run tests
    result1 = test_basic_parsing()
    result2 = test_with_line_numbers()
    result3 = test_page_estimation()
    result4 = test_output_md_file()
    result5 = save_test_results()

    # Validate results
    test_results = [r for r in [result1, result2, result3, result4, result5] if r is not None]

    if test_results:
        print("\n" + "=" * 50)
        print("Validation Results:")
        for i, result in enumerate(test_results):
            print(f"\nTest {i+1}:")
            validate_against_schema(result)

    # Compare with expected
    compare_with_expected()

    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main()
