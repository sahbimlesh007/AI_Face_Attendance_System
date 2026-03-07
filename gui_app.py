import tkinter as tk
import subprocess

def register():
    subprocess.run(["python","capture_face.py"])

def train():
    subprocess.run(["python","train_model.py"])

def attendance():
    subprocess.run(["python","face_recognition_system.py"])

def dashboard():
    subprocess.run(["python","app.py"])

root = tk.Tk()

root.title("AI Attendance System")

root.geometry("400x400")

tk.Label(root,text="AI Face Attendance System",
font=("Arial",18)).pack(pady=20)

tk.Button(root,text="Register Student",
width=25,command=register).pack(pady=10)

tk.Button(root,text="Train Model",
width=25,command=train).pack(pady=10)

tk.Button(root,text="Start Attendance",
width=25,command=attendance).pack(pady=10)

tk.Button(root,text="Open Dashboard",
width=25,command=dashboard).pack(pady=10)

root.mainloop()