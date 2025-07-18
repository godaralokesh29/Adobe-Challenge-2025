import os
from extractor.heading_classifier import classify_headings
from extractor.json_writer import write_output_json

input_dir = os.environ.get("INPUT_DIR", "input")
output_dir = os.environ.get("OUTPUT_DIR", "output")

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        result = classify_headings(input_path)
        output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
        write_output_json(result, output_path)
