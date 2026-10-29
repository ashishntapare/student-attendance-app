
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student-attendance-demo-key"

# Temporary demo data. Resets when the server restarts.
students = [
    {"id": 1, "roll_number": "101", "name": "Demo Student One", "course": "BSc Computer Science", "status": None},
    {"id": 2, "roll_number": "102", "name": "Demo Student Two", "course": "BSc Computer Science", "status": None},
    {"id": 3, "roll_number": "103", "name": "Demo Student Three", "course": "BSc Computer Science", "status": None},
]

attendance_records = {}


@app.route("/")
def home():
    selected_date = request.args.get("date", date.today().isoformat())
    try:
        date.fromisoformat(selected_date)
    except ValueError:
        selected_date = date.today().isoformat()

    display_students = []
    for student in students:
        item = student.copy()
        item["status"] = attendance_records.get(
            (student["id"], selected_date)
        )
        display_students.append(item)

    total_students = len(display_students)
    present_count = sum(
        1 for student in display_students
        if student["status"] == "Present"
    )

    return render_template(
        "index.html",
        students=display_students,
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

    if any(s["roll_number"] == roll_number for s in students):
        flash("That roll number already exists.", "error")
        return redirect(url_for("home"))

    students.append({
        "id": max((s["id"] for s in students), default=0) + 1,
        "roll_number": roll_number,
        "name": name,
        "course": course,
        "status": None
    })
    flash("Demo student added successfully!", "success")
    return redirect(url_for("home"))


@app.route("/mark-attendance", methods=["POST"])
def mark_attendance():
    selected_date = request.form.get("attendance_date", "").strip()
    try:
        date.fromisoformat(selected_date)
    except ValueError:
        flash("Please select a valid date.", "error")
        return redirect(url_for("home"))

    for student in students:
        status = request.form.get(f"status_{student['id']}")
        if status in ("Present", "Absent"):
            attendance_records[(student["id"], selected_date)] = status

    flash("Demo attendance saved!", "success")
    return redirect(url_for("home", date=selected_date))


if __name__ == "__main__":
    app.run(debug=True)
