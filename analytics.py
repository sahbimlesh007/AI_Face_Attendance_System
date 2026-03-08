import pandas as pd
import matplotlib.pyplot as plt

# Load attendance data
df = pd.read_csv("attendance/attendance.csv")

# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# ==============================
# Student Attendance Count
# ==============================

attendance_count = df["Name"].value_counts()

plt.figure(figsize=(10,5))
attendance_count.plot(kind="bar", color="skyblue")

plt.title("Student Attendance Count")
plt.xlabel("Students")
plt.ylabel("Total Attendance")
plt.xticks(rotation=45)
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# ==============================
# Daily Attendance Trend
# ==============================

daily_attendance = df.groupby("Date").size()

plt.figure(figsize=(10,5))
daily_attendance.plot(kind="line", marker="o")

plt.title("Daily Attendance Trend")
plt.xlabel("Date")
plt.ylabel("Number of Students")
plt.grid(True)

plt.tight_layout()
plt.show()


# ==============================
# Top 5 Students Attendance
# ==============================

top_students = attendance_count.head(5)

plt.figure(figsize=(8,5))
top_students.plot(kind="pie", autopct="%1.1f%%")

plt.title("Top 5 Students Attendance Share")
plt.ylabel("")

plt.tight_layout()
plt.show()