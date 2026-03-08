from flask import Flask, render_template, redirect, request, session, url_for
import pandas as pd
import os
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "secret123"   # required for login session


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # simple admin login
        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    df = pd.read_csv("attendance/attendance.csv")

    table = df.to_html(classes="data", index=False)

    return render_template(
        "dashboard.html",
        table=table
    )


# ---------------- REGISTER STUDENT ----------------

@app.route("/register")
def register():

    if "user" not in session:
        return redirect("/login")

    os.system("python capture_face.py")

    return redirect("/")


# ---------------- TRAIN MODEL ----------------

@app.route("/train")
def train():

    if "user" not in session:
        return redirect("/login")

    os.system("python train_model.py")

    return redirect("/")


# ---------------- START ATTENDANCE ----------------

@app.route("/start")
def start():

    if "user" not in session:
        return redirect("/login")

    os.system("python face_recognition_system.py")

    return redirect("/")


# ---------------- ANALYTICS ----------------



@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    # Load CSV without headers
    df = pd.read_csv("attendance/attendance.csv", header=None)
    df.columns = ["ID", "Name", "Date", "Time"]

    # Count attendance per student
    attendance_count = df.groupby("Name")["ID"].count()

    # Plot
    plt.figure(figsize=(8,5))
    attendance_count.plot(kind="bar", color="skyblue")
    plt.title("Total Attendance per Student")
    plt.ylabel("Attendance Count")
    plt.xlabel("Student Name")
    plt.tight_layout()

    # Convert to image
    img = BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Render template
    return render_template("analytics.html", plot_url=plot_url)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)