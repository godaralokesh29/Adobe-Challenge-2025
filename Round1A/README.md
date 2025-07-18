# PDF Outline Extractor (Round 1A)

## Overview
This tool extracts a structured outline (Title, H1, H2, H3 headings with page numbers) from PDF files and outputs them as JSON files in the required format for the Adobe Challenge.

## Requirements
- Python 3.8+
- pip
- [PyMuPDF](https://pymupdf.readthedocs.io/) (see requirements.txt)

## Setup
```bash
pip install -r requirements.txt
```

## Usage
1. Place your PDF files in the `input/` directory.
2. Run the main script:
   ```bash
   python main.py
   ```
3. The output JSON files will be generated in the `output/` directory, one per PDF.

## Output Format
```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Heading 1", "page": 1 },
    { "level": "H2", "text": "Subheading", "page": 2 }
  ]
}
```

## Notes
- Only font size is used for heading detection (see `extractor/heading_classifier.py`).
- For best results, use clean, well-formatted PDFs.
