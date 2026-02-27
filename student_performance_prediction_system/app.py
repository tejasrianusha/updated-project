from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

CSV_FILE = "student_data.csv"

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Roll Number", "Name", "Phone", "Email", "Password"])
    df.to_csv(CSV_FILE, index=False)


# -------------------- LOGIN --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        roll = request.form["roll"].strip()
        password = request.form["password"].strip()

        df = pd.read_csv(CSV_FILE, dtype=str)   # ✅ LOAD CSV HERE

        student = df[df["Roll Number"].astype(str) == roll]

        if not student.empty:
            stored_password = student.iloc[0]["Password"]

            if password == stored_password:
                session["roll"] = roll
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect Password", "danger")
        else:
            flash("Roll Number Not Found", "danger")

    return render_template("index.html")

# -------------------- REGISTER --------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        roll = request.form["roll number"].strip()
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        df = pd.read_csv(CSV_FILE, dtype=str)

        if roll in df["Roll Number"].values:
            return "<script>alert('Roll Number already exists!'); window.location='/register';</script>"

        new_student = {
            "Roll Number": roll,
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Password": password
        }

        df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        # 🔥 Professional popup + redirect
        return """
        <script>
            alert("🎉 Registration Successful!\\n\\nNow login with your Roll Number and Password.");
            window.location = "/";
        </script>
        """

    return render_template("register.html")

# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():

    if "roll" not in session:
        return redirect(url_for("index"))

    df = pd.read_csv(CSV_FILE, dtype=str)  # ✅ LOAD CSV HERE

    roll = session["roll"]

    student_data = df[df["Roll Number"].astype(str) == roll]

    if student_data.empty:
        flash("Student not found", "error")
        return redirect(url_for("index"))

    student = student_data.iloc[0].to_dict()

    # SAFE FLOAT CONVERSION
    def safe_float(value):
        try:
            return float(value)
        except:
            return 0.0

    # Convert Placement Readiness to float (for doughnut chart)
    student["Placement Readiness"] = safe_float(
        student.get("Placement Readiness")
    )

    semesters = ["Sem1","Sem2","Sem3","Sem4","Sem5","Sem6"]

    sem_marks = [safe_float(student.get(f"{s} Marks")) for s in semesters]
    sem_perc = [safe_float(student.get(f"{s} Percentage")) for s in semesters]

    bca_scores = [
        safe_float(student.get("Internal Exam1 Marks")),
        safe_float(student.get("Internal Exam2 Marks")),
        safe_float(student.get("Assignment Average")),
        safe_float(student.get("Lab Marks")),
        safe_float(student.get("Mini Project Marks")),
        safe_float(student.get("Major Project Marks"))
    ]

    bca_labels = ["Internal1","Internal2","Assignment","Lab","Mini","Major"]

    return render_template(
        "dashboard.html",
        student=student,
        semesters=semesters,
        sem_marks=sem_marks,
        sem_perc=sem_perc,
        bca_scores=bca_scores,
        bca_labels=bca_labels
    )
# -------------------- MANUAL PREDICTION --------------------
@app.route("/manual_prediction", methods=["GET", "POST"])
def manual_prediction():
    prediction = None
    career = None
    suggestion = None

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        gender = request.form["gender"]
        sem_marks = float(request.form["sem_marks"])
        gpa = float(request.form["gpa"])
        attendance = float(request.form["attendance"])
        assignment = request.form["assignment"]
        study_hours = float(request.form["study_hours"])

        # Simple logic
        score = (sem_marks * 0.4) + (gpa * 10 * 0.3) + (attendance * 0.2) + (study_hours * 2)

        if assignment == "Yes":
            score += 5

        if score >= 75:
            prediction = "Excellent"
            career = "Software Developer / Data Scientist"
            suggestion = "Keep improving coding & real-world projects."
        elif score >= 55:
            prediction = "Average"
            career = "System Analyst / Support Engineer"
            suggestion = "Improve consistency & practical exposure."
        else:
            prediction = "Needs Improvement"
            career = "Skill Development Required"
            suggestion = "Focus on fundamentals & daily study habits."

        return render_template("manual_prediction.html",
                               prediction=prediction,
                               career=career,
                               suggestion=suggestion,
                               name=name,
                               roll=roll,
                               gender=gender,
                               sem_marks=sem_marks,
                               gpa=gpa,
                               attendance=attendance,
                               assignment=assignment,
                               study_hours=study_hours)

    return render_template("manual_prediction.html")
from flask import send_file
import os

@app.route("/download_csv")
def download_csv():
    return send_file(
        CSV_FILE,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)