
import os
import sqlite3

DATABASE_NAME = (
    ":memory:"
    if os.environ.get("VERCEL") == "1"
    else os.path.join(os.path.dirname(os.path.abspath(__file__)), "attendance.db")
)

_connection = None


def get_connection():
    global _connection

    if DATABASE_NAME == ":memory:":
        if _connection is None:
            _connection = sqlite3.connect(
                ":memory:",
                check_same_thread=False
            )
            _connection.row_factory = sqlite3.Row
        return _connection

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('Present', 'Absent')),
            UNIQUE (student_id, attendance_date),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    connection.commit()

    if DATABASE_NAME != ":memory:":
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
