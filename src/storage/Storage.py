from typing import Union


class Storage:
    """
    Storage handles the data.
    It handles writing and reading the user settings
    """

    def __init__(self) -> None:
        self.loadSettings()
        return None

    def loadDefaultSettings(self) -> None:
        """
        Loads the default settings
        TODO
        """

        return None

    def loadSettings(self) -> None:
        """
        Loads the stored user settings
        TODO
        """

        return None

    def setSetting(self, data: Union[str, str]) -> bool:
        """
        Sets an user setting
        Returns True if the saving was successful
        TODO
        """

        return False

    def getSetting(self, key: str) -> str | None:
        """
        Returns an user setting
        Returns None if the setting was not found
        TODO
        """

        return None
