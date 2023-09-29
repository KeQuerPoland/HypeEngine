from flask_mail import Message
from backend import mail
from config import Config

def send(title,recipient,author,html=None):
    msg = Message(title,
        sender=author+"@"+Config.MAIL_SERVER_DOMAIN,
        recipients=recipient
    )

    if not html == None:
        msg.html = html

    return mail.send(msg)