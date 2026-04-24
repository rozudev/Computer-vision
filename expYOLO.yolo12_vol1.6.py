from ultralytics import YOLO

# Load pretrained yolo12n model
model = YOLO("yolo12n.pt")

# Run interface
results = model(source=0, show=True, conf=0.4, save =True)