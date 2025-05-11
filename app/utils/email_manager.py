# ./app/utils/email_manager.py
from flask import render_template
from flask_mail import Message

class EmailManager:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def send_email(self, subject, recipients, template, context):
        """
        Send an email using a specified template and context.
        """
        from app.extensions import mail
        with self.app.app_context():
            # Render email body
            html_body = render_template(f"emails/{template}.html", **context)
            text_body = render_template(f"emails/{template}.txt", **context)

            # Create and send the email
            msg = Message(
                sender='<noreply@demo.com>',
                subject=subject,
                recipients=recipients,
                body=text_body,
                html=html_body,
            )
            mail.send(msg)


    def send_password_reset_email(self, recipient, fname, lname, reset_link):
        """
        Send a password reset email.
        """
        subject = "Password Reset Request"
        template = "password_reset"
        context = {
            "reset_link": reset_link,
            "user_name": f"{fname} {lname}",
        }
        self.send_email(subject, [recipient], template, context)

    