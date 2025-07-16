import os
from extractor.pdf_reader import extract_blocks_from_pdf
from extractor.heading_classifier import classify_headings
from extractor.json_writer import write_output_json

input_dir = "/app/input"
output_dir = "/app/output"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        blocks = extract_blocks_from_pdf(input_path)
        result = classify_headings(blocks)
        output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
        write_output_json(result, output_path)
