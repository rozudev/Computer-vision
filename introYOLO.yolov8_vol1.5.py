from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Run interface on the source
results = model(source=0, show=True, conf=0.4, save=True)  # generator of results objects