import smtplib
from email.mime.text import MIMEText
import config

def send_report():

    msg = MIMEText("Attendance report generated.")

    msg["Subject"] = "Attendance Report"

    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = config.RECEIVER_EMAIL

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(
        config.EMAIL_ADDRESS,
        config.EMAIL_PASSWORD
    )

    server.send_message(msg)

    server.quit()

    print("Email Sent")