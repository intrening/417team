from threading import Thread

from flask import current_app, render_template
from flask_babel import lazy_gettext as _l
from flask_mail import Message

from vshaurme.extensions import mail


def send_mail(to, subject, template, user, token):
    message = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to],
        html=render_template(template, user=user, token=token)
    )
    mail.send(message)


def send_confirm_email(user, token, to=None):
    send_mail(subject=_l('Подтверждение Email'), to=to or user.email, template='emails/confirm.html', user=user, token=token)


def send_reset_password_email(user, token):
    send_mail(subject=_l('Смена пароля'), to=user.email, template='emails/reset_password.html', user=user, token=token)


def send_change_email_email(user, token, to=None):
    send_mail(subject=_l('Изменение Email'), to=to or user.email, template='emails/change_email.html', user=user, token=token)
