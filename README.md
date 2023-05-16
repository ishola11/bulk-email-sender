# Bulk Email Sender Script

This script allows you to send bulk emails to a list of recipients using a CSV file, a pre-defined email template and a signature file. The script uses the email_validator library to validate email addresses and the smtplib library to send emails over a SMTP server.

## Requirements

- Python 3.x
- email_validator
- tqdm

## Installation

1. Clone this repository to your local machine using `git clone https://github.com/ishola11/bulk-email-sender.git`.
2. Install the required packages using `pip install -r requirements.txt`.
3. Update the configuration variables in the script to match your SMTP server details, email content file, signature file and CSV file containing the list of recipients.
4. Run the script using `python bulk_email_sender.py`.

## Usage

1. Create a CSV file containing a list of recipients with their name and email address. The file should have two columns: "name" and "email".
2. Create an email content file and a signature file in HTML format. The email content file should contain the email message template, while the signature file should contain your email signature.
3. Update the configuration variables in the script to match your SMTP server details, email content file, signature file and CSV file containing the list of recipients.
4. Run the script using `python bulk_email_sender.py`.
5. The script will validate each email address using the email_validator library, and send the email to the recipient using the provided SMTP server details.
6. The script will generate a progress report file containing the status of each email sent.

## Configuration

The script includes several configuration variables that can be customized to match your needs:

- SMTP_SERVER: The address of the SMTP server used to send emails.
- SMTP_PORT: The port number of the SMTP server used to send emails.
- SMTP_USERNAME: The username used to authenticate with the SMTP server.
- SMTP_PASSWORD: The password used to authenticate with the SMTP server.
- EMAILS_FILE: The name of the CSV file containing the list of recipients.
- EMAIL_CONTENT_FILE: The name of the HTML file containing the email message template.
- EMAIL_SIGNATURE_FILE: The name of the HTML file containing your email signature.
- REPORT_FILE: The name of the file used to store the progress report.

## Credits

This script was created by Mjay (www.mjaycloud.com) and is licensed under the MIT License. It uses the email_validator library and the tqdm library, which are both open-source projects available on GitHub.
