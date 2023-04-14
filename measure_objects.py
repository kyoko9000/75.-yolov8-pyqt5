import cv2


def measure(frame):
    height, width, channels = frame.shape

    # Start coordinate, here (0, 0)
    start_point = (int(1/3*width), int(1/2*height))
    # End coordinate, here (250, 250)
    end_point = (int(2/3*width), int(1/2*height))
    # Green color in BGR
    color = (0, 255, 0)
    # Line thickness of 9 px
    thickness = 3

    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    image = cv2.line(frame, start_point, end_point, color, thickness)
    return image

