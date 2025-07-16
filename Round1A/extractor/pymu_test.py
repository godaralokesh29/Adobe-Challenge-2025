import pymupdf4llm, pathlib

md_text = pymupdf4llm.to_markdown("E0H1CM114.pdf")
pathlib.Path("output.md").write_bytes(md_text.encode())
