# session_history.py

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QLabel, QPushButton, QMessageBox, QHBoxLayout, QHeaderView  # Added QHeaderView
)
from PyQt5.QtCore import Qt
from models import Session, ScheduledSession
from datetime import datetime

class SessionHistory(QWidget):
    def __init__(self):
        super().__init__()

        # Create a database session
        self.db_session = Session()

        # Create UI components
        self.create_ui()

    def create_ui(self):
        """Creates the UI components for the Session History tab."""
        layout = QVBoxLayout()

        # Label for the title
        title_label = QLabel("Session History")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(title_label)

        # Table to display sessions
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'Date', 'Planned Start', 'Planned End',
            'Actual Start', 'Actual End', 'Category',
            'Status', 'Notes'
        ])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Corrected line

        layout.addWidget(self.table)

        # Delete Button
        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete Selected Session")
        self.delete_button.clicked.connect(self.delete_session)
        button_layout.addStretch()
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load sessions into the table
        self.load_sessions()

    def load_sessions(self):
        """Loads all sessions from the database into the table."""
        sessions = self.db_session.query(ScheduledSession).order_by(
            ScheduledSession.date.desc(),
            ScheduledSession.planned_start_time.desc()
        ).all()

        self.table.setRowCount(len(sessions))
        self.sessions = sessions  # Store sessions for easy access

        for row, session in enumerate(sessions):
            date_item = QTableWidgetItem(session.date.strftime('%Y-%m-%d'))
            planned_start_item = QTableWidgetItem(
                session.planned_start_time.strftime('%Y-%m-%d %H:%M') if session.planned_start_time else ''
            )
            planned_end_item = QTableWidgetItem(
                session.planned_end_time.strftime('%Y-%m-%d %H:%M') if session.planned_end_time else ''
            )
            actual_start_item = QTableWidgetItem(
                session.actual_start_time.strftime('%Y-%m-%d %H:%M') if session.actual_start_time else ''
            )
            actual_end_item = QTableWidgetItem(
                session.actual_end_time.strftime('%Y-%m-%d %H:%M') if session.actual_end_time else ''
            )
            category_item = QTableWidgetItem(session.category)
            status_item = QTableWidgetItem(session.status)
            notes_item = QTableWidgetItem(session.notes or '')

            # Set text alignment
            date_item.setTextAlignment(Qt.AlignCenter)
            planned_start_item.setTextAlignment(Qt.AlignCenter)
            planned_end_item.setTextAlignment(Qt.AlignCenter)
            actual_start_item.setTextAlignment(Qt.AlignCenter)
            actual_end_item.setTextAlignment(Qt.AlignCenter)
            category_item.setTextAlignment(Qt.AlignCenter)
            status_item.setTextAlignment(Qt.AlignCenter)

            # Set items in the table
            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, planned_start_item)
            self.table.setItem(row, 2, planned_end_item)
            self.table.setItem(row, 3, actual_start_item)
            self.table.setItem(row, 4, actual_end_item)
            self.table.setItem(row, 5, category_item)
            self.table.setItem(row, 6, status_item)
            self.table.setItem(row, 7, notes_item)

    def delete_session(self):
        """Deletes the selected session from the database."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a session to delete.")
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete the selected session?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            # Get the session object
            session_to_delete = self.sessions[selected_row]

            # Delete from the database
            self.db_session.delete(session_to_delete)
            self.db_session.commit()

            # Refresh the table
            self.load_sessions()

            QMessageBox.information(self, "Session Deleted", "The session has been deleted.")

    def refresh(self):
        """Refreshes the session list."""
        self.load_sessions()

    def closeEvent(self, event):
        """Handle the widget close event to clean up resources."""
        self.db_session.close()
        super().closeEvent(event)
