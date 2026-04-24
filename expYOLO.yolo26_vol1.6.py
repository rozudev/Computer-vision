from ultralytics import YOLO

# Load pretrained yolo26n model
model = YOLO("yolo26n.pt")

# Run interface
results = model(source=0, show=True, conf=0.4, save =True)