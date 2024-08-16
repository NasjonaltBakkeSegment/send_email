#!/usr/bin/python3
"""
Send email.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yaml
import os

def email_sender(recipients, subject, body, attachment_path=None, cc=None):
    """
    Send emails to multiple recipients.

    Args:
        recipients (list of str): List of email addresses of the recipients.
        subject (str): Subject of the email.
        body (str): Body of the email message.
        attachment_path (str): Path to the file to be attached to the email.
        cc (list of str): Optional CC recipient(s) of the email
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Construct the path to the config file
    config_path = os.path.join(script_dir, 'config.yml')

    # Load the YAML configuration file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Extract email configuration
    sender = config['email_app']['sender']
    password = config['email_app']['password']

    # Loop through recipients and send email to each
    for recipient in recipients:
        # Create a new MIMEText object for each recipient
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        # Add CC header if cc is provided
        if cc:
            msg['Cc'] = ', '.join(cc)

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            try:
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                msg.attach(part)
            except FileNotFoundError:
                print(f"Attachment file {attachment_path} not found.")
                continue

        # Send the email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, [recipient] + (cc if cc else []), msg.as_string())
                print(f"Email sent successfully to {recipient}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email to {recipient}: {e}")
