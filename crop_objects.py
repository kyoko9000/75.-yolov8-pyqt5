import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture("video1.mp4")

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        for result in results:
            boxes = result.boxes.numpy()  # Boxes object for bbox outputs
            for box in boxes:  # there could be more than one detection
                print("xyxy", box.xyxy)
                x1 = int(box.xyxy[0][0])
                y1 = int(box.xyxy[0][1])
                x2 = int(box.xyxy[0][2])
                y2 = int(box.xyxy[0][3])

                print("xyxy", box.xyxy)
                if 192 > y1 > 185:
                    print("ok")

        cv2.imshow("cv2", annotated_frame)
        cv2.waitKey(1)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()


