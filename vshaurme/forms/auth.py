from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from vshaurme.validators import check_passwords_rules, check_swear_usernames
from vshaurme.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Запомнить меня'))
    submit = SubmitField(_l('Войти'))

    
class RegisterForm(FlaskForm):
    name = StringField(_l('Имя'), validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField(_l('Имя пользователя'), validators=[DataRequired(), check_swear_usernames, 
                                                   Length(1, 20), Regexp('^[a-zA-Z0-9]*$',
                                                          message=_l('Имя пользователя должно состоять из a-z, A-Z или 0-9.'))])
    password = PasswordField(_l('Пароль'), validators=[
        DataRequired(), Length(10, 128, message=_l('Длина пароля должна быть не меньше 10 символов')), 
             EqualTo('password2'), check_passwords_rules])
    password2 = PasswordField(_l('Подтвердите пароль'), validators=[DataRequired()])
    recaptcha = RecaptchaField('Подтвердите, что вы не робот')
    submit = SubmitField(_l('Присоединиться'))

    

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_('Этот email уже используется.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_('Это имя пользователя уже используется.'))

    


class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField(_l('Подтвердить'))


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField(_l('Пароль'), validators=[
        DataRequired(), Length(10, 128, message=_l('Длина пароля должна быть не меньше 10 символов')), 
             EqualTo('password2'), check_passwords_rules])
    password2 = PasswordField(_l('Подтвердите пароль'), validators=[DataRequired()])
    submit = SubmitField(_l('Подтвердить'))
