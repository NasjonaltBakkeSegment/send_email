#!/usr/bin/python3
"""
Send email.
"""

import smtplib
from email.message import EmailMessage

def send_email(recipients, subject, message, sender='nbs-helpdesk@met.no', server="127.0.0.1", attachment_path=None):
    """
    Send emails to multiple recipients.

    Args:
        recipients (list of dict): List of dictionaries representing recipients.
            Each dictionary should contain 'name' and 'email' keys.
        subject (str): Subject of the email.
        message (str): Body of the email message.
            'Hi {recipient.name}' is added within so don't include greetings in the message body
        sender (str, optional): Sender's email address. Defaults to 'nbs-helpdesk@met.no'.
        server (str, optional): SMTP server address. Defaults to '127.0.0.1'.
    """
    for recipient in recipients:
        assert isinstance(recipient, dict)

        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = recipient['email']
        msg['Subject'] = subject

        # Adding recipient's name to the beginning of the message
        message_with_name = f"Hi {recipient['name']},\n\n{message}"
        msg.set_content(message_with_name)

        # Adding attachment if provided
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                attachment_content = attachment.read()
                attachment_filename = attachment_path.split('/')[-1]  # Extracting filename from path
                msg.add_attachment(attachment_content, maintype='application', subtype='octet-stream', filename=attachment_filename)

        smtp = smtplib.SMTP(server)
        smtp.send_message(msg)
        smtp.quit()
