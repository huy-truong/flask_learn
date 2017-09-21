from . import mail
from flask_mail import Message

def sendmail():
    msg = Message('Send mail testing',sender='truonghuy1801@gmail.com',
            recipients=['truonghuy1801@gmail.com'],body = 'Congratulation, sending is ok')

    mail.send(msg)
    return "Mail sent"


