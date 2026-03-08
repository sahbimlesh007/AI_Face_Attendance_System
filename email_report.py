import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import config


def send_report():

    sender = config.EMAIL_ADDRESS
    receiver = config.RECEIVER_EMAIL

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "AI Attendance Report"

    body = "Hello,\n\nAttached is the latest attendance report.\n\nRegards,\nAI Attendance System"
    msg.attach(MIMEText(body, "plain"))

    # Attach CSV file
    filename = "attendance/attendance.csv"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={filename}",
    )

    msg.attach(part)

    # Connect to Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, config.EMAIL_PASSWORD)

    text = msg.as_string()

    server.sendmail(sender, receiver, text)

    server.quit()

    print("Email with attendance report sent successfully")


if __name__ == "__main__":
    send_report()