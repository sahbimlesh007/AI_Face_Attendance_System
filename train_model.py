import cv2
import numpy as np
from PIL import Image
import os

def train_model():

    path = "dataset"

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    ids = []

    for image in os.listdir(path):

        img_path = os.path.join(path,image)

        img = Image.open(img_path).convert('L')

        img_np = np.array(img,'uint8')

        student_id = int(image.split(".")[1])

        faces.append(img_np)
        ids.append(student_id)

    recognizer.train(faces,np.array(ids))

    if not os.path.exists("models"):
        os.makedirs("models")

    recognizer.save("models/trainer.yml")

    print("Model Trained Successfully")


if __name__ == "__main__":
    train_model()