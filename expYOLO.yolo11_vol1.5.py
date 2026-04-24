from ultralytics import YOLO

# Load pretrained yolo11n model
model = YOLO('yolo11n.pt')

# Run interface
results = model(source=0, show=True, conf=0.4, save =True)