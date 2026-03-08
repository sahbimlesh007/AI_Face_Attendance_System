from flask import Flask, render_template, redirect, request, session, url_for
import pandas as pd
import os
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')  # prevents GUI issues on server
import matplotlib.pyplot as plt
from datetime import datetime, time

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    # Always show login page first
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        print("Login attempt:", username, password)  # debug info

        if username.lower() == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    # Always redirect to login page
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    # Load students list
    students_file = "attendance/students.csv"
    if os.path.exists(students_file):
        students_df = pd.read_csv(students_file)
    else:
        return "students.csv not found!"

    # Load attendance records
    attendance_file = "attendance/attendance.csv"
    if os.path.exists(attendance_file):
        attendance_df = pd.read_csv(attendance_file)
    else:
        attendance_df = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])

    # Set attendance window (optional)
    start_time = session.get("start_time", "08:30:00")
    end_time = session.get("end_time", "09:30:00")
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

    # Convert attendance time to time object
    if not attendance_df.empty:
        attendance_df["Time"] = pd.to_datetime(attendance_df["Time"]).dt.time
        present_students = attendance_df[
            (attendance_df["Time"] >= start_time_obj) &
            (attendance_df["Time"] <= end_time_obj)
        ]["Name"].tolist()
    else:
        present_students = []

    # Prepare table with Status
    students_df["Status"] = students_df["Name"].apply(lambda x: "Present" if x in present_students else "Absent")

    # Convert to records for Jinja
    students = students_df.to_dict(orient="records")

    return render_template("dashboard.html", students=students)

# ---------------- REGISTER STUDENT ----------------
@app.route("/register")
def register():
    if "user" not in session:
        return redirect(url_for("login"))
    ret = os.system("python capture_face.py")
    if ret != 0:
        return "Error running capture_face.py"
    return redirect(url_for("dashboard"))

# ---------------- TRAIN MODEL ----------------
@app.route("/train")
def train():
    if "user" not in session:
        return redirect(url_for("login"))
    ret = os.system("python train_model.py")
    if ret != 0:
        return "Error running train_model.py"
    return redirect(url_for("dashboard"))

# ---------------- START ATTENDANCE ----------------
# ---------------- START ATTENDANCE ----------------
@app.route("/start")
def start():
    if "user" not in session:
        return redirect(url_for("login"))

    # Set fixed attendance time
    start_time_obj = datetime.strptime("08:30:00", "%H:%M:%S").time()
    end_time_obj = datetime.strptime("09:30:00", "%H:%M:%S").time()
    session["start_time"] = start_time_obj.strftime("%H:%M:%S")
    session["end_time"] = end_time_obj.strftime("%H:%M:%S")

    # Run face recognition attendance script
    ret = os.system("python face_recognition_system.py")
    if ret != 0:
        return "Error running face_recognition_system.py"

    return redirect(url_for("dashboard"))

# ---------------- ANALYTICS ----------------
@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect(url_for("login"))

    attendance_file = "attendance/attendance.csv"
    if os.path.exists(attendance_file):
        df = pd.read_csv(attendance_file)
    else:
        df = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])

    if not df.empty:
        attendance_count = df.groupby("Name")["ID"].count()
    else:
        attendance_count = pd.Series(dtype=int)

    plt.figure(figsize=(8, 5))
    attendance_count.plot(kind="bar", color="skyblue")
    plt.title("Total Attendance per Student")
    plt.ylabel("Attendance Count")
    plt.xlabel("Student Name")
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("analytics.html", plot_url=plot_url)

# ---------------- ABSENT MARKING ----------------
@app.route("/absent")
def absent():
    if "user" not in session:
        return redirect(url_for("login"))

    students_file = "attendance/students.csv"
    if os.path.exists(students_file):
        students_df = pd.read_csv(students_file)
    else:
        return "students.csv not found!"

    attendance_file = "attendance/attendance.csv"
    if os.path.exists(attendance_file):
        attendance_df = pd.read_csv(attendance_file)
    else:
        attendance_df = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])

    start_time = session.get("start_time", "08:30:00")
    end_time = session.get("end_time", "09:30:00")
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

    if not attendance_df.empty:
        attendance_df["Time"] = pd.to_datetime(attendance_df["Time"]).dt.time
        present_students = attendance_df[
            (attendance_df["Time"] >= start_time_obj) &
            (attendance_df["Time"] <= end_time_obj)
        ]["Name"].tolist()
    else:
        present_students = []

    absent_students = [s for s in students_df["Name"].tolist() if s not in present_students]

    return render_template("absent.html", absent_students=absent_students, start=start_time, end=end_time)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)