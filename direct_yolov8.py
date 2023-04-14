import cv2
from ultralytics import YOLO

from measure_objects import measure

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = "video1.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # draw_frame = measure(annotated_frame)
        # cv2.imshow("YOLOv8 Inference", draw_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        for result in results:
            boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            for box in boxes:  # there could be more than one detection
                print("class", box.cls)
                print("xyxy", box.xyxy)
                print("conf", box.conf)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
