# Markdown to JSON Parser

A Python tool for extracting document outlines from Markdown files and converting them to structured JSON format. This parser is specifically designed to extract heading hierarchies and generate document outlines with page number estimation.

## Features

- **Header Extraction**: Automatically detects and extracts Markdown headers (H1-H6)
- **Page Number Estimation**: Estimates page numbers based on line count or extracts from header annotations
- **Line Number Support**: Parses line number annotations like `[L1-2]` from headers
- **Schema Validation**: Validates output against predefined JSON schema
- **Multiple Output Formats**: Support for pretty-printed JSON and stdout output
- **Command Line Interface**: Easy-to-use CLI for batch processing
- **Flexible Parsing**: Handles various Markdown formatting styles

## Installation

No external dependencies required - uses only Python standard library.

```bash
# Clone or download the parser files
# Ensure you have Python 3.6+ installed
python --version
```

## Quick Start

### Command Line Usage

```bash
# Basic usage - convert markdown to JSON
python convert_markdown.py document.md

# Specify output file
python convert_markdown.py document.md output.json

# Pretty print with validation
python convert_markdown.py document.md --pretty --validate --verbose

# Output to stdout
python convert_markdown.py document.md --stdout --pretty

# Custom page estimation
python convert_markdown.py document.md --lines-per-page 40
```

### Python API Usage

```python
from markdown_parser import MarkdownParser, parse_markdown_to_json

# Method 1: Parse file directly
result = parse_markdown_to_json("document.md", "output.json")
print(result)

# Method 2: Parse content string
parser = MarkdownParser()
markdown_content = """
# Main Title
## Section 1
### Subsection 1.1
## Section 2
"""
result = parser.parse_markdown_content(markdown_content)
print(result)

# Method 3: Parse with page estimation
result = parser.parse_with_page_estimation(markdown_content, lines_per_page=50)
print(result)
```

## Output Format

The parser generates JSON output following this schema:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Header Text",
      "page": 1
    }
  ]
}
```

### Schema Details

- **title** (string): Document title extracted from the first significant header
- **outline** (array): List of header objects
  - **level** (string): Header level (H1, H2, H3, H4, H5, H6)
  - **text** (string): Clean header text without markdown formatting
  - **page** (integer): Estimated or extracted page number

## Supported Markdown Formats

### Basic Headers

```markdown
# Level 1 Header
## Level 2 Header
### Level 3 Header
#### Level 4 Header
##### Level 5 Header
###### Level 6 Header
```

### Headers with Formatting

```markdown
# **Bold Header**
## *Italic Header*
### `Code Header`
#### Mixed **bold** and *italic*
```

### Headers with Line Numbers

```markdown
# Header [L1-2]
## Another Header [L5-6]
### Header with page info [page 3]
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Input Markdown file path | Required |
| `output_file` | Output JSON file path | `input_file.json` |
| `--lines-per-page` | Lines per page for estimation | 50 |
| `--pretty` | Pretty-print JSON output | False |
| `--stdout` | Output to stdout instead of file | False |
| `--validate` | Validate output against schema | False |
| `--verbose` | Enable verbose output | False |
| `--encoding` | File encoding | utf-8 |

## Examples

### Example 1: Basic Document

**Input:** `sample.md`
```markdown
# Project Documentation
## Introduction
### Overview
### Goals
## Implementation
### Phase 1
### Phase 2
## Conclusion
```

**Output:** `sample.json`
```json
{
  "title": "Project Documentation",
  "outline": [
    {"level": "H1", "text": "Project Documentation", "page": 1},
    {"level": "H2", "text": "Introduction", "page": 1},
    {"level": "H3", "text": "Overview", "page": 1},
    {"level": "H3", "text": "Goals", "page": 1},
    {"level": "H2", "text": "Implementation", "page": 1},
    {"level": "H3", "text": "Phase 1", "page": 1},
    {"level": "H3", "text": "Phase 2", "page": 1},
    {"level": "H2", "text": "Conclusion", "page": 1}
  ]
}
```

### Example 2: Document with Line Numbers

**Input:**
```markdown
#### Preface [L1-2]
# **Main Title** [L3-4]
## Section One [L5-10]
### Subsection A [L11-15]
## Section Two [L16-20]
```

**Output:**
```json
{
  "title": "Main Title",
  "outline": [
    {"level": "H4", "text": "Preface", "page": 1},
    {"level": "H1", "text": "Main Title", "page": 3},
    {"level": "H2", "text": "Section One", "page": 5},
    {"level": "H3", "text": "Subsection A", "page": 11},
    {"level": "H2", "text": "Section Two", "page": 16}
  ]
}
```

## API Reference

### MarkdownParser Class

#### Methods

##### `parse_markdown_file(file_path: str) -> Dict[str, Any]`
Parse a markdown file and return JSON structure.

**Parameters:**
- `file_path` (str): Path to the markdown file

**Returns:**
- `Dict[str, Any]`: JSON structure with title and outline

##### `parse_markdown_content(content: str) -> Dict[str, Any]`
Parse markdown content string and return JSON structure.

**Parameters:**
- `content` (str): Markdown content as string

**Returns:**
- `Dict[str, Any]`: JSON structure with title and outline

##### `parse_with_page_estimation(content: str, lines_per_page: int = 50) -> Dict[str, Any]`
Parse markdown content with page estimation based on line count.

**Parameters:**
- `content` (str): Markdown content
- `lines_per_page` (int): Estimated lines per page (default: 50)

**Returns:**
- `Dict[str, Any]`: JSON structure with title and outline

### Utility Functions

##### `parse_markdown_to_json(input_file: str, output_file: str = None, lines_per_page: int = 50) -> Dict[str, Any]`
Convenience function to parse markdown file to JSON.

**Parameters:**
- `input_file` (str): Path to input markdown file
- `output_file` (str, optional): Path to output JSON file
- `lines_per_page` (int): Lines per page for page estimation

**Returns:**
- `Dict[str, Any]`: Parsed JSON structure

## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python test_parser.py

# The test suite includes:
# - Basic parsing tests
# - Line number parsing tests
# - Page estimation tests
# - Schema validation tests
# - Comparison with expected output
```

## Error Handling

The parser handles various error conditions gracefully:

- **File not found**: Clear error message with file path
- **Encoding issues**: Suggestion to try different encoding
- **Invalid JSON**: JSON encoding error details
- **Schema validation**: Detailed validation error messages

## Limitations

- Page number estimation is approximate and based on line count
- Complex Markdown features (tables, code blocks, etc.) are not considered for page breaks
- Headers inside code blocks or quotes are still processed
- Very large files may require memory optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Changelog

### Version 1.0.0
- Initial release
- Basic header parsing
- Page number estimation
- Command line interface
- Schema validation
- Test suite