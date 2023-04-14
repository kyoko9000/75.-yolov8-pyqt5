import cv2


def measure(result, frame):
    height, width, channels = frame.shape

    # Start coordinate, here (0, 0)
    start_point = (int(1/3*width), int(1/4*height))
    # End coordinate, here (250, 250)
    end_point = (int(2/3*width), int(1/4*height))
    # Green color in BGR
    color = (0, 255, 0)
    # Line thickness of 9 px
    thickness = 3

    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    image = cv2.line(frame, start_point, end_point, color, thickness)

    boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
    for box in boxes:  # there could be more than one detection
        print("class", box.cls)
        print("xyxy", box.xyxy)
        print("conf", box.conf)

    return image

