import csv
import time
import sys
from datetime import datetime
from pathlib import Path
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Configuration
SMTP_SERVER = "smtp.titan.email"
SMTP_PORT = 587
SMTP_USERNAME = "youremailaddress"
SMTP_PASSWORD = "yourpassword"
EMAILS_FILE = "emails.csv"
EMAIL_CONTENT_FILE = "email_content.html"
EMAIL_SIGNATURE_FILE = "email_signature.html"
REPORT_FILE = "progress_report.txt"

EMAIL_SUBJECT = "add emaill subject"  # Subject updates
EMAIL_FROM_NAME = "YourName"  # Sender name
EMAIL_FROM_ADDRESS = "senderemailaddress"  # Sender email
DELAY_BETWEEN_EMAILS = 10  # Delay time (seconds) to prevent rate limits

# Hacker-style print effect
def hacker_print(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  

def get_email_content():
    with open(EMAIL_CONTENT_FILE, "r") as content_file:
        content = content_file.read()

    with open(EMAIL_SIGNATURE_FILE, "r") as signature_file:
        signature = signature_file.read()

    return f"{content}<br>{signature}"

def send_email(name, email, subject, content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM_ADDRESS}>"  # Easy sender config
    msg["To"] = f"{name} <{email}>"

    msg.attach(MIMEText(content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        return True
    except Exception as e:
        print(Fore.RED + f"Error sending to {email}: {e}")
        return False

def save_report_line(line):
    with open(REPORT_FILE, "a", encoding="utf-8") as report_file: 
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
    hacker_print(Fore.GREEN + "Initializing email sender... Access granted. ✅", delay=0.03)
    time.sleep(1)
    
    recipients, duplicate_count = read_emails_from_file()
    email_content = get_email_content()

    Path(REPORT_FILE).touch(exist_ok=True)

    hacker_print(Fore.YELLOW + f"\n📂 {len(recipients)} unique email addresses loaded.")
    hacker_print(Fore.RED + f"⚠️ {duplicate_count} duplicate emails skipped.\n")

    default_name = "Candidate"

    verified_count = 0
    unverified_count = 0
    invalid_count = 0

    hacker_print(Fore.CYAN + "🚀 Engaging email transmission sequence...\n", delay=0.02)
    time.sleep(1)

    for recipient in tqdm(recipients, desc=Fore.GREEN + "Sending emails", unit="email"):
        email = recipient["email"]
        try:
            validate_email(email)
            name = recipient["name"] if recipient["name"] else default_name
            customized_content = email_content.replace("{name}", name)
            result = send_email(name, email, EMAIL_SUBJECT, customized_content)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if result:
                save_report_line(f"{current_time} | {name} | {email} | ✅ Sent")
                verified_count += 1
                print(Fore.GREEN + f"[✔] Email successfully sent to {name} ({email})")
            else:
                save_report_line(f"{current_time} | {name} | {email} | ❌ Failed")
                unverified_count += 1
                print(Fore.RED + f"[✖] Failed to send email to {name} ({email})")

        except EmailNotValidError:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_report_line(f"{current_time} | {recipient['name']} | {email} | ❌ Invalid email")
            invalid_count += 1
            print(Fore.RED + f"[⚠] Invalid email detected: {email}")

        time.sleep(DELAY_BETWEEN_EMAILS)  # Delay to avoid SMTP limits

    # Final report summary
    hacker_print(Fore.MAGENTA + "\n💾 Transmission Summary Report:", delay=0.03)
    hacker_print(Fore.GREEN + f"✅ Successfully sent: {verified_count}", delay=0.02)
    hacker_print(Fore.YELLOW + f"⚠️ Failed to send: {unverified_count}", delay=0.02)
    hacker_print(Fore.RED + f"🚨 Invalid emails: {invalid_count}", delay=0.02)
    hacker_print(Fore.BLUE + f"🔁 Duplicates ignored: {duplicate_count}", delay=0.02)

    hacker_print(Fore.CYAN + "\n💻 Data stored in progress_report.txt", delay=0.03)
    hacker_print(Fore.GREEN + "📡 Email transmission complete. Logging out... 🔒\n", delay=0.05)
    time.sleep(1)

if __name__ == "__main__":
    main()
