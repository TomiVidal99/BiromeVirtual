"""
Comienzo de algo épico...
"""

import cv2 as cv
import numpy as np

MIN_AREA = 100

def drawGreenRects(frame):
    """
    Dibuja en la pantalla los rectangulos
    """
    # Convert frame to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([30, 100, 100])  # Lower hue value
    upper_green = np.array([90, 255, 255])  # Upper hue value

    # Create a mask to isolate green areas
    mask = cv.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if cv.contourArea(contour) >= MIN_AREA]

    # Draw bounding boxes around the green objects
    for contour in filtered_contours:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        xf = x + w
        yf = y + h
        cv.line(frame, (xf, yf), (w, h), (255, 0, 0), 2)

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # muta frame
        drawGreenRects(frame)

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv.imshow('frame', frame)

        # salir cuando apretas la Q
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()