"""
The start of something epic...
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.App import App

if __name__ == "__main__":
    # execute only if run as the entry point into the program
    app = QApplication(sys.argv)
    main_window = App()
    sys.exit(app.exec())
