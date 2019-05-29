from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from vshaurme.validators import check_passwords_rules, check_swear_usernames
from vshaurme.models import User


swear_words = ['fuck', 'shit', 'cunt', 'asshole', 'bitch', 'bint', 'xuy', 'pizda', 'ebat']


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    
class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField('Имя пользователя', validators=[DataRequired(), check_swear_usernames, 
                                                   Length(1, 20), Regexp('^[a-zA-Z0-9]*$',
                                                          message='Имя пользователя должно состоять из a-z, A-Z или 0-9.')])
    password = PasswordField('Пароль', validators=[
        DataRequired(), Length(10, 128, message='Длинна пароля должна быть не меньше 10 символов'), 
             EqualTo('password2'), check_passwords_rules])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Присоединиться')

    

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Этот email уже используется.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Это имя пользователя уже используется.')

    


class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('Подтвердить')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(), Length(10, 128, message='Длинна пароля должна быть не меньше 10 символов'), 
             EqualTo('password2')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

    def validate_password(self, field):
        if field.data.isdigit():
            raise ValidationError('Пароль не должен состоять только из цифр')
        elif field.data.isalpha():
            raise ValidationError('Пароль не должен состоять только из букв')
        elif field.data.islower():
            raise ValidationError('Пароль не должен состоять только из букв нижнего регистра')
        elif field.data.isupper():
            raise ValidationError('Пароль не должен состоять только из букв верхнего регистра')
