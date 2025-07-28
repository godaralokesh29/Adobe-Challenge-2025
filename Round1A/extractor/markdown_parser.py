import re
import json
from typing import Dict, List, Any, Optional

class MarkdownParser:
    """
    A parser to convert markdown files to JSON format following the specified schema.
    """

    def __init__(self):
        self.title = ""
        self.outline = []
        self.current_page = 1

    def parse_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a markdown file and return JSON structure.

        Args:
            file_path (str): Path to the markdown file

        Returns:
            Dict[str, Any]: JSON structure with title and outline
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return self.parse_markdown_content(content)

    def parse_markdown_content(self, content: str) -> Dict[str, Any]:
        """
        Parse markdown content and return JSON structure.

        Args:
            content (str): Markdown content as string

        Returns:
            Dict[str, Any]: JSON structure with title and outline
        """
        self.title = ""
        self.outline = []
        self.current_page = 1

        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Check if it's a header
            header_match = self._parse_header(line)
            if header_match:
                level, text, page = header_match

                # Set title from first significant header (H1 or H2)
                if not self.title and level in ['H1', 'H2']:
                    self.title = text.strip()

                # Add to outline
                self.outline.append({
                    "level": level,
                    "text": text.strip(),
                    "page": page if page else self.current_page
                })

        # If no title was found, try to extract from first outline item
        if not self.title and self.outline:
            self.title = self.outline[0]["text"]

        return {
            "title": self.title,
            "outline": self.outline
        }

    def _parse_header(self, line: str) -> Optional[tuple]:
        """
        Parse a header line and extract level, text, and page number.

        Args:
            line (str): Line to parse

        Returns:
            tuple: (level, text, page) or None if not a header
        """
        # Pattern to match markdown headers with optional line numbers and page info
        header_pattern = r'^(#{1,6})\s*\**(.*?)\**\s*(?:\[L?\d+-?\d*\])?(?:\s*\[.*?\])?\s*$'
        match = re.match(header_pattern, line)

        if match:
            hash_count = len(match.group(1))
            text = match.group(2).strip()

            # Remove markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
            text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
            text = re.sub(r'`(.*?)`', r'\1', text)        # Code

            # Map hash count to header level
            level_map = {1: 'H1', 2: 'H2', 3: 'H3', 4: 'H4', 5: 'H5', 6: 'H6'}
            level = level_map.get(hash_count, 'H1')

            # Try to extract page number from line
            page = self._extract_page_number(line)

            return (level, text, page)

        return None

    def _extract_page_number(self, line: str) -> int:
        """
        Extract page number from line, if available.

        Args:
            line (str): Line to extract page from

        Returns:
            int: Page number or current page
        """
        # Look for page indicators in various formats
        page_patterns = [
            r'\[.*?(\d+).*?\]',  # [L1-2] or [page 1] etc.
            r'page\s*(\d+)',     # "page 1"
            r'p\.?\s*(\d+)',     # "p. 1" or "p1"
        ]

        for pattern in page_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return self.current_page

    def parse_with_page_estimation(self, content: str, lines_per_page: int = 50) -> Dict[str, Any]:
        """
        Parse markdown content with page estimation based on line count.

        Args:
            content (str): Markdown content
            lines_per_page (int): Estimated lines per page

        Returns:
            Dict[str, Any]: JSON structure with title and outline
        """
        self.title = ""
        self.outline = []

        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Estimate current page
            estimated_page = max(1, (line_num - 1) // lines_per_page + 1)
            self.current_page = estimated_page

            # Check if it's a header
            header_match = self._parse_header(line)
            if header_match:
                level, text, page = header_match

                # Set title from first significant header
                if not self.title and level in ['H1', 'H2']:
                    self.title = text.strip()

                # Add to outline with estimated page if no page found
                self.outline.append({
                    "level": level,
                    "text": text.strip(),
                    "page": page if page != self.current_page else estimated_page
                })

        # If no title was found, try to extract from first outline item
        if not self.title and self.outline:
            self.title = self.outline[0]["text"]

        return {
            "title": self.title,
            "outline": self.outline
        }


def parse_markdown_to_json(input_file: str, output_file: str = None, lines_per_page: int = 50) -> Dict[str, Any]:
    """
    Convenience function to parse markdown file to JSON.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output JSON file
        lines_per_page (int): Lines per page for page estimation

    Returns:
        Dict[str, Any]: Parsed JSON structure
    """
    parser = MarkdownParser()

    # Parse the file
    result = parser.parse_markdown_file(input_file)

    # If no headers found, try with page estimation
    if not result["outline"]:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        result = parser.parse_with_page_estimation(content, lines_per_page)

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=2, ensure_ascii=False)

    return result


# Example usage
if __name__ == "__main__":
    # Example 1: Parse a markdown file
    # result = parse_markdown_to_json("input.md", "output.json")
    # print(json.dumps(result, indent=2))

    # Example 2: Parse markdown content directly
    markdown_content = """
# Main Title
## Introduction
### Overview
#### Details
## Background
### History
### Current State
## Conclusion
    """

    parser = MarkdownParser()
    result = parser.parse_markdown_content(markdown_content)
    print(json.dumps(result, indent=2))
