import csv
import time
from datetime import datetime
from pathlib import Path
from email_validator import validate_email, EmailNotValidError
import requests
from tqdm import tqdm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration
SMTP_SERVER = "smtp.titan.email"
SMTP_PORT = 587
SMTP_USERNAME = "lori.f@transcompanyusa.com"
SMTP_PASSWORD = "YourTitanPasswordhere"
EMAILS_FILE = "emails.csv"
EMAIL_CONTENT_FILE = "email_content.html"
EMAIL_SIGNATURE_FILE = "email_signature.html"
REPORT_FILE = "progress_report.txt"

def get_email_content():
    with open(EMAIL_CONTENT_FILE, "r") as content_file:
        content = content_file.read()

    with open(EMAIL_SIGNATURE_FILE, "r") as signature_file:
        signature = signature_file.read()

    return f"{content}<br>{signature}"

def send_email(name, email, subject, content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Lori <lori.f@transcompanyusa.com>"
    # You must change my email and my name on number 34 to your STMP details to aviod hitting spam box
    msg["To"] = f"{name} <{email}>"

    msg.attach(MIMEText(content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        return True
    except Exception as e:
        print(e)
        return False

def save_report_line(line):
    with open(REPORT_FILE, "a") as report_file:
        report_file.write(line + "\n")

def read_emails_from_file():
    recipients = []
    unique_emails = set()
    duplicate_count = 0
    with open(EMAILS_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row["email"]
            if email not in unique_emails:
                unique_emails.add(email)
                recipients.append({"name": row["name"].strip(), "email": email})
            else:
                duplicate_count += 1
    return recipients, duplicate_count

def main():
    recipients, duplicate_count = read_emails_from_file()
    email_content = get_email_content()
    subject = "Test Jobs Available at ABC Company"
    # You must change email suject to yours on 72

    Path(REPORT_FILE).touch(exist_ok=True)

    default_name = "Candidate"

    verified_count = 0
    unverified_count = 0
    invalid_count = 0

    for recipient in tqdm(recipients, desc="Sending emails", unit="email"):
        email = recipient["email"]
        try:
            validate_email(email)
            name = recipient["name"] if recipient["name"] else default_name
            customized_content = email_content.replace("{name}", name)
            result = send_email(name, email, subject, customized_content)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if result:
                save_report_line(f"{current_time} | {name} | {email} | Verified")
                verified_count += 1
            else:
                save_report_line(f"{current_time} | {name} | {email} | Unverified")
                unverified_count += 1
        except EmailNotValidError:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_report_line(f"{current_time} | {recipient['name']} | {email} | Invalid email")
            invalid_count += 1

    print("Bulk email sending completed.")
    print(f"Total emails sent: {len(recipients)}")
    print(f"Verified emails: {verified_count}")
    print(f"Unverified emails: {unverified_count}")
    print(f"Duplicate emails: {duplicate_count}")
    print(f"Invalid emails: {invalid_count}")

if __name__ == "__main__":
    main()