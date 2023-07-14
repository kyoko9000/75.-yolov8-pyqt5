import cv2
from ultralytics import YOLO
model = YOLO("yolov8n.pt")

results = model.track(source="video1.mp4", show=True, stream=True)
count = 1
for result, frame1, frame in results:
    boxes = result[0].boxes.numpy()
    for box in boxes:
        for box in boxes:  # there could be more than one detection
            x1 = int(box.xyxy[0][0])
            y1 = int(box.xyxy[0][1])
            x2 = int(box.xyxy[0][2])
            y2 = int(box.xyxy[0][3])
            if box.id is not None:
                print("id", int(box.id[0]))
                if y1 < 185 and int(box.id[0]) == count:
                    crop_img = frame[y1:y2, x1:x2]
                    cv2.imwrite(f"save_crop/savedImage{count}.jpg", crop_img)
                    count += 1
                    print("count", count)

    cv2.imshow("cv2", frame1)
    cv2.waitKey(1)

cv2.destroyAllWindows()