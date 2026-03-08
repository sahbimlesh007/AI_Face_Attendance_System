@app.route("/")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    # Load master student list
    students_df = pd.read_csv("attendance/students.csv")  # ID, Name

    # Load attendance CSV
    try:
        attendance_df = pd.read_csv("attendance/attendance.csv", header=None)
        attendance_df.columns = ["ID", "Name", "Date", "Time"]

        # Convert Time to datetime.time
        attendance_df["Time"] = pd.to_datetime(attendance_df["Time"]).dt.time

        # Filter attendance between 08:30 and 09:30
        start_time = time(8, 30)
        end_time = time(9, 30)
        attendance_window = attendance_df[
            (attendance_df["Time"] >= start_time) &
            (attendance_df["Time"] <= end_time)
        ]

        # List of students present in time window
        present_students = attendance_window["Name"].tolist()
    except FileNotFoundError:
        present_students = []

    # Build table HTML with Status column
    table_html = '<table class="data">'
    table_html += "<tr><th>ID</th><th>Name</th><th>Status</th></tr>"

    for _, row in students_df.iterrows():
        student_id = row["ID"]
        name = row["Name"]
        if name in present_students:
            status = "Present"
            color = "green"
        else:
            status = "Absent"
            color = "red"
        table_html += f'<tr><td>{student_id}</td><td>{name}</td><td style="color:{color}; font-weight:bold">{status}</td></tr>'
    table_html += "</table>"

    return render_template("dashboard.html", table=table_html)