from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model

# Predict with the model
results = model('video.mp4', show=True, stream=True)  # predict on an image
for result in results:
    keypoints = result[0].keypoints.numpy()
    for keypoint in keypoints:
        print(keypoint.xy[0][0])
    # boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
    # for box in boxes:  # there could be more than one detection
    #     print("class", box.cls)
    #     print("xyxy", box.xyxy)
    #     print("conf", box.conf)