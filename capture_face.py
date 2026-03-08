import cv2
import os
from database import connect

def capture_student():

    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")

    db = connect()
    cursor = db.cursor()


    cursor.execute(
        "INSERT INTO students (id,name) VALUES (%s,%s)",
        (student_id,name)
    )

    db.commit()

    cam = cv2.VideoCapture(0)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    count = 0

    while True:

        ret,img = cam.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = detector.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:

            count += 1

            cv2.imwrite(
                f"dataset/User.{student_id}.{count}.jpg",
                gray[y:y+h,x:x+w]
            )

            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Register Face",img)

        if cv2.waitKey(1)==27 or count>=30:
            break

    cam.release()
    cv2.destroyAllWindows()

    print("Student Registered Successfully")


if __name__ == "__main__":
    capture_student()

# import cv2
# print(cv2.__version__)