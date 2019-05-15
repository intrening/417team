from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp

from vshaurme.models import User


class EditProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(1, 30)])
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='Имя пользователя может содержать только a-z, A-Z и 0-9.')])
    website = StringField('Вебсайт', validators=[Optional(), Length(0, 255)])
    location = StringField('Город', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('О себе', validators=[Optional(), Length(0, 120)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Такое имя пользователя уже занято.')


class UploadAvatarForm(FlaskForm):
    image = FileField('Загрузить', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Файл должен быть формата .jpg или .png.')
    ])
    submit = SubmitField()


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Обрезать и обновить')


class ChangeEmailForm(FlaskForm):
    email = StringField('Новый Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Такой email уже используется.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField()


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('Новый комментарий')
    receive_follow_notification = BooleanField('Новый подписчик')
    receive_collect_notification = BooleanField('Новый коллекционер')
    submit = SubmitField()


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('Публиковать мои коллекции')
    submit = SubmitField()


class DeleteAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('Неверное имя пользователя.')
