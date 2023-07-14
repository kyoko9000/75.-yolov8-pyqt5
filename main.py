import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
results = model('video1.mp4', show=True, stream=True)  # List of Results objects


def show_frame():
    cv2.imshow("show", frame)
    cv2.waitKey(1)


for result, frame in results:
    show_frame()
    boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
