# settings_tab.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QListWidget, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from models import Session, Settings, Category, engine
from sqlalchemy.orm import sessionmaker

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Database session
        self.Session = sessionmaker(bind=engine)
        self.db_session = self.Session()

        # Default settings
        self.settings = self.load_settings()

        # Categories
        self.categories = self.load_categories()

        # Create UI components
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(title_label)

        # Default Values Configuration
        defaults_layout = QVBoxLayout()
        defaults_title = QLabel("Default Values Configuration")
        defaults_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        defaults_layout.addWidget(defaults_title)

        # Session Duration
        session_duration_layout = QHBoxLayout()
        self.session_duration_spin = QSpinBox()
        self.session_duration_spin.setRange(1, 120)
        self.session_duration_spin.setValue(self.settings.session_duration)
        session_duration_layout.addWidget(QLabel("Session Duration (min):"))
        session_duration_layout.addWidget(self.session_duration_spin)
        defaults_layout.addLayout(session_duration_layout)

        # Sessions per Full Pomodoro Cycle
        sessions_per_cycle_layout = QHBoxLayout()
        self.sessions_per_cycle_spin = QSpinBox()
        self.sessions_per_cycle_spin.setRange(1, 10)
        self.sessions_per_cycle_spin.setValue(self.settings.sessions_per_cycle)
        sessions_per_cycle_layout.addWidget(QLabel("Sessions per Full Pomodoro Cycle:"))
        sessions_per_cycle_layout.addWidget(self.sessions_per_cycle_spin)
        defaults_layout.addLayout(sessions_per_cycle_layout)

        # Short Break Duration
        short_break_duration_layout = QHBoxLayout()
        self.short_break_duration_spin = QSpinBox()
        self.short_break_duration_spin.setRange(1, 60)
        self.short_break_duration_spin.setValue(self.settings.short_break_duration)
        short_break_duration_layout.addWidget(QLabel("Short Break Duration (min):"))
        short_break_duration_layout.addWidget(self.short_break_duration_spin)
        defaults_layout.addLayout(short_break_duration_layout)

        # Long Break Duration
        long_break_duration_layout = QHBoxLayout()
        self.long_break_duration_spin = QSpinBox()
        self.long_break_duration_spin.setRange(1, 120)
        self.long_break_duration_spin.setValue(self.settings.long_break_duration)
        long_break_duration_layout.addWidget(QLabel("Long Break Duration (min):"))
        long_break_duration_layout.addWidget(self.long_break_duration_spin)
        defaults_layout.addLayout(long_break_duration_layout)

        # Save Defaults Button
        save_defaults_button = QPushButton("Save Default Settings")
        save_defaults_button.clicked.connect(self.save_default_settings)
        defaults_layout.addWidget(save_defaults_button)

        layout.addLayout(defaults_layout)

        # Spacer
        layout.addSpacing(20)

        # Manage Session Categories
        categories_layout = QVBoxLayout()
        categories_title = QLabel("Manage Session Categories")
        categories_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        categories_layout.addWidget(categories_title)

        # Category List
        self.category_list = QListWidget()
        self.category_list.addItems(self.categories)
        categories_layout.addWidget(self.category_list)

        # Add and Remove Category
        category_buttons_layout = QHBoxLayout()
        self.new_category_input = QLineEdit()
        self.new_category_input.setPlaceholderText("New Category")
        category_buttons_layout.addWidget(self.new_category_input)

        add_category_button = QPushButton("Add Category")
        add_category_button.clicked.connect(self.add_category)
        category_buttons_layout.addWidget(add_category_button)

        remove_category_button = QPushButton("Remove Selected Category")
        remove_category_button.clicked.connect(self.remove_category)
        category_buttons_layout.addWidget(remove_category_button)

        categories_layout.addLayout(category_buttons_layout)

        layout.addLayout(categories_layout)

        self.setLayout(layout)

    def load_settings(self):
        """Load settings from the database or create defaults."""
        settings = self.db_session.query(Settings).first()
        if not settings:
            # Create default settings
            settings = Settings(
                session_duration=25,
                sessions_per_cycle=4,
                short_break_duration=5,
                long_break_duration=30
            )
            self.db_session.add(settings)
            self.db_session.commit()
        return settings

    def save_default_settings(self):
        """Save the default settings to the database."""
        self.settings.session_duration = self.session_duration_spin.value()
        self.settings.sessions_per_cycle = self.sessions_per_cycle_spin.value()
        self.settings.short_break_duration = self.short_break_duration_spin.value()
        self.settings.long_break_duration = self.long_break_duration_spin.value()
        self.db_session.commit()
        QMessageBox.information(self, "Success", "Default settings saved successfully.")

    def load_categories(self):
        """Load categories from the database."""
        categories = self.db_session.query(Category).all()
        if not categories:
            # Add default categories
            default_categories = ["Work", "Chores", "Reading", "Exercise"]
            for cat in default_categories:
                new_category = Category(name=cat)
                self.db_session.add(new_category)
            self.db_session.commit()
            categories = self.db_session.query(Category).all()
        return [category.name for category in categories]

    def add_category(self):
        """Add a new category."""
        category_name = self.new_category_input.text().strip()
        if category_name:
            if category_name not in self.categories:
                new_category = Category(name=category_name)
                self.db_session.add(new_category)
                self.db_session.commit()
                self.categories.append(category_name)
                self.category_list.addItem(category_name)
                self.new_category_input.clear()
                QMessageBox.information(self, "Success", f"Category '{category_name}' added.")
            else:
                QMessageBox.warning(self, "Error", "Category already exists.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a category name.")

    def remove_category(self):
        """Remove the selected category."""
        selected_items = self.category_list.selectedItems()
        if selected_items:
            for item in selected_items:
                category_name = item.text()
                if category_name in ["Work", "Chores", "Reading", "Exercise"]:
                    QMessageBox.warning(self, "Error", f"Cannot remove default category '{category_name}'.")
                    continue
                category = self.db_session.query(Category).filter_by(name=category_name).first()
                if category:
                    self.db_session.delete(category)
                    self.db_session.commit()
                    self.categories.remove(category_name)
                    self.category_list.takeItem(self.category_list.row(item))
                    QMessageBox.information(self, "Success", f"Category '{category_name}' removed.")
        else:
            QMessageBox.warning(self, "Error", "Please select a category to remove.")

    def closeEvent(self, event):
        """Handle the widget close event to clean up resources."""
        self.db_session.close()
        super().closeEvent(event)