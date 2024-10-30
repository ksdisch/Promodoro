# pomodoro_timer.py

# Important:
    # Database Integration: Make sure to include the database session creation and use models.py for database interactions.
    # Categories Persistence: Categories are loaded from and saved to a file (data/categories.txt). Ensure that the data directory exists.
    # Method Implementations: Include all method implementations as provided in the previous code.

# Explanation:
    # Defines the PomodoroTimer class, inheriting from QWidget.
    # Implements functionalities for starting, pausing, resetting the timer, adding categories, setting durations, and interacting with the database for persistent storage.
    # Includes methods for loading and saving categories, and handling calendar interactions.

# pomodoro_timer.py

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSpinBox, QLineEdit, QComboBox, QCalendarWidget, QTextEdit,
    QMessageBox, QDateTimeEdit, QListWidget
)
from PyQt5.QtCore import QTimer, Qt, QDateTime, pyqtSignal
from models import Session, ScheduledSession
from datetime import datetime

class PomodoroTimer(QWidget):
    # Signal to indicate that a session has been completed
    session_completed = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Pomodoro settings
        self.work_duration = 25 * 60  # default 25 minutes
        self.break_duration = 5 * 60  # default 5 minutes
        self.remaining_time = self.work_duration
        self.is_work_session = True
        self.running = False

        # Task categories
        self.categories = []
        self.load_categories()

        # Database session
        self.db_session = Session()

        # Variables to track session times
        self.session_start_time = None
        self.session_end_time = None

        # Variable to store the selected planned session
        self.current_session = None

        # Create UI components
        self.create_ui()

        # Timer to update the display every second
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)

    def create_ui(self):
        """Creates the UI components for the Pomodoro Timer."""
        layout = QVBoxLayout()

        # Display for remaining time
        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.time_label)

        # Buttons for Start, Pause, Reset
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setEnabled(False)
        button_layout.addWidget(self.reset_button)

        self.add_time_button = QPushButton("+3 Minutes")
        self.add_time_button.clicked.connect(self.add_three_minutes)
        button_layout.addWidget(self.add_time_button)

        layout.addLayout(button_layout)

        # Inputs for work and break durations
        duration_layout = QHBoxLayout()
        self.work_duration_spin = QSpinBox()
        self.work_duration_spin.setRange(1, 120)
        self.work_duration_spin.setValue(25)
        duration_layout.addWidget(QLabel("Work Duration (min):"))
        duration_layout.addWidget(self.work_duration_spin)

        self.break_duration_spin = QSpinBox()
        self.break_duration_spin.setRange(1, 60)
        self.break_duration_spin.setValue(5)
        duration_layout.addWidget(QLabel("Break Duration (min):"))
        duration_layout.addWidget(self.break_duration_spin)

        self.set_duration_button = QPushButton("Set Durations")
        self.set_duration_button.clicked.connect(self.set_durations)
        duration_layout.addWidget(self.set_duration_button)

        layout.addLayout(duration_layout)

        # Inputs for planned start and end times
        time_layout = QHBoxLayout()
        self.planned_start_time_edit = QDateTimeEdit()
        self.planned_start_time_edit.setCalendarPopup(True)
        self.planned_start_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.planned_start_time_edit.setDateTime(QDateTime.currentDateTime())
        time_layout.addWidget(QLabel("Planned Start Time:"))
        time_layout.addWidget(self.planned_start_time_edit)

        self.planned_end_time_edit = QDateTimeEdit()
        self.planned_end_time_edit.setCalendarPopup(True)
        self.planned_end_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.planned_end_time_edit.setDateTime(QDateTime.currentDateTime().addSecs(25 * 60))
        time_layout.addWidget(QLabel("Planned End Time:"))
        time_layout.addWidget(self.planned_end_time_edit)

        layout.addLayout(time_layout)

        # Category selection and addition
        category_layout = QHBoxLayout()
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        category_layout.addWidget(QLabel("Category:"))
        category_layout.addWidget(self.category_combo)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("New Category")
        category_layout.addWidget(self.category_input)

        self.add_category_button = QPushButton("Add Category")
        self.add_category_button.clicked.connect(self.add_category)
        category_layout.addWidget(self.add_category_button)

        layout.addLayout(category_layout)

        # Calendar widget for scheduling
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.date_selected)
        layout.addWidget(self.calendar)

        # Sessions list
        self.sessions_list = QListWidget()
        self.sessions_list.itemClicked.connect(self.session_selected)
        layout.addWidget(self.sessions_list)

        # Button to start selected planned session
        self.start_planned_button = QPushButton("Start Selected Session")
        self.start_planned_button.clicked.connect(self.start_planned_session)
        self.start_planned_button.setEnabled(False)
        layout.addWidget(self.start_planned_button)

        # Notes area
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Enter notes or tasks for this date.")
        layout.addWidget(self.notes_edit)

        # Buttons for saving and deleting scheduled sessions
        schedule_button_layout = QHBoxLayout()
        self.save_schedule_button = QPushButton("Save Session")
        self.save_schedule_button.clicked.connect(self.save_session)
        schedule_button_layout.addWidget(self.save_schedule_button)

        self.delete_schedule_button = QPushButton("Delete Session")
        self.delete_schedule_button.clicked.connect(self.delete_session)
        schedule_button_layout.addWidget(self.delete_schedule_button)

        layout.addLayout(schedule_button_layout)

        self.setLayout(layout)

    def start_timer(self):
        """Starts the Pomodoro timer."""
        self.running = True
        self.update_timer.start(1000)
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.reset_button.setEnabled(True)

        # Record the session start time if starting a new session
        if self.session_start_time is None:
            self.session_start_time = datetime.now()

    def pause_timer(self):
        """Pauses the Pomodoro timer."""
        self.running = False
        self.update_timer.stop()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def reset_timer(self):
        """Resets the Pomodoro timer."""
        self.running = False
        self.update_timer.stop()
        self.remaining_time = self.work_duration if self.is_work_session else self.break_duration
        self.update_display()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.reset_button.setEnabled(False)

        # Reset session times
        self.session_start_time = None
        self.session_end_time = None

    def add_three_minutes(self):
        """Adds three minutes to the current session."""
        self.remaining_time += 3 * 60
        self.update_display()

    def set_durations(self):
        """Sets the work and break durations."""
        self.work_duration = self.work_duration_spin.value() * 60
        self.break_duration = self.break_duration_spin.value() * 60
        self.set_initial_time()
        self.update_display()
        QMessageBox.information(self, "Success", "Durations updated successfully.")

    def set_initial_time(self):
        """Sets the initial remaining time based on the session type."""
        if self.is_work_session:
            self.remaining_time = self.work_duration
        else:
            self.remaining_time = self.break_duration

    def update_display(self):
        """Updates the time display."""
        if self.running:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                # Save the session upon completion
                if self.current_session and self.current_session.status == 'in progress':
                    self.current_session.actual_end_time = datetime.now()
                    self.current_session.status = 'completed'
                    self.db_session.commit()
                    # Emit the session_completed signal
                    self.session_completed.emit()
                    QMessageBox.information(self, "Session Completed", "Planned session completed.")
                    self.current_session = None
                else:
                    self.save_completed_session()

                # Switch between work and break sessions
                self.is_work_session = not self.is_work_session
                self.set_initial_time()
                self.update_display()  # Update display immediately
                if self.is_work_session:
                    QMessageBox.information(self, "Pomodoro", "Work session started.")
                else:
                    QMessageBox.information(self, "Pomodoro", "Break time!")

        # Update the label
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def save_completed_session(self):
        """Automatically saves the completed Pomodoro session to the database."""
        if self.session_start_time:
            self.session_end_time = datetime.now()

            # Get category and notes (if any)
            category = self.category_combo.currentText() or "Uncategorized"
            notes = self.notes_edit.toPlainText()

            # Create a new ScheduledSession instance
            new_session = ScheduledSession(
                date=self.session_start_time.date(),
                actual_start_time=self.session_start_time,
                actual_end_time=self.session_end_time,
                category=category,
                notes=notes,
                status='completed'
            )

            # Save to the database
            self.db_session.add(new_session)
            self.db_session.commit()

            # Emit the session_completed signal
            self.session_completed.emit()

            QMessageBox.information(
                self,
                "Session Saved",
                f"Pomodoro session from {self.session_start_time.strftime('%H:%M:%S')} "
                f"to {self.session_end_time.strftime('%H:%M:%S')} saved."
            )

            # Reset session times
            self.session_start_time = None
            self.session_end_time = None

    def add_category(self):
        """Adds a new category to the list."""
        category = self.category_input.text()
        if category and category not in self.categories:
            self.categories.append(category)
            self.category_combo.addItem(category)
            self.category_input.clear()
            self.save_categories()
            QMessageBox.information(self, "Success", f"Category '{category}' added.")
        else:
            QMessageBox.warning(self, "Error", "Invalid or duplicate category.")

    def save_categories(self):
        """Saves categories to a file."""
        # For simplicity, we save categories to a text file.
        with open('data/categories.txt', 'w') as f:
            for category in self.categories:
                f.write(f"{category}\n")

    def load_categories(self):
        """Loads categories from a file."""
        try:
            with open('data/categories.txt', 'r') as f:
                self.categories = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.categories = []

    def date_selected(self):
        """Handles date selection in the calendar."""
        date = self.calendar.selectedDate()
        date_obj = date.toPyDate()
        sessions = self.db_session.query(ScheduledSession).filter_by(date=date_obj).all()
        
        self.sessions_list.clear()
        if sessions:
            for session in sessions:
                if session.status == 'planned':
                    display_text = (f"Planned: {session.category} at "
                                    f"{session.planned_start_time.strftime('%H:%M')}")
                elif session.status == 'completed':
                    display_text = (f"Completed: {session.category} at "
                                    f"{session.actual_start_time.strftime('%H:%M')}")
                else:
                    continue
                self.sessions_list.addItem(display_text)
        else:
            self.sessions_list.clear()

    def session_selected(self, item):
        """Handles selection of a session from the list."""
        self.selected_session_text = item.text()
        if 'Planned' in item.text():
            self.start_planned_button.setEnabled(True)
        else:
            self.start_planned_button.setEnabled(False)

    def start_planned_session(self):
        """Starts the selected planned session."""
        date_obj = self.calendar.selectedDate().toPyDate()
        sessions = self.db_session.query(ScheduledSession).filter_by(date=date_obj).all()

        # Find the selected planned session
        for session in sessions:
            if session.status == 'planned' and session.category in self.selected_session_text:
                self.current_session = session
                break

        if self.current_session:
            # Update status and actual start time
            self.current_session.status = 'in progress'
            self.current_session.actual_start_time = datetime.now()
            self.db_session.commit()

            # Calculate planned duration
            planned_duration = (self.current_session.planned_end_time - self.current_session.planned_start_time).total_seconds()
            self.work_duration = int(planned_duration)
            self.set_initial_time()
            self.start_timer()
        else:
            QMessageBox.warning(self, "Error", "Could not find the selected session.")

    def save_session(self):
        """Saves the scheduled session to the database."""
        date = self.planned_start_time_edit.date().toPyDate()
        planned_start = self.planned_start_time_edit.dateTime().toPyDateTime()
        planned_end = self.planned_end_time_edit.dateTime().toPyDateTime()
        notes = self.notes_edit.toPlainText()
        category = self.category_combo.currentText()

        if not category:
            QMessageBox.warning(self, "Error", "Please select a category.")
            return

        new_session = ScheduledSession(
            date=date,
            planned_start_time=planned_start,
            planned_end_time=planned_end,
            category=category,
            notes=notes,
            status='planned'
        )
        self.db_session.add(new_session)
        self.db_session.commit()
        QMessageBox.information(self, "Success", "Session saved successfully.")

        # Refresh the sessions list
        self.date_selected(self.calendar.selectedDate())

    def delete_session(self):
        """Deletes the selected scheduled session from the database."""
        if self.selected_session_text:
            date_obj = self.calendar.selectedDate().toPyDate()
            sessions = self.db_session.query(ScheduledSession).filter_by(date=date_obj).all()

            # Find the selected session
            for session in sessions:
                session_text = ''
                if session.status == 'planned':
                    session_text = f"Planned: {session.category} at {session.planned_start_time.strftime('%H:%M')}"
                elif session.status == 'completed':
                    session_text = f"Completed: {session.category} at {session.actual_start_time.strftime('%H:%M')}"
                if session_text == self.selected_session_text:
                    self.current_session = session
                    break

            if self.current_session:
                confirm = QMessageBox.question(
                    self,
                    "Confirm Deletion",
                    "Are you sure you want to delete the selected session?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if confirm == QMessageBox.Yes:
                    self.db_session.delete(self.current_session)
                    self.db_session.commit()
                    QMessageBox.information(self, "Session Deleted", "The session has been deleted.")
                    self.current_session = None
                    self.selected_session_text = ''
                    self.start_planned_button.setEnabled(False)
                    # Refresh the sessions list
                    self.date_selected(self.calendar.selectedDate())
            else:
                QMessageBox.warning(self, "Error", "Could not find the selected session.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a session to delete.")

    def closeEvent(self, event):
        """Handle the widget close event to clean up resources."""
        self.db_session.close()
        super().closeEvent(event)
