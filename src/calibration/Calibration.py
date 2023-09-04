class Calibration:
    """
    It triggers all the calibration proceses for the camera,
    in which the parameters of the camera are estimated.
    """

    def __init__(self) -> None:
        self.startCalibration()

    def startCalibration(self) -> bool:
        """
        Initializes the calibration process
        Returns true if the calibration was sucessful, false otherwise
        """

        return False

    def getCameraParameters(self) -> bool:
        """
        Gets the camera parameters
        Returns True if it was sucessful
        """

        return False
