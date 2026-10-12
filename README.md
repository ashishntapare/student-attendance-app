# Student Attendance Application

A web-based student attendance management application built with Python, Flask, and SQLite.

## Features

- Register student records with roll number, name, and course.
- Store student information in an SQLite database.
- Mark students as Present or Absent.
- Record attendance by date.
- View registered students and attendance records on a dashboard.
- Prevent duplicate roll numbers and duplicate attendance entries for the same student on the same date.

## Technologies

- Python
- Flask
- SQLite
- HTML and CSS
- Git and GitHub

## Installation and Setup

1. Install Python 3.10 or later.
2. Clone this repository:

   ```bash
   git clone https://github.com/ashishntapare/student-attendance-app.git
   ```

3. Open the project folder:

   ```bash
   cd student-attendance-app
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

## Project Structure

```text
student-attendance-app/
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    └── index.html
```

## Database

The application uses SQLite. The database file is created locally when the application runs and is excluded from Git using `.gitignore`.

## Privacy and Security

This project is intended for learning and demonstration. Avoid using real student information in public demonstrations. Before production use, implement appropriate authentication, authorization, input validation, and security protections.

## Author

Ashish N Tapare

## License

This project is available for educational and portfolio purposes.