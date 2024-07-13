import os
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Initialize Celery
celery = Celery('mails', broker='pyamqp://myuser:mypassword@35.171.162.220//')

@celery.task
def send_email(recipient):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText('This is a test email.')
    msg['Subject'] = 'Test Email'
    msg['From'] = 'sample@gmail.com'
    msg['To'] = recipient

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login('sample@gmail.com', 'password')  # Log in to your Gmail account
            server.sendmail(msg['From'], [msg['To']], msg.as_string())  # Send the email
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

send_email('sample@gmail.com')

@celery.task
def log_time():
    with open('/var/log/messaging_system.log', 'a') as f:
        f.write(f'{datetime.now()}\n')
