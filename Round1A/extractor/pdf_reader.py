import fitz  # PyMuPDF

def extract_blocks_from_pdf(file_path):
    doc = fitz.open(file_path)
    blocks = []
    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    spans = line["spans"]
                    if spans:
                        text = "".join(span["text"] for span in spans).strip()
                        if text:
                            blocks.append({
                                "text": text,
                                "font": spans[0]["font"],
                                "size": spans[0]["size"],
                                "page": page_num
                            })
    return blocks
