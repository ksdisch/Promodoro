# main_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from stopwatch import Stopwatch
from pomodoro_timer import PomodoroTimer
from session_history import SessionHistory
import models  # Ensure models are loaded and tables are created

# Explanation:

# Imports the Stopwatch and PomodoroTimer classes.
# Initializes them and adds them to a tabbed interface.
# Sets the main layout and window properties.

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Productivity App")
        self.resize(600, 800)

        # Create tabs for Stopwatch, Pomodoro Timer, and Session History
        self.tabs = QTabWidget()
        self.stopwatch_tab = Stopwatch()
        self.pomodoro_tab = PomodoroTimer()
        self.history_tab = SessionHistory()
        self.tabs.addTab(self.stopwatch_tab, "Stopwatch")
        self.tabs.addTab(self.pomodoro_tab, "Pomodoro Timer")
        self.tabs.addTab(self.history_tab, "Session History")

        # Set the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
