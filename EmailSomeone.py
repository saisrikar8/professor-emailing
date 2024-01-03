import ssl
from email.message import EmailMessage
import smtplib

from Attachment import Attachment

class EmailSender:
    user = ''
    password = ''
    domain = ''
    servers = {
        'icloud.com': 'smtp.mail.me.com',
        'outlook.com': 'smtp-mail.outlook.com',
        'hotmail.com': 'smtp-mail.outlook.com',
        'gmail.com': 'smtp.gmail.com',
        'yahoo.com': 'smtp.mail.yahoo.com',
        'aol.com': 'smtp.aol.com',
    }
    server = ''
    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.domain = self.user.split('@')[1]
        self.server = self.servers[self.domain]


    def send_email(self, text, subject, receiving_addresses: list | str, attachments=tuple()):
        print('Starting email process')
        print('Generating Email Message format...')
        message = EmailMessage()
        message['Subject'] = subject
        message['To'] = receiving_addresses
        message['From'] = self.user
        message.set_content(text)
        print('Successfully generated!')
        print('Attaching files...')
        for attachment in attachments:
            print(attachment)
            attachmentObj = Attachment(attachment)
            message.add_attachment(attachmentObj.content, maintype = 'application', subtype = 'octet-stream', filename = attachmentObj.filename)
        print('Loaded attachments!')
        print('Connecting to the server...')
        connection = smtplib.SMTP(self.server, 587)
        print('Connected to port 587!')
        print('Executing StartTLS protocol...')
        connection.starttls(context = ssl.create_default_context())
        print('Successfully executed StartTLS protocol!')
        print('Logging in to the server...')
        connection.login(self.user, self.password)
        print('Logged in!')
        print('Sending...')
        connection.send_message(message, self.user, receiving_addresses)
        print("Sent!")
        connection.quit()