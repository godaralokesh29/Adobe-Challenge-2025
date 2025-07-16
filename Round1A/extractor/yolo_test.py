from huggingface_hub import hf_hub_download
from doclayout_yolo import YOLOv10

# Download the model file to a specific location
filepath = hf_hub_download(
    repo_id="juliozhao/DocLayout-YOLO-DocStructBench", 
    filename="doclayout_yolo_docstructbench_imgsz1024.pt"
)

# Load the model using the downloaded file path
model = YOLOv10(filepath)
