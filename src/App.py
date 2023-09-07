from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QColorDialog, QFrame, QMainWindow, QVBoxLayout, QWidget
from src.camera.CameraWidget import CameraWidget
from src.GUI.app_ui import Ui_MainWindow

from src.storage.Storage import KEYS, SECTIONS, Storage
from src.utils.Log import Log


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

        self.buildGUI()
        self.applyUserSettings()
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

        self.camera_widget = CameraWidget(self.storage)

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
        self.ui_components.button_color_a_lower.clicked.connect(
            lambda: self.handlePickColor(
                self.ui_components.display_color_a_lower, "threshold_colors", "low_a"
            )
        )
        self.ui_components.button_color_a_higher.clicked.connect(
            lambda: self.handlePickColor(
                self.ui_components.display_color_a_higher, "threshold_colors", "high_a"
            )
        )
        self.ui_components.button_color_b_lower.clicked.connect(
            lambda: self.handlePickColor(
                self.ui_components.display_color_b_lower, "threshold_colors", "low_b"
            )
        )
        self.ui_components.button_color_b_higher.clicked.connect(
            lambda: self.handlePickColor(
                self.ui_components.display_color_b_higher, "threshold_colors", "high_b"
            )
        )

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

        # Colors
        self.setComponentBgColor(
            self.ui_components.display_color_a_lower,
            self.getColorFromString(
                self.storage.getSetting("threshold_colors", "low_a")
            ),
        )
        self.setComponentBgColor(
            self.ui_components.display_color_a_higher,
            self.getColorFromString(
                self.storage.getSetting("threshold_colors", "high_a")
            ),
        )
        self.setComponentBgColor(
            self.ui_components.display_color_b_lower,
            self.getColorFromString(
                self.storage.getSetting("threshold_colors", "low_b")
            ),
        )
        self.setComponentBgColor(
            self.ui_components.display_color_b_higher,
            self.getColorFromString(
                self.storage.getSetting("threshold_colors", "high_b")
            ),
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

    def handlePickColor(self, component: QFrame, section: SECTIONS, key: KEYS) -> None:
        color = QColorDialog().getColor()
        if color.isValid():
            colorStr = color.name()
            self.storage.setSetting(section, key, colorStr)
            self.Log.info(f"You've picked: {colorStr}, {section}, {key}")
            self.setComponentBgColor(component, color)

    def setComponentBgColor(self, component: QFrame, color: QColor) -> None:
        """
        Sets the background color of a component
        """
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, color)
        component.setAutoFillBackground(True)
        component.setPalette(palette)
        return None

    def getColorFromString(self, string: str | None) -> QColor:
        """
        Returns a QColor from a given string like '#000'
        """
        color = QColor()
        if string is None:
            return color
        color.setNamedColor(string)
        return color

    def closeEvent(self, event) -> None:
        """
        Clean up method
        TODO
        """
        self.Log.warn("Saving data before quitting")
        self.storage.saveUserSettings()
        return None
