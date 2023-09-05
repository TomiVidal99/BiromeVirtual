from enum import Enum
import os
import shutil
import configparser
from typing import Literal

from src.utils.getDefaultSettingsPath import getDefaultSettingsPath
from src.utils.Log import Log

SECTIONS = Literal["camera", "threshold_colors"]
KEYS = Literal["livefeed", "low_a", "high_a", "low_b", "high_b"]


class Storage:
    """
    Storage handles the data.
    It handles writing and reading the user settings
    """

    def __init__(self) -> None:
        self.Log = Log()
        self.DEFAULT_SETTINGS_FILEPATH = "./src/storage/defaultSettings.ini"
        self.SETTINGS_FILENAME = "settings.ini"
        self.SETTINGS_PATH = getDefaultSettingsPath()
        self.SETTINGS_FILEPATH = os.path.join(
            self.SETTINGS_PATH, self.SETTINGS_FILENAME
        )
        self.config = configparser.ConfigParser()
        self.settings = None

        self.Log.info(f"setting path: {self.SETTINGS_FILEPATH}")

        self.loadSettings()
        return None

    def loadSettings(self) -> None:
        """
        Loads the stored user settings
        """
        if not os.path.exists(self.SETTINGS_FILEPATH):
            # copy the settings.init in first init
            os.makedirs(self.SETTINGS_PATH, exist_ok=True)
            shutil.copy(self.DEFAULT_SETTINGS_FILEPATH, self.SETTINGS_FILEPATH)
            self.loadSettings()

        self.settings = self.config.read(self.SETTINGS_FILEPATH)
        self.Log.info("loaded settings successfully")

        return None

    def setSetting(self, section: SECTIONS, key: KEYS, value: str) -> None:
        """
        Sets an user setting
        """

        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, key, value)

        return None

    def getSetting(self, section: SECTIONS, key: KEYS) -> str | None:
        """
        Returns an user setting
        Returns None if the setting was not found
        """

        if not self.config.has_section(section):
            return ""

        if not self.config.has_option(section, key):
            return ""

        return self.config.get(section, key)

    def saveUserSettings(self) -> None:
        """
        Saves the current config to the user settings file
        """
        with open(self.SETTINGS_FILEPATH, "w") as configfile:
            self.config.write(configfile)
        return None
