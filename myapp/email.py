from threading import Thread
from flask import render_template
from flask_mail import Message
from myapp import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, recipients=recipients, body=text_body, html=html_body,sender=sender)
    Thread(target=send_async_email,args=(app,msg)).start()

def send_email_reset_password(user):
    token = user.get_reset_password_token()
    subject = "[Microblog] Reset Your Password"
    sender = app.config["ADMINS"][0]
    recipients = [user.email]
    text_body = render_template("email/reset_password.txt",user=user, token=token)
    html_body = render_template("email/reset_password.html",user=user, token=token)
    
    send_email(subject=subject, sender=sender, recipients=recipients, text_body=text_body, html_body=html_body)
