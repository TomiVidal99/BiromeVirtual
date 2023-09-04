"""
Comienzo de algo épico...
"""

import cv2 as cv
import numpy as np
from pynput.mouse import Button, Controller
import screeninfo
import pyautogui

MIN_AREA = 300

SCREEN_WIDTH = screeninfo.get_monitors()[0].width
SCREEN_HEIGHT = screeninfo.get_monitors()[0].height

def mapPointToScreen(x, y):
    """
    Mapea un punto a un punto en la pantalla
    """
    x_min = 0
    y_min = 0
    x_max = 640
    y_max = 480

    # Map x from its current range to the screen width
    x_mapped = int((x - x_min) / (x_max - x_min) * SCREEN_WIDTH)

    # Map y from its current range to the screen height
    y_mapped = int((y - y_min) / (y_max - y_min) * SCREEN_HEIGHT)

    return x_mapped, y_mapped


def drawGreenRects(frame, mouse):
    """
    Dibuja en la pantalla los rectangulos
    """

    # Convert frame to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([83, 100, 100])  # Lower hue value
    upper_green = np.array([90, 255, 255])  # Upper hue value

    lower_blue = np.array([100, 100, 100])  # Lower Hue, Saturation, and Value values
    upper_blue = np.array([130, 255, 255])  # Upper Hue, Saturation, and Value values

    # Create a mask to isolate green areas
    mask_green = cv.inRange(hsv, lower_green, upper_green)

    # Create a mask to isolate green areas
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the binary mask
    contours_green, _ = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area
    filtered_contours_green = [contour for contour in contours_green if cv.contourArea(contour) >= MIN_AREA]
    
    # Find contours in the binary mask
    contours_blue, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area
    filtered_contours_blue = [contour for contour in contours_blue if cv.contourArea(contour) >= MIN_AREA]

    if (len(filtered_contours_green) == 0):
        return

    if (len(filtered_contours_blue) == 0):
        return

    x1, y1, w1, h1 = cv.boundingRect(filtered_contours_green[0])
    x2, y2, w2, h2 = cv.boundingRect(filtered_contours_blue[0])
    pf = (x1, y1)
    pi = (x2, y2)
    # cv.circle(frame, pi, 10, (0, 0, 255), 2)
    # cv.circle(frame, pf, 10, (255, 255, 255), 2)
    cv.line(frame, pi, pf, (255, 0, 0), 3)
    cv.circle(frame, pf, 5, (0, 0, 255), 4)
    # mx, my = mouse.position
    # mouse.move(mx+w, my+h)
    mpx, mpy = mapPointToScreen(x1, y1)
    print(f"En la pantalla: ({mpx}, {mpy})")
    pyautogui.moveTo(mpx, mpy)


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