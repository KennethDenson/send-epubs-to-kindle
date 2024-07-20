import os
import fnmatch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

# File to keep track of sent .epub files
SENT_FILES_LOG = 'sent_files.log'

def load_sent_files():
    if os.path.exists(SENT_FILES_LOG):
        with open(SENT_FILES_LOG, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_sent_file(file_path):
    with open(SENT_FILES_LOG, 'a') as file:
        file.write(file_path + '\n')

def find_epub_files(directory, sent_files):
    epub_files = []
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        # Filter out .epub files and add them to the list if they have not been sent
        for filename in fnmatch.filter(files, '*.epub'):
            file_path = os.path.join(root, filename)
            if file_path not in sent_files:
                epub_files.append(file_path)
    return epub_files

def send_email(smtp_server, port, login, password, to_email, subject, body, file_path):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the .epub file
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
        msg.attach(part)
    
    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Secure the connection
        server.login(login, password)
        server.sendmail(login, to_email, msg.as_string())

def main():
    # Define the directory to search and email server details
    directory_to_search = '/path/to/search'  # <-- EDIT THIS: Change to the directory you want to search
    smtp_server = 'your_smtp_server'         # <-- EDIT THIS: Change to your SMTP server address
    port = 587                               # <-- EDIT THIS: Change to your SMTP server port if different
    email_login = os.environ['EMAIL_LOGIN']  # <-- SET ENVIRONMENT VARIABLE: Your email login
    email_password = os.environ['EMAIL_PASSWORD']  # <-- SET ENVIRONMENT VARIABLE: Your email password
    to_email = 'kindle-email-address'        # <-- EDIT THIS: Change to the Kindle email address
    
    # Load sent files
    sent_files = load_sent_files()
    
    # Find all .epub files in the directory that haven't been sent
    epub_files = find_epub_files(directory_to_search, sent_files)
    for epub_file in epub_files:
        # Send an email with the .epub file attached
        send_email(smtp_server, port, email_login, email_password, to_email, 'EPUB File', 'Please find the attached EPUB file.', epub_file)
        print(f"Sent {epub_file}")
        # Log the sent file
        save_sent_file(epub_file)
        # Wait for 1 minute before sending the next email
        time.sleep(60)

if __name__ == "__main__":
    main()
