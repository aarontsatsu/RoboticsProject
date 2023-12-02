import cv2
import numpy as np

def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the clicked pixel
        pixel_color = frame[y, x]
        print("RGB Color:", pixel_color)

# Open a connection to the webcam (camera index 0 by default)
cap = cv2.VideoCapture('http://192.168.106.220:4747/video?start=0')

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a window named "RGB Color Picker"
cv2.namedWindow("RGB Color Picker")
cv2.setMouseCallback("RGB Color Picker", get_color)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame in the "RGB Color Picker" window
    cv2.imshow("RGB Color Picker", frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
