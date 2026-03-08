import cv2
import datetime
import csv
import time
from database import connect
import email_report


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/trainer.yml")

faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

marked_students = set()


# ==============================
# MARK ATTENDANCE
# ==============================

def mark_attendance(student_id, name):

    now = datetime.datetime.now()

    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    # Save to CSV
    with open("attendance/attendance.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([student_id, name, date, time_now])

    # Save to database
    db = connect()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO attendance VALUES (%s,%s,%s,%s)",
        (student_id, name, date, time_now)
    )

    db.commit()

    cursor.close()
    db.close()


print("Starting Face Recognition Attendance...")

verified = False

while True:

    ret, img = cam.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        student_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 70:

            db = connect()
            cursor = db.cursor()

            cursor.execute(
                "SELECT name FROM students WHERE id=%s",
                (student_id,)
            )

            result = cursor.fetchone()

            cursor.close()
            db.close()

            if result:

                name = result[0]

                if student_id not in marked_students:

                    mark_attendance(student_id, name)

                    marked_students.add(student_id)

                    verified = True

                    cv2.putText(
                        img,
                        "Attendance Marked",
                        (x, y - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2
                    )

                    cv2.imshow("Face Recognition Attendance", img)

                    # Wait 2 seconds then close
                    cv2.waitKey(2000)

                    break

                cv2.putText(
                    img,
                    name,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        else:

            cv2.putText(
                img,
                "Unknown",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Face Recognition Attendance", img)

    if verified:
        break

    if cv2.waitKey(1) == 27:   # ESC to exit
        break


# ==============================
# CLOSE CAMERA AUTOMATICALLY
# ==============================

cam.release()
cv2.destroyAllWindows()

print("Attendance session completed")


# ==============================
# SEND EMAIL REPORT
# ==============================

try:
    email_report.send_report()
    print("Attendance report email sent")
except:
    print("Email sending failed")