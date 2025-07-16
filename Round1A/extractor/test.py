from pypdf import PdfReader
import pymupdf
import pymupdf4llm
import pathlib

# doc=pymupdf.open("../E0H1CM114.pdf")
# for page_cont in doc:
#     text=page_cont.get_text()
#     print(text)
#

md_file=pymupdf4llm.to_markdown("../E0H1CM114.pdf")

pathlib.Path("output.md").write_bytes(md_file.encode())



