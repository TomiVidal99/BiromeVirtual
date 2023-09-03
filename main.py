"""
Comienzo de algo épico...
"""

import cv2 as cv
import numpy as np
from pynput.mouse import Button, Controller

MIN_AREA = 300

def drawGreenRects(frame, mouse):
    """
    Dibuja en la pantalla los rectangulos
    """

    # Convert frame to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([80, 100, 100])  # Lower hue value
    upper_green = np.array([90, 255, 255])  # Upper hue value

    lower_blue = np.array([100, 100, 100])  # Lower Hue, Saturation, and Value values
    upper_blue = np.array([130, 255, 255])  # Upper Hue, Saturation, and Value values

    # Create a mask to isolate green areas
    mask_green = cv.inRange(hsv, lower_green, upper_green)

    # Create a mask to isolate green areas
    mask_blue = cv.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary mask
    contours, _ = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    contours, _ = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if cv.contourArea(contour) >= MIN_AREA]

    # Draw bounding boxes around the green objects
    max_contours = 0
    for contour in filtered_contours:
        if (max_contours > 1):
            break
        x, y, w, h = cv.boundingRect(contour)
        # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv.line(frame, (xf, yf), (w, h), (255, 0, 0), 2)
        max_contours += 1

    if (len(filtered_contours) < 2):
        return
    

    x1, y1, w1, h1 = cv.boundingRect(filtered_contours[0])
    x2, y2, w2, h2 = cv.boundingRect(filtered_contours[1])
    pf = (x1, y1)
    pi = (x2, y2)
    # cv.circle(frame, pi, 10, (0, 0, 255), 2)
    # cv.circle(frame, pf, 10, (255, 255, 255), 2)
    cv.line(frame, pi, pf, (255, 0, 0), 3)
    cv.circle(frame, pf, 5, (0, 0, 255), 4)
    # mx, my = mouse.position
    # mouse.move(mx+w, my+h)


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    mouse = Controller()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # muta frame
        drawGreenRects(frame, mouse)

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