# main.py

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

# Explanation:
    # Imports the necessary modules.
    # Creates an instance of QApplication.
    # Initializes the MainWindow class (defined in main_window.py).
    # Starts the application's event loop.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
