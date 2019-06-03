from flask_babel import _
from wtforms import ValidationError


def check_swear_usernames(form, field):
    swear_words = ['fuck', 'shit', 'cunt', 'asshole', 'bitch', 'bint', 'xuy', 'pizda', 'ebat']
    for word in swear_words:
        if word in field.data.lower():
            raise ValidationError(_('Имя пользователя не должно содержать бранных слов'))


def check_passwords_rules(form, field):
        if field.data.isdigit():
            raise ValidationError(_('Пароль не должен состоять только из цифр'))
        elif field.data.isalpha():
            raise ValidationError(_('Пароль не должен состоять только из букв'))
        elif field.data.islower():
            raise ValidationError(_('Пароль не должен состоять только из букв нижнего регистра'))
        elif field.data.isupper():
            raise ValidationError(_('Пароль не должен состоять только из букв верхнего Регистра'))