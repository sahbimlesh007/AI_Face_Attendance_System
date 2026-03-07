
# Create folders
mkdir -p dataset
mkdir -p models
mkdir -p attendance
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Create files
touch models/trainer.yml
touch attendance/attendance.csv

touch static/css/style.css
touch static/js/script.js

touch templates/login.html
touch templates/dashboard.html
touch templates/analytics.html

touch capture_face.py
touch train_model.py
touch face_recognition_system.py
touch mask_detection.py
touch analytics.py
touch database.py
touch email_report.py
touch app.py
touch gui_app.py
touch config.py
touch requirements.txt

echo "Project structure created successfully!"