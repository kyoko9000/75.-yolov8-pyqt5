import cv2
from ultralytics import YOLO

from measure_objects import measure

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
results = model('video1.mp4', show=True, stream=True)  # List of Results objects


def show_frame():
    draw_frame = measure(result, frame)
    cv2.imshow("show", draw_frame)
    cv2.waitKey(1)


for result in results:
    frame = result.plot()
    show_frame()
    # boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
    # for box in boxes:  # there could be more than one detection
    #     print("class", box.cls)
    #     print("xyxy", box.xyxy)
    #     print("conf", box.conf)
