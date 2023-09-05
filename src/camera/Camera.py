import cv2 as cv

from src.utils.Log import Log


class Camera:
    def __init__(self):
        self.Log = Log()
        self.frame = None
        self.ret = None
        self.cap = cv.VideoCapture(0)

    def startLiveFeed(self) -> bool:
        if not self.cap or not self.cap.isOpened():
            self.Log.error("Cannot open camera")
            return False

        ret, self.frame = self.cap.read()

        if not ret:
            self.Log.error("Can't receive frame (stream end?). Exiting ...")
            return False

        return True
