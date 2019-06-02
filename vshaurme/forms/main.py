from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class DescriptionForm(FlaskForm):
    description = TextAreaField(_l('Описание'), validators=[Optional(), Length(0, 500)])
    submit = SubmitField(_l('Подтвердить'))


class TagForm(FlaskForm):
    tag = StringField(_l('Добавить теги (используйте пробел для разделения)'), validators=[Optional(), Length(0, 64)])
    submit = SubmitField(_l('Подтвердить'))


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField(_l('Опубликовать'))
