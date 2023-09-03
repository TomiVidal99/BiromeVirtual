import cv2
import numpy as np

# Initialize camera capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # Create a mask to isolate green areas
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area]

    # Identify and draw the two green points
    if len(filtered_contours) >= 2:
        # Implement logic to choose the two closest points among filtered_contours
        # You can calculate centroids and find the two closest to your expected positions
        pass

    # Draw contours on the original frame
    cv2.drawContours(frame, filtered_contours, -1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Green Point Detection', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
