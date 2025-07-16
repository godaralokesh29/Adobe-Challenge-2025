def classify_headings(blocks):
    result = {
        "title": "",
        "outline": []
    }

    # Sort by size descending to find the most prominent font (likely title)
    sorted_blocks = sorted(blocks, key=lambda x: -x["size"])

    if sorted_blocks:
        result["title"] = sorted_blocks[0]["text"]
        max_size = sorted_blocks[0]["size"]

    for block in blocks:
        text = block["text"]
        size = block["size"]
        page = block["page"]

        if size >= max_size:
            continue  # Already used as title

        # Simple font size based heuristic (can be replaced by clustering or ML)
        if size > 18:
            level = "H1"
        elif size > 14:
            level = "H2"
        elif size > 12:
            level = "H3"
        else:
            continue  # Body text

        result["outline"].append({
            "level": level,
            "text": text,
            "page": page
        })

    return result
