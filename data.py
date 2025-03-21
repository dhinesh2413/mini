from ultralytics import YOLO

model = YOLO("yolo12n.pt")
model.train(data="C:/GENAI/dataset/vehicle_dataset/data.yaml",epochs=5, imgsz=320, batch=16, amp=True)
