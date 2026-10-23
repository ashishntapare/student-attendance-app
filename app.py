
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from database import initialize_database, get_connection

app = Flask(__name__)
app.secret_key = "student-attendance-local-key"

import os

if os.environ.get("VERCEL") != "1":
    initialize_database()


@app.route("/")
def home():
    selected_date = request.args.get("date", date.today().isoformat())

    # Accept only a valid calendar date.
    try:
        date.fromisoformat(selected_date)
    except ValueError:
        selected_date = date.today().isoformat()

    connection = get_connection()

    students = connection.execute(
        """
        SELECT
            students.id,
            students.roll_number,
            students.name,
            students.course,
            attendance.status
        FROM students
        LEFT JOIN attendance
            ON students.id = attendance.student_id
            AND attendance.attendance_date = ?
        ORDER BY students.roll_number
        """,
        (selected_date,)
    ).fetchall()

    total_students = len(students)

    present_count = sum(
        1 for student in students
        if student["status"] == "Present"
    )

    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        present_count=present_count,
        selected_date=selected_date
    )


@app.route("/add-student", methods=["POST"])
def add_student():
    roll_number = request.form.get("roll_number", "").strip()
    name = request.form.get("name", "").strip()
    course = request.form.get("course", "").strip()

    if not roll_number or not name or not course:
        flash("Please fill in all three fields.", "error")
        return redirect(url_for("home"))

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO students (roll_number, name, course)
            VALUES (?, ?, ?)
            """,
            (roll_number, name, course)
        )
        connection.commit()
        flash("Student registered successfully!", "success")

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            flash("That roll number already exists.", "error")
        else:
            app.logger.exception("Could not register student")
            flash("Could not register student. Please try again.", "error")

    finally:
        connection.close()

    return redirect(url_for("home"))


@app.route("/mark-attendance", methods=["POST"])
def mark_attendance():
    selected_date = request.form.get("attendance_date", "").strip()

    try:
        date.fromisoformat(selected_date)
    except ValueError:
        flash("Please select a valid date.", "error")
        return redirect(url_for("home"))

    connection = get_connection()

    try:
        students = connection.execute(
            "SELECT id FROM students"
        ).fetchall()

        for student in students:
            status = request.form.get(f"status_{student['id']}")

            if status not in ("Present", "Absent"):
                continue

            connection.execute(
                """
                INSERT INTO attendance
                    (student_id, attendance_date, status)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, attendance_date)
                DO UPDATE SET status = excluded.status
                """,
                (student["id"], selected_date, status)
            )

        connection.commit()
        flash("Attendance saved successfully!", "success")

    except Exception:
        connection.rollback()
        app.logger.exception("Could not save attendance")
        flash("Could not save attendance. Please try again.", "error")

    finally:
        connection.close()

    return redirect(url_for("home", date=selected_date))


if __name__ == "__main__":
    app.run(debug=True)
