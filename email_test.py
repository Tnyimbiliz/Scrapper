import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "asventuresx@outlook.com"
EMAIL_PASSWORD = "Instacred@2024"

# Recipients
RECIPIENTS = ["jortiatisthomas@gmail.com"]

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENTS, msg.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"SMTP Authentication Error: {auth_error}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage to test the email function
subject = "Test Email"
body = "This is a test email to check the functionality of the email sending script."
send_email(subject, body)
