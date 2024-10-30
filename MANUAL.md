# Productivity App User Manual

**Version:** 1.0  
**Last Updated:** [Your Update Date]

---

## Introduction

Welcome to the **Productivity App**, a desktop application designed to enhance your time management and productivity. This application combines a feature-rich **Stopwatch**, a customizable **Pomodoro Timer**, and a comprehensive **Session History** to help you track and optimize your work sessions effectively.

This user manual will guide you through the features of the Productivity App and provide instructions on how to use it optimally.

---

## Table of Contents

1. [Getting Started](#getting-started)
   - [System Requirements](#system-requirements)
   - [Installation](#installation)
   - [Launching the Application](#launching-the-application)
2. [Navigating the Interface](#navigating-the-interface)
3. [Stopwatch Component](#stopwatch-component)
   - [Starting the Stopwatch](#starting-the-stopwatch)
   - [Pausing and Resetting](#pausing-and-resetting)
   - [Recording Laps](#recording-laps)
   - [Setting a Custom Start Time](#setting-a-custom-start-time)
4. [Pomodoro Timer Component](#pomodoro-timer-component)
   - [Understanding the Pomodoro Technique](#understanding-the-pomodoro-technique)
   - [Configuring Work and Break Durations](#configuring-work-and-break-durations)
   - [Starting a Pomodoro Session](#starting-a-pomodoro-session)
   - [Adding Extra Time](#adding-extra-time)
   - [Creating Task Categories](#creating-task-categories)
   - [Scheduling Sessions](#scheduling-sessions)
5. [Session History Tab](#session-history-tab)
   - [Viewing Completed Sessions](#viewing-completed-sessions)
   - [Session Details](#session-details)
6. [Tips for Optimal Use](#tips-for-optimal-use)
7. [Troubleshooting](#troubleshooting)
8. [Support and Feedback](#support-and-feedback)

---

## Getting Started

### System Requirements

- **Operating System**: Windows 7 or later, macOS 10.12 Sierra or later, Linux.
- **Python Version**: Python 3.6 or higher.
- **Dependencies**:
  - PyQt5
  - SQLAlchemy
  - psycopg2-binary
- **Database**:
  - PostgreSQL database server

### Installation

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

4. **Initialize the Database**:

   Run the application once to create the necessary tables:

   ```bash
   python main.py
   ```

   If you encounter errors related to the database schema, consider using Alembic for migrations or dropping and recreating the tables as needed.

### Launching the Application

Start the application by running:

```bash
python main.py
```

---

## Navigating the Interface

Upon launching the application, you will see a window with three main tabs:

- **Stopwatch**
- **Pomodoro Timer**
- **Session History**

Use these tabs to navigate between different functionalities of the app.

---

## Stopwatch Component

The **Stopwatch** tab allows you to track time intervals, record laps, and set custom start times.

### Starting the Stopwatch

- Click the **Start** button to begin timing.
- The elapsed time will be displayed in `HH:MM:SS` format.

### Pausing and Resetting

- **Pause**: Click the **Pause** button to pause the stopwatch.
- **Reset**: Click the **Reset** button to reset the stopwatch to zero.

### Recording Laps

- Click the **Lap** button to record a lap time.
- Laps are listed below the time display, showing:
  - **Individual Lap Time**
  - **Cumulative Time**

### Setting a Custom Start Time

- If you forgot to start the stopwatch earlier, you can set a custom start time:
  - Enter the desired time in the `HH:MM:SS` format in the input field.
  - Click the **Set Start Time** button.
  - The stopwatch will start from the specified time.

---

## Pomodoro Timer Component

The **Pomodoro Timer** helps you manage work and break intervals using the Pomodoro Technique.

### Understanding the Pomodoro Technique

The Pomodoro Technique involves working in focused intervals (typically 25 minutes) followed by short breaks (usually 5 minutes). This method aims to improve concentration and productivity.

### Configuring Work and Break Durations

- **Work Duration**:
  - Use the **Work Duration** spin box to set the length of your work sessions.
- **Break Duration**:
  - Use the **Break Duration** spin box to set the length of your breaks.
- Click the **Set Durations** button to apply the changes.

### Starting a Pomodoro Session

- Select a task category from the **Category** drop-down menu.
- Click the **Start** button to begin the timer.
- The timer will count down, indicating the remaining time in the session.

### Adding Extra Time

- If you need more time during a session, click the **+3 Minutes** button to add three minutes to the current timer.

### Creating Task Categories

- Enter a new category name in the **New Category** input field.
- Click the **Add Category** button.
- The category will be added to the **Category** drop-down menu for future sessions.

### Scheduling Sessions

- **Select a Date**:
  - Use the calendar widget to choose a date for scheduling.
- **Add Notes**:
  - Write tasks or notes for the session in the text area provided.
- **Save Session**:
  - Click the **Save Session** button to store the scheduled session.
- **View Scheduled Sessions**:
  - On selecting a date with scheduled sessions, the notes and category will be displayed.

---

## Session History Tab

The **Session History** tab displays all your completed Pomodoro sessions.

### Viewing Completed Sessions

- Sessions are listed in a table format with the following columns:
  - **Date**
  - **Start Time**
  - **End Time**
  - **Category**
  - **Notes**
- The most recent sessions appear at the top.

### Session Details

- Click on a session to view detailed information.
- Use this data to analyze your productivity patterns.

---

## Tips for Optimal Use

- **Consistency**: Stick to regular work and break intervals to build a productive routine.
- **Task Categorization**: Use categories to organize your tasks and focus areas.
- **Session Notes**: Write notes for each session to track progress and plan ahead.
- **Review History**: Regularly check your session history to identify patterns and make adjustments.
- **Custom Durations**: Adjust work and break durations to fit your personal workflow.

---

## Troubleshooting

### Application Does Not Start

- Ensure that all dependencies are installed correctly.
- Verify your database connection and credentials.

### Stopwatch or Timer Not Working

- Make sure you have clicked the **Start** button.
- Check if the durations are set correctly.

### Cannot Save Sessions or Categories

- Confirm that the database is running and accessible.
- Ensure that you have write permissions to the application's directories.

### UI Elements Not Responding

- Restart the application.
- Check for any console error messages for clues.

---

## Support and Feedback

If you encounter issues or have suggestions, please reach out:

- **Email**: support@productivityapp.com
- **GitHub**: [Productivity App Repository](https://github.com/yourusername/productivity_app)

---

**Thank you for choosing the Productivity App! We hope this tool enhances your productivity and time management.**