from flask_mail import Message
from backend import mail
from backend.database.config_db import Config as cfg

def send(title,recipient,author,html=None):
    msg = Message(title,
        sender=author+"@"+cfg.get_by_name('MAIL_SERVER_DOMAIN'),
        recipients=recipient
    )

    if not html == None:
        msg.html = html

    return mail.send(msg)