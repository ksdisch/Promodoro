# Productivity App

**Version:** 1.1  
**Last Updated:** [Date]

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
  - [Stopwatch](#stopwatch)
  - [Pomodoro Timer](#pomodoro-timer)
  - [Calendar Scheduling](#calendar-scheduling)
  - [Session History](#session-history)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Navigating the Interface](#navigating-the-interface)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Change Log](#change-log)
- [Acknowledgments](#acknowledgments)

---

## Introduction

The **Productivity App** is a desktop application built with Python and PyQt5, designed to enhance your time management and productivity. It integrates a feature-rich **Stopwatch**, a customizable **Pomodoro Timer**, a comprehensive **Calendar Scheduling** system, and a detailed **Session History** to help you plan, track, and optimize your work sessions effectively. The application uses PostgreSQL and SQLAlchemy for persistent data storage, ensuring your sessions and schedules are saved securely.

---

## Features

### Stopwatch

- **Basic Stopwatch Functionality**:
  - Start, pause, and reset the stopwatch.
  - Display elapsed time in hours, minutes, and seconds.
- **Lap Recording**:
  - Record lap times at any moment.
  - View individual lap times and cumulative times.
- **Custom Start Time**:
  - Begin the stopwatch from a specified time if you forgot to start it earlier.

### Pomodoro Timer

- **Configurable Work and Break Durations**:
  - Set custom durations for work and break sessions.
  - Adjust durations on the fly to suit your workflow.
- **Task Categories**:
  - Create custom categories for tasks (e.g., Coding, Reading).
  - Tag each Pomodoro session with a specific category.
- **Session Notes**:
  - Add notes or tasks to each session for better planning and reflection.
- **Automatic Session Saving**:
  - Sessions are automatically saved upon completion, including start and end times, category, and notes.

### Calendar Scheduling

- **Plan Sessions with Specific Times**:
  - Schedule sessions with specific planned start and end times.
  - Use a calendar interface to select dates and times.
- **View Planned and Completed Sessions**:
  - Click on a date to view all planned and completed sessions for that day.
- **Start Planned Sessions**:
  - Start a planned session directly from the calendar interface.
  - If actual start and end times differ from planned times, the app updates them accordingly.
- **Session Management**:
  - Delete planned or completed sessions directly from the calendar interface.
  - Edit session details as needed.

### Session History

- **Detailed Session Logs**:
  - View all sessions in a comprehensive table with the following columns:
    - **Date**
    - **Planned Start Time**
    - **Planned End Time**
    - **Actual Start Time**
    - **Actual End Time**
    - **Category**
    - **Status** (`Planned`, `In Progress`, `Completed`)
    - **Notes**
- **Session Deletion**:
  - Delete any session from the history.
- **Automatic Refresh**:
  - Session history updates automatically when a new session is completed or modified.

---

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **PostgreSQL database server**
- **Python Packages**:
  - PyQt5
  - SQLAlchemy
  - psycopg2-binary
  - Alembic (for database migrations)

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/productivity_app.git
   cd productivity_app
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the PostgreSQL Database**:

   - **Create a Database**:

     ```sql
     CREATE DATABASE productivity_app;
     ```

   - **Create a Database User** (optional):

     ```sql
     CREATE USER app_user WITH PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE productivity_app TO app_user;
     ```

   - **Update Database URI**:

     In `models.py`, update the `DATABASE_URI` with your database credentials:

     ```python
     DATABASE_URI = 'postgresql+psycopg2://app_user:your_password@localhost/productivity_app'
     ```

4. **Initialize the Database with Alembic**:

   - **Initialize Alembic**:

     ```bash
     alembic init alembic
     ```

   - **Configure Alembic**:

     - In `alembic.ini`, set the `sqlalchemy.url` to your `DATABASE_URI`.
     - In `alembic/env.py`, import your `Base` from `models.py` and set `target_metadata = Base.metadata`.

   - **Generate Migration Script**:

     ```bash
     alembic revision --autogenerate -m "Initial migration"
     ```

   - **Apply Migration**:

     ```bash
     alembic upgrade head
     ```

5. **Run the Application**:

   ```bash
   python main.py
   ```

---

## Usage

### Running the Application

Start the application by running:

```bash
python main.py
```

### Navigating the Interface

- The application window has three main tabs:
  - **Stopwatch**
  - **Pomodoro Timer**
  - **Session History**

#### Stopwatch Tab

- **Start**: Begin timing by clicking the **Start** button.
- **Pause**: Pause the stopwatch with the **Pause** button.
- **Reset**: Reset the stopwatch to zero using the **Reset** button.
- **Lap**: Record lap times by clicking the **Lap** button.
- **Set Custom Time**:
  - Enter a time in `HH:MM:SS` format.
  - Click **Set Start Time** to start from that time.

#### Pomodoro Timer Tab

- **Configure Durations**:
  - Set work and break durations using the spin boxes.
  - Click **Set Durations** to apply changes.
- **Schedule Sessions**:
  - **Select Planned Start and End Times**:
    - Use the `Planned Start Time` and `Planned End Time` fields to schedule sessions with specific times.
  - **Select a Category**:
    - Choose a category from the drop-down menu or add a new one.
  - **Add Notes**:
    - Write notes or tasks for the session.
  - **Save Session**:
    - Click **Save Session** to store the scheduled session.
- **View and Manage Sessions**:
  - **Calendar Interface**:
    - Click on a date to view planned and completed sessions.
    - Sessions are listed with their status and times.
  - **Start Planned Sessions**:
    - Select a planned session and click **Start Selected Session**.
    - The timer will begin, and actual start and end times will be recorded.
  - **Delete Sessions**:
    - Select a session and click **Delete Session** to remove it.

#### Session History Tab

- **View Sessions**:
  - All sessions are displayed in a table with detailed information.
- **Delete Sessions**:
  - Select a session and click **Delete Selected Session** to remove it from the history.

---

## Directory Structure

```
productivity_app/
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── data/
│   └── categories.txt
├── main.py
├── main_window.py
├── models.py
├── pomodoro_timer.py
├── session_history.py
├── stopwatch.py
├── requirements.txt
├── README.md
└── resources/
    ├── images/
    └── styles/
```

- **`main.py`**: Entry point of the application.
- **`main_window.py`**: Integrates all components into the main window.
- **`stopwatch.py`**: Contains the `Stopwatch` class.
- **`pomodoro_timer.py`**: Contains the `PomodoroTimer` class with calendar scheduling.
- **`session_history.py`**: Contains the `SessionHistory` class.
- **`models.py`**: Defines the database models and initializes the database.
- **`alembic/`**: Directory for database migrations.
- **`data/`**: Stores category data and other persistent files.
- **`resources/`**: Directory for images and stylesheets.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**:

   - Create a personal fork of the project on GitHub.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/yourusername/productivity_app.git
   ```

3. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Commit Your Changes**:

   ```bash
   git commit -am "Add new feature"
   ```

5. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:

   - Open a pull request against the main repository.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Support

If you have any questions, issues, or suggestions, please contact:

- **Email**: support@productivityapp.com
- **GitHub Issues**: [Productivity App Issues](https://github.com/yourusername/productivity_app/issues)

---

## Frequently Asked Questions

### How do I schedule a session with specific times?

- Navigate to the **Pomodoro Timer** tab.
- Use the **Planned Start Time** and **Planned End Time** fields to set the desired times.
- Select a category and add any notes.
- Click **Save Session** to schedule it.

### Can I start a planned session immediately?

- Yes, select the planned session from the sessions list and click **Start Selected Session**.
- The timer will begin, and the actual start time will be recorded.

### What happens if the actual start and end times differ from the planned times?

- The application records the actual start and end times upon completion.
- The Session History will display both planned and actual times for your reference.

### How can I delete a session?

- **From the Calendar Interface**:
  - Select the session from the list.
  - Click **Delete Session**.
- **From the Session History Tab**:
  - Select the session in the table.
  - Click **Delete Selected Session**.

### Does the application support multiple sessions per day?

- Yes, you can schedule and complete multiple sessions on the same day.

### How do I handle database migrations?

- The application uses **Alembic** for database migrations.
- Follow the [Setup Instructions](#setup-instructions) to initialize and apply migrations.

---

## Change Log

### Version 1.1

- **New Features**:
  - Ability to schedule sessions with specific planned start and end times.
  - Calendar interface updated to display both planned and completed sessions.
  - Start planned sessions directly from the calendar interface.
  - Session History now displays both planned and actual times.
- **Improvements**:
  - Added session deletion functionality in both the calendar interface and the session history tab.
  - Enhanced error handling and user feedback.
- **Bug Fixes**:
  - Resolved issues with signal-slot mismatches in the calendar interface.
  - Fixed database schema synchronization using Alembic migrations.

### Version 1.0

- Initial release with the following features:
  - Stopwatch with lap recording and custom start time.
  - Pomodoro Timer with configurable durations and categories.
  - Basic calendar scheduling for sessions.
  - Automatic saving of completed sessions.
  - Session History tab to view all completed sessions.

---

## Acknowledgments

- **PyQt5**: For providing powerful GUI components.
- **SQLAlchemy**: For simplifying database interactions.
- **Alembic**: For managing database migrations.
- **PostgreSQL**: For reliable data storage.

---

**Thank you for using the Productivity App! We hope it helps you manage your time effectively and boost your productivity.**

Feel free to reach out if you have any questions or need assistance!

---

## Additional Notes

- **Data Persistence**:
  - The application uses PostgreSQL for data storage.
  - Ensure the database server is running when using the app.
- **Error Handling**:
  - The app includes error handling to prevent crashes.
  - Error messages are displayed via dialogs for user awareness.
- **Customization**:
  - You can customize categories and durations to fit your workflow.
  - UI elements can be styled using Qt Style Sheets (QSS) located in the `resources/styles/` directory.

---

## Troubleshooting

### Application Does Not Start

- Ensure all dependencies are installed correctly.
- Verify your database connection and credentials in `models.py` and `alembic.ini`.
- Check that the PostgreSQL server is running.

### Database Migration Issues

- Make sure Alembic is properly configured.
- Run `alembic upgrade head` to apply migrations.
- Check for any migration conflicts or errors.

### UI Elements Not Responding

- Restart the application.
- Check the console for error messages.
- Ensure all code files are saved and updated.

### Sessions Not Saving or Loading

- Confirm that the database is accessible.
- Check for exceptions in the console output.
- Ensure that the database schema is up to date with the latest migrations.

---

## Contact

For any additional support or inquiries:

- **Email**: support@productivityapp.com
- **Website**: [www.productivityapp.com](http://www.productivityapp.com)

---

# Instructions

To use the updated features effectively, please ensure that you have followed the installation and migration steps carefully. Keep your application and dependencies up to date to benefit from the latest improvements.

---

**Happy Productivity!**