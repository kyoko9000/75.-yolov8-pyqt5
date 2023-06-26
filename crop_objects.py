import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture("video1.mp4")
count = 0
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
                if 195 > y1 > 185:
                    crop_img = annotated_frame[y1:y2, x1:x2]
                    # cv2.imshow("cropped", crop_img)
                    # cv2.waitKey(1)
                    count += 1
                    cv2.imwrite(f"save_crop/savedImage{count}.jpg", crop_img)

        cv2.imshow("cv2", annotated_frame)
        cv2.waitKey(1)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()


