# stopwatch.py

import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt

# Explanation:
#     Defines the Stopwatch class, which inherits from QWidget.
#     Implements all the required functionalities for the Stopwatch, including starting, pausing, resetting, setting custom time, and recording laps.
#     Make sure to include all the method implementations as provided in the previous code.

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the stopwatch time and lap times
        self.elapsed_time = 0  # in seconds
        self.running = False
        self.lap_times = []

        # Create UI components
        self.create_ui()

        # Setup a timer to update the display every second
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)

    def create_ui(self):
        """Creates the UI components for the stopwatch."""
        layout = QVBoxLayout()

        # Display for elapsed time
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.time_label)

        # Buttons for Start, Pause, Reset
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_stopwatch)
        button_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_stopwatch)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_stopwatch)
        self.reset_button.setEnabled(False)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        # Input for custom start time
        custom_time_layout = QHBoxLayout()
        self.custom_time_input = QLineEdit()
        self.custom_time_input.setPlaceholderText("HH:MM:SS")
        custom_time_layout.addWidget(self.custom_time_input)

        self.set_time_button = QPushButton("Set Start Time")
        self.set_time_button.clicked.connect(self.set_custom_time)
        custom_time_layout.addWidget(self.set_time_button)

        layout.addLayout(custom_time_layout)

        # Lap recording
        self.lap_button = QPushButton("Lap")
        self.lap_button.clicked.connect(self.record_lap)
        self.lap_button.setEnabled(False)
        layout.addWidget(self.lap_button)

        self.lap_list = QListWidget()
        layout.addWidget(self.lap_list)

        self.setLayout(layout)

    def start_stopwatch(self):
        """Starts the stopwatch."""
        self.running = True
        self.start_time = time.time() - self.elapsed_time
        self.update_timer.start(1000)
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.lap_button.setEnabled(True)

    def pause_stopwatch(self):
        """Pauses the stopwatch."""
        self.running = False
        self.update_timer.stop()
        self.elapsed_time = time.time() - self.start_time
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def reset_stopwatch(self):
        """Resets the stopwatch."""
        self.running = False
        self.update_timer.stop()
        self.elapsed_time = 0
        self.lap_times.clear()
        self.update_display()
        self.lap_list.clear()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.lap_button.setEnabled(False)

    def update_display(self):
        """Updates the time display."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time

        # Convert elapsed time to hours, minutes, and seconds
        total_seconds = int(self.elapsed_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Update the label
        self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def set_custom_time(self):
        """Sets a custom start time for the stopwatch."""
        time_str = self.custom_time_input.text()
        try:
            h, m, s = map(int, time_str.split(":"))
            self.elapsed_time = h * 3600 + m * 60 + s
            self.update_display()
            QMessageBox.information(self, "Success", "Start time set successfully.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter time in HH:MM:SS format.")

    def record_lap(self):
        """Records a lap time."""
        lap_time = self.elapsed_time
        lap_number = len(self.lap_times) + 1

        # Calculate individual lap time
        if self.lap_times:
            individual_lap = lap_time - self.lap_times[-1][0]
        else:
            individual_lap = lap_time

        # Store lap time
        self.lap_times.append((lap_time, individual_lap))

        # Display lap times
        total_seconds = int(lap_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        individual_seconds = int(individual_lap)
        i_hours = individual_seconds // 3600
        i_minutes = (individual_seconds % 3600) // 60
        i_seconds = individual_seconds % 60

        lap_text = (f"Lap {lap_number}: "
                    f"{i_hours:02d}:{i_minutes:02d}:{i_seconds:02d} "
                    f"(Total: {hours:02d}:{minutes:02d}:{seconds:02d})")
        self.lap_list.addItem(lap_text)
