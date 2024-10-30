# models.py

# Important:

# `productivity_app % brew services start postgresql`

# Database Connection String: Replace 'app_user', 'your_password', and 'productivity_app' with your actual PostgreSQL username, password, and database name.
# Explanation:

# Sets up the connection to the PostgreSQL database using SQLAlchemy.
# Defines the ScheduledSession model to represent scheduled Pomodoro sessions.
# Creates the necessary database tables if they do not exist.

# Create a Database User (Optional):

# Create a user with a password:

# sql
# Copy code
# CREATE USER app_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE productivity_app TO app_user;
# models.py

from sqlalchemy import (
    create_engine, Column, Integer, String, Text,
    Date, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this connection string with your PostgreSQL credentials
DATABASE_URI = 'postgresql+psycopg2://postgres:Bashor47@localhost/productivity_app'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ScheduledSession(Base):
    __tablename__ = 'scheduled_sessions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    planned_start_time = Column(DateTime)
    planned_end_time = Column(DateTime)
    actual_start_time = Column(DateTime)
    actual_end_time = Column(DateTime)
    category = Column(String(50), nullable=False)
    notes = Column(Text)
    status = Column(String(20), nullable=False, default='planned')  # 'planned', 'in progress', 'completed'

    def __repr__(self):
        return f"<ScheduledSession(id={self.id}, date={self.date}, category='{self.category}', status='{self.status}')>"

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    session_duration = Column(Integer, default=25)
    sessions_per_cycle = Column(Integer, default=4)
    short_break_duration = Column(Integer, default=5)
    long_break_duration = Column(Integer, default=30)

    def __repr__(self):
        return f"<Settings(id={self.id}, session_duration={self.session_duration}, sessions_per_cycle={self.sessions_per_cycle})>"

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(engine)