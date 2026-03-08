# AI-Face-Recognition-Attendance-System
Overview

The AI-Face-Recognition-Attendance-System is an intelligent application designed to automate attendance using face recognition technology. It captures, trains, and recognizes faces of students/employees to mark attendance automatically in a CSV-based database. This system eliminates manual attendance, ensures accuracy, and can be used in schools, colleges, and offices.

Features

Real-time Face Recognition: Detects and recognizes faces using your webcam.

Automated Attendance Logging: Attendance automatically recorded in attendance.csv.

Student Database Management: Maintains student information in students.csv.

Face Dataset Creation: Capture multiple face images per student for accurate recognition.

Training Module: Trains a model to recognize faces efficiently.

CSV-based Storage: Easy to export, view, or manipulate attendance records.

Dashboard Interface: User-friendly dashboard for managing and viewing attendance.

Table of Contents

System Requirements

Folder Structure

Installation

Usage

Modules and Scripts

Configuration

How it Works

Troubleshooting

Contributing

License

System Requirements

Operating System: Windows / Linux / macOS

Python Version: 3.9+

Libraries / Dependencies:

OpenCV (opencv-python)

face_recognition

numpy

pandas

Flask

matplotlib (optional for plots)

werkzeug

pillow

Hardware: Webcam for face capture

Installation

Clone the repository:

git clone https://github.com/sahbimlesh007/AI_Face_Attendance_System.git
cd AI-Face-Recognition-Attendance-System

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Usage

Run the Flask Application:

python app.py

Access the Dashboard:

Open your browser and go to http://127.0.0.1:5000/

Register Students:

Navigate to Capture Faces and add a new student.

Capture multiple images for better accuracy.

Train the Model:

After capturing faces, run the training script (if separate):

python train_model.py

This will create/update trainer.yml in the models/ folder.

Mark Attendance:

Go to the Dashboard, start the attendance process, and the system will automatically detect and log attendance for recognized faces in attendance/attendance.csv.

View Attendance:

Open attendance/attendance.csv or view in the dashboard.

Modules and Scripts

app.py – Main Flask application for the dashboard.

train_model.py – Trains face recognition model on the dataset.

capture_faces.py – Script to capture student face images.

facedet/ – Folder containing face detection utilities.

requirements.txt – Python package requirements.

dataset/ – Stores images for each student.

attendance/ – Stores attendance logs.

Configuration

CSV Files:

students.csv – Add student info here: ID, Name, Roll No, Class

attendance/attendance.csv – Attendance logs: Name, Roll No, Date, Time, Status

Face Recognition Model:

Stored in models/trainer.yml.

Retrain whenever new students are added.

How it Works

Face Capture: Captures multiple images per student via webcam.

Model Training: Encodes faces and saves in trainer.yml.

Recognition: Detects faces in real-time and matches with trained dataset.

Attendance Logging: Marks present automatically in CSV.

Dashboard: Provides a UI to manage students, start attendance, and view reports.

Troubleshooting

Webcam Not Working: Check permissions and drivers.

Face Not Recognized: Ensure enough images per student and retrain model.

CSV Not Updating: Ensure proper write permissions for the folder.

Flask App Issues: Make sure no other process is using port 5000.

Contributing

Fork the repository.

Create a branch: git checkout -b feature-name.

Make your changes.

Commit: git commit -m "Add feature".

Push: git push origin feature-name.

Create a Pull Request.

License

This project is licensed under the MIT License. See LICENSE file for details.