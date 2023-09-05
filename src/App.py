import cv2 as cv

from src.storage.Storage import Storage
from src.utils.Log import Log


class App:
    """
    App englobes all the other scripts/classes
    and it's like the entry point
    """

    def __init__(self) -> None:
        super().__init__()
        self.appname = "BiromeVirtual"
        self.Log = Log()
        self.storage = Storage()
        # self.gui = QApplication
        self.isAppRunning = True
        self.cap = None
        self.frame = None
        self.QUITTING_KEY = "q"
        self.cap = cv.VideoCapture(0)
        self.showLiveFeed = True

        self.applyUserSettings()
        self.buildGUI()
        self.connectGUIButtons()
        self.startMainLoop()
        return None

    def startMainLoop(self) -> None:
        """
        This is the main loop
        """
        while self.isAppRunning:
            if not self.startLiveFeed():
                self.Log.error("Some error ocurred with the camera")

            self.handleQuit()

        return None

    def buildGUI(self) -> None:
        """
        Starts the GUI
        """
        # self.ui_components = (
        #     Ui_MainWindow()
        # )  # this imports the GUI created in the qt-designer
        # self.ui_components.setupUi(self)  # this initializes the UI components
        # self.setWindowTitle(self.appname)
        # self.show()

        return None

    def connectGUIButtons(self) -> None:
        """
        Hook up the callbacks to the buttons click events
        """
        # self.ui_components.toggle_camera_feed.clicked.connect(
        #     lambda: self.setShowLiveFeed(not self.showLiveFeed)
        # )

        return None

    def startLiveFeed(self) -> bool:
        """
        Gets the camera up and running
        Updates the frame value
        And shows the livefeed if set to active
        """
        if not self.cap or not self.cap.isOpened():
            # TODO: handle this in some other way
            self.Log.error("Cannot open camera")
            return False

        ret, self.frame = self.cap.read()

        # if frame is read correctly ret is True
        if not ret:
            self.Log.error("Can't receive frame (stream end?). Exiting ...")
            return False

        if self.showLiveFeed:
            cv.imshow("frame", self.frame)

        return True

    def handleQuit(self) -> None:
        """
        Quits the app
        It should close and quit all proceses
        TODO
        """

        # TODO: change this behaviour to just toggle the camera feed
        if cv.waitKey(1) == ord(self.QUITTING_KEY):
            self.isAppRunning = False

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

    def __del__(self):
        """
        Clean up method
        """
        if self.cap:
            self.cap.release()
        self.cap = None
        cv.destroyAllWindows()
