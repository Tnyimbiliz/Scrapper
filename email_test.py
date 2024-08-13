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

def login():
    print("🔃 Logging in....")

    username = '770125562'
    password = 'thebag'

    try:
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-text-field__slot'))
        )
        username_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Mobile Number" and @type="number"]')
        password_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Password" and @type="password"]')
        
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-btn__content'))
        )
        cancel_button = parent_element.find_element(By.XPATH, '//button[@type="button" and @class="v-icon notranslate v-icon--link theme--light"]')

        cancel_button.click()
        login_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"mx-1") and contains(@class,"rounded-lg") and contains(@class,"v-btn") and contains(@class,"v-btn--text") and contains(@class,"theme--dark") and contains(@class,"v-size--default") and contains(@class,"white") and contains(@class,"font-weight-black")]'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("✅ Logged in successfully!")
        driver.minimize_window()

    except Exception as e:
        print(f"❌ Unable to login: {e}")
        time.sleep(30)
        driver.quit()

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
