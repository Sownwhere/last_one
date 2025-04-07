import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

import cv2
from cvzone.ObjectDetectionModule import Detector

# Initialize the detector (using YOLO model)
detector = Detector()

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()
    
    if not ret:
        break

    # Detect persons and other objects in the frame
    img, objects = detector.update(frame)
    
    # Loop through the detected objects and draw bounding boxes around persons
    for obj in objects:
        if obj["name"] == "person":  # You can also check for other objects here
            cv2.rectangle(img, obj["top_left"], obj["bottom_right"], (255, 0, 0), 2)
            cv2.putText(img, obj["name"], obj["top_left"], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Display the frame with detected persons
    cv2.imshow("Person Detection", img)
    
    # Break if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()

