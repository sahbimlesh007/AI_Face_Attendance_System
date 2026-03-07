import cv2
import datetime
import csv
from database import connect

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("models/trainer.yml")

faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

def mark_attendance(student_id,name):

    now = datetime.datetime.now()

    date = now.strftime("%Y-%m-%d")

    time = now.strftime("%H:%M:%S")

    with open("attendance/attendance.csv","a",newline="") as f:

        writer = csv.writer(f)

        writer.writerow([student_id,name,date,time])

    db = connect()

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO attendance VALUES (%s,%s,%s,%s)",
        (student_id,name,date,time)
    )

    db.commit()

while True:

    ret,img = cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,1.3,5)

    for(x,y,w,h) in faces:

        id,confidence = recognizer.predict(gray[y:y+h,x:x+w])

        db = connect()

        cursor = db.cursor()

        cursor.execute(
            "SELECT name FROM students WHERE id=%s",
            (id,)
        )

        name = cursor.fetchone()

        if name:

            name = name[0]

            mark_attendance(id,name)

            cv2.putText(
                img,
                name,
                (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow("Face Recognition Attendance",img)

    if cv2.waitKey(1)==27:
        break

cam.release()
cv2.destroyAllWindows()