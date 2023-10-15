from flask_mail import Message
from flask import current_app
from backend import mail
from database.config_db import Config as cfg
import threading

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_with_app_context(to, subject, template="No content"):
    app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    a = threading.Thread(target=send_email, args=[app, msg])
    a.start()
