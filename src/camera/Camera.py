from typing import Tuple
from PyQt6.QtGui import QColor
import cv2 as cv
import numpy as np
import pyautogui
import screeninfo

from src.utils.Log import Log
from src.storage.Storage import KEYS, Storage

MIN_AREA = 300

SCREEN_WIDTH = screeninfo.get_monitors()[0].width
SCREEN_HEIGHT = screeninfo.get_monitors()[0].height


class Camera:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.Log = Log()
        self.frame = None
        self.ret = None
        self.cap = cv.VideoCapture(0)

    def startLiveFeed(self) -> bool:
        if not self.cap or not self.cap.isOpened():
            self.Log.error("Cannot open camera")
            return False

        ret, self.frame = self.cap.read()

        self.calculatePointVector()

        if not ret:
            self.Log.error("Can't receive frame (stream end?). Exiting ...")
            return False

        return True

    def getColorFromSettings(self, key: KEYS) -> Tuple[int, int, int]:
        """
        Returns an array as HSV from a stored settings color
        """
        storedColor = self.storage.getSetting("threshold_colors", key)
        color = QColor()
        color.setNamedColor(storedColor if storedColor is not None else "")
        if not color.isValid():
            return (255, 255, 255)

        hue = color.hue()
        saturation = color.saturation()
        value = color.value()
        return (hue, saturation, value)

    def calculatePointVector(self) -> None:
        """
        Calculates the vector between A and B and moves the mouse
        """

        frame = self.frame
        if frame is None:
            return

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        a, b, c = self.getColorFromSettings("low_a")
        print(f"{a}, {b}, {c}")
        lower_A = np.array([a, b, c])
        print(lower_A)
        a, b, c = self.getColorFromSettings("high_a")
        print(f"{a}, {b}, {c}")
        upper_A = np.array([a, b, c])
        print(upper_A)

        lower_B = np.array([100, 100, 100])
        upper_B = np.array([130, 255, 255])

        mask_A = cv.inRange(hsv, lower_A, upper_A)
        mask_B = cv.inRange(hsv, lower_B, upper_B)

        contours_A, _ = cv.findContours(
            mask_A, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        filtered_contours_A = [
            contour for contour in contours_A if cv.contourArea(contour) >= MIN_AREA
        ]

        contours_B, _ = cv.findContours(
            mask_B, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        filtered_contours_B = [
            contour for contour in contours_B if cv.contourArea(contour) >= MIN_AREA
        ]

        for contour in filtered_contours_A:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        for contour in filtered_contours_B:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    def drawGreenRects(self) -> None:
        """
        Draws the rectangles in the screen
        """

        frame = self.frame
        if frame is None:
            return
        # Convert frame to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Define lower and upper bounds for green color in HSV
        lower_green = np.array([83, 100, 100])  # Lower hue value
        upper_green = np.array([90, 255, 255])  # Upper hue value

        lower_blue = np.array(
            [100, 100, 100]
        )  # Lower Hue, Saturation, and Value values
        upper_blue = np.array(
            [130, 255, 255]
        )  # Upper Hue, Saturation, and Value values

        # Create a mask to isolate green areas
        mask_green = cv.inRange(hsv, lower_green, upper_green)

        # Create a mask to isolate green areas
        mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

        # Find contours in the binary mask
        contours_green, _ = cv.findContours(
            mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        # Filter contours based on area
        filtered_contours_green = [
            contour for contour in contours_green if cv.contourArea(contour) >= MIN_AREA
        ]

        # Find contours in the binary mask
        contours_blue, _ = cv.findContours(
            mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        # Filter contours based on area
        filtered_contours_blue = [
            contour for contour in contours_blue if cv.contourArea(contour) >= MIN_AREA
        ]

        if len(filtered_contours_green) == 0:
            return

        if len(filtered_contours_blue) == 0:
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
        mpx, mpy = self.mapPointToScreen(x1, y1)
        print(f"En la pantalla: ({mpx}, {mpy})")
        pyautogui.moveTo(mpx, mpy)

    def mapPointToScreen(self, x, y):
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
