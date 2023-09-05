from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
import cv2 as cv
from src.camera.CameraWidget import CameraWidget
from src.GUI.app_ui import Ui_MainWindow

from src.storage.Storage import Storage
from src.utils.Log import Log
from src.camera.Camera import Camera


class App(QMainWindow):
    """
    App englobes all the other scripts/classes
    and it's like the entry point
    """

    def __init__(self) -> None:
        super().__init__()
        self.appname = "BiromeVirtual"
        self.Log = Log()
        self.storage = Storage()
        self.isAppRunning = True

        self.applyUserSettings()
        self.buildGUI()
        self.connectGUIButtons()
        return None

    def buildGUI(self) -> None:
        """
        Starts the GUI
        """
        self.ui_components = (
            Ui_MainWindow()
        )  # this imports the GUI created in the qt-designer
        self.ui_components.setupUi(self)  # this initializes the UI components
        self.setWindowTitle(self.appname)

        self.camera_window = QMainWindow()
        self.camera_window.setWindowTitle("Camera Feed")

        # Create a container widget to hold the CameraWidget
        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)

        self.camera_widget = CameraWidget()

        # Add the CameraWidget to the container
        container_layout.addWidget(self.camera_widget)

        # Set the container widget as the central widget of self.camera_window
        self.camera_window.setCentralWidget(container_widget)

        self.show()

        return None

    def connectGUIButtons(self) -> None:
        """
        Hook up the callbacks to the buttons click events
        """
        self.ui_components.toggle_camera_feed.clicked.connect(self.handleToggleLiveFeed)

        return None

    def handleQuit(self) -> None:
        """
        Quits the app
        It should close and quit all proceses
        TODO
        """

        return None

    def setShowLiveFeed(self, show) -> None:
        """
        Sets the live feed on or off
        """
        self.showLiveFeed = show

        return None

    def applyUserSettings(self) -> None:
        """
        Retrieves the user settings
        """

        self.Log.warn("Applying user settings...")

        self.setShowLiveFeed(
            True if self.storage.getSetting("camera", "livefeed") == "True" else False
        )

        return None

    def handleToggleLiveFeed(self) -> None:
        """
        Toggles on/off the livefeed
        """
        self.Log.warn(f"Toggling livefeed: {self.showLiveFeed}")
        self.showLiveFeed = not self.showLiveFeed
        if not self.camera_window:
            return
        if self.showLiveFeed:
            self.camera_window.show()
        else:
            self.camera_window.hide()
        return None

    def __del__(self) -> None:
        """
        Clean up method
        TODO
        """
        return None
