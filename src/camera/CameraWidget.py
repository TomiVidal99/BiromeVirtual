from PyQt6.QtGui import QImage, QPixmap
import cv2 as cv
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from src.camera.Camera import Camera
from src.storage.Storage import Storage


class CameraWidget(QWidget):
    def __init__(self, storage: Storage):
        super().__init__()

        self.camera = Camera(storage)

        self.widget_layout = QVBoxLayout()
        self.label = QLabel()
        self.widget_layout.addWidget(self.label)
        self.setLayout(self.widget_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.timer.start(30)

    def update_frame(self):
        if not self.camera.startLiveFeed():
            return

        frame = self.camera.frame
        if frame is None:
            return

        height, width, channel = frame.shape
        bytes_per_line = channel * width
        qt_image = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_BGR888,
        )
        pixmap = QPixmap.fromImage(qt_image)
        self.label.setPixmap(pixmap)
