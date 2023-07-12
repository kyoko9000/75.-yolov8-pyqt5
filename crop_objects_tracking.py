from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(source="video1.mp4", show=True, stream=True)
for result in results:
    if result.boxes.id is not None:
        id = result.boxes.id.cpu().numpy().astype(int)
        print(id)