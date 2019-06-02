from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp

from vshaurme.models import User
from vshaurme.validators import check_passwords_rules


class EditProfileForm(FlaskForm):
    name = StringField(_l('Имя'), validators=[DataRequired(), Length(1, 30)])
    username = StringField(_l('Имя пользователя'), validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message=_l('Имя пользователя может содержать только a-z, A-Z и 0-9.'))])
    website = StringField(_l('Вебсайт'), validators=[Optional(), Length(0, 255)])
    location = StringField(_l('Город'), validators=[Optional(), Length(0, 50)])
    bio = TextAreaField(_l('О себе'), validators=[Optional(), Length(0, 120)])
    submit = SubmitField(_l('Сохранить'))

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError(_('Такое имя пользователя уже занято.'))


class UploadAvatarForm(FlaskForm):
    image = FileField(_l('Загрузить'), validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], _l('Файл должен быть формата .jpg или .png.'))
    ])
    submit = SubmitField(_l('Сохранить'))


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField(_l('Обрезать и обновить'))


class ChangeEmailForm(FlaskForm):
    email = StringField(_l('Новый Email'), validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField(_l('Сохранить'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_('Такой email уже используется.'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_l('Старый пароль'), validators=[DataRequired()])
    password = PasswordField(_l('Пароль'), validators=[
        DataRequired(), Length(10, 128, message=_l('Длина пароля должна быть не меньше 10 символов')), 
             EqualTo('password2'), check_passwords_rules])
    password2 = PasswordField(_l('Подтвердите пароль'), validators=[DataRequired()])
    submit = SubmitField(_l('Сохранить'))


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField(_l('Новый комментарий'))
    receive_follow_notification = BooleanField(_l('Новый подписчик'))
    receive_collect_notification = BooleanField(_l('Новый коллекционер'))
    submit = SubmitField(_l('Сохранить'))


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField(_l('Публиковать мои коллекции'))
    submit = SubmitField(_l('Сохранить'))


class DeleteAccountForm(FlaskForm):
    username = StringField(_l('Имя пользователя'), validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField(_l('Подтвердить'))

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError(_('Неверное имя пользователя.'))
