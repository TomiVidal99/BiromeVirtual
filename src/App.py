import cv2 as cv


class App:
    """
    App englobes all the other scripts/classes
    and it's like the entry point
    """

    def __init__(self) -> None:
        self.isAppRunning = True
        self.cap = None
        self.frame = None
        self.QUITTING_KEY = "q"

        self.startGUI()
        self.startMainLoop()
        return None

    def startMainLoop(self) -> None:
        """
        This is the main loop
        """
        while self.isAppRunning:
            if not self.startLiveFeed():
                print("Some error ocurred with the camera")

            self.handleQuit()

        return None

    def startGUI(self) -> None:
        """
        Starts the GUI
        TODO
        """
        return None

    def startLiveFeed(self) -> bool:
        """
        Gets the camera up and running
        Updates the frame value
        """
        self.cap = cv.VideoCapture(0)
        if self.cap.isOpened():
            # TODO: handle this in some other way
            print("Cannot open camera")
            return False

        ret, self.frame = self.cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return False

        cv.imshow("frame", self.frame)

        return True

    def handleQuit(self) -> None:
        """
        Quits the app
        It should close and quit all proceses
        """

        if cv.waitKey(1) == ord(self.QUITTING_KEY):
            self.isAppRunning = False
            # TODO define a clean up method
            if self.cap:
                self.cap.release()
            cv.destroyAllWindows()
            return None

        return None
