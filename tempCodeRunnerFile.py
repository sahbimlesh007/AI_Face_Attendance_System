from flask import Flask, render_template, Response, redirect
import pandas as pd
import os
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)


# ================= DASHBOARD =================
@app.route("/")
def dashboard():

    df = pd.read_csv("attendance/attendance.csv")

    total_students = df["Name"].nunique()
    total_attendance = len(df)

    table = df.to_html(classes="table table-striped", index=False)

    return render_template(
        "dashboard.html",
        table=table,
        students=total_students,
        attendance=total_attendance
    )


# ================= LIVE CAMERA =================
def generate_frames():
    while True:

        success, frame = camera.read()

        if not success:
            break

        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ================= REGISTER =================
@app.route("/register")
def register():
    os.system("python capture_face.py")
    return redirect("/")


# ================= TRAIN =================
@app.route("/train")
def train():
    os.system("python train_model.py")
    return redirect("/")


# ================= START ATTENDANCE =================
@app.route("/start")
def start():
    os.system("python face_recognition_system.py")
    return redirect("/")


# ================= ANALYTICS =================
@app.route("/analytics")
def analytics():

    df = pd.read_csv("attendance/attendance.csv")

    data = df["Name"].value_counts()

    labels = list(data.index)
    values = list(data.values)

    return render_template(
        "analytics.html",
        labels=labels,
        values=values
    )


# ================= STUDENTS =================
@app.route("/students")
def students():

    df = pd.read_csv("attendance/attendance.csv")

    students = df["Name"].unique()

    return render_template(
        "students.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)