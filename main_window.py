# main_window.py

# Explanation:

# Imports the Stopwatch and NewPomo classes.
# Initializes them and adds them to a tabbed interface.
# Sets the main layout and window properties.

# main_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from stopwatch import Stopwatch
from new_pomo_tab import NewPomo  # Assuming you have renamed pomodoro_timer.py
from session_history import SessionHistory
from settings_tab import SettingsTab  # Import the SettingsTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Productivity App")
        self.resize(800, 600)

        # Create tabs
        self.tabs = QTabWidget()

        # Stopwatch Tab
        self.stopwatch_tab = Stopwatch()
        self.tabs.addTab(self.stopwatch_tab, "Stopwatch")

        # New Pomo Tab
        self.new_pomo_tab = NewPomo()
        self.tabs.addTab(self.new_pomo_tab, "New Pomo")

        # Session History Tab
        self.history_tab = SessionHistory()
        self.tabs.addTab(self.history_tab, "Session History")

        # Settings Tab
        self.settings_tab = SettingsTab()
        self.tabs.addTab(self.settings_tab, "Settings")

        # Set the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)