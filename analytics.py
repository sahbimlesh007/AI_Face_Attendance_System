import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("attendance/attendance.csv")

attendance_count = df["Name"].value_counts()

attendance_count.plot(kind="bar")

plt.title("Attendance Analytics")

plt.xlabel("Students")

plt.ylabel("Attendance Count")

plt.show()