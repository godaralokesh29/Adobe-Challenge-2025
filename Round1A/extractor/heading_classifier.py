import fitz  # PyMuPDF
from huggingface_hub import hf_hub_download
from doclayout_yolo import YOLOv10
import numpy as np
from PIL import Image

# Download and load the YOLOv10 model (do this once)
filepath = hf_hub_download(
    repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
    filename="doclayout_yolo_docstructbench_imgsz1024.pt"
)
model = YOLOv10(filepath)

# Map model class indices to heading levels (update as per model's class mapping)
CLASS_TO_LEVEL = {
    0: "Title",  # Example: 0 might be Title
    1: "H1",
    2: "H2",
    3: "H3"
    # Add more if your model supports more heading levels
}


def classify_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = ""
    for page_num, page in enumerate(doc, start=1):
        # Render page to image (RGB)
        pix = page.get_pixmap(dpi=200, colorspace=fitz.csRGB)
        img = Image.fromarray(np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n))
        # Run YOLO model
        results = model(img)
        # Each result contains boxes, class ids, and confidence
        for box, cls_id, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf):
            level = CLASS_TO_LEVEL.get(int(cls_id), None)
            if not level:
                continue
            # Crop the detected region and extract text using PyMuPDF
            x1, y1, x2, y2 = map(int, box.tolist())
            rect = fitz.Rect(x1, y1, x2, y2)
            text = page.get_textbox(rect).strip()
            if not text:
                continue
            if level == "Title" and not title:
                title = text
            else:
                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })
    if not title and outline:
        title = outline[0]["text"]
    return {"title": title, "outline": outline}
