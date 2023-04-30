import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')


def draw_rectangle(frame, xyxy, names, cls, cof):
    # 1 ====== draw cv2.putText() method ======
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    # print("xyxy", xyxy)
    org = (int(xyxy[0][0]), int(xyxy[0][1]))

    # fontScale
    fontScale = 1

    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    if int(xyxy[0][1]) < int(frame.shape[0]/2):
        # Using cv2.putText() method
        frame = cv2.putText(frame, names[cls[0]] + " " + str(round(cof[0], 2)),
                            org, font, fontScale, color, thickness, cv2.LINE_AA)

    # 2 ====== draw cv2.rectangle() method ===================
    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    start_point = (5, 5)

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    end_point = (int(frame.shape[1]), int(frame.shape[0] / 2))

    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    image = cv2.rectangle(frame, start_point, end_point, color, thickness)

    # 3 ============ resize image =============================
    scale_percent = 60  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow("zone", resized)


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

        # Display the annotated frame
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        for result in results:
            boxes = result.boxes.numpy()  # Boxes object for bbox outputs
            names = result.names
            for box in boxes:  # there could be more than one detection
                # print("class", box.cls)
                # print("xyxy", box.xyxy)
                # print("conf", box.conf)
                draw_rectangle(frame, box.xyxy, names, box.cls, box.conf)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
