from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class CommentForm(FlaskForm):
    comment = TextAreaField('Комментарий',
                            validators=[DataRequired(message='Содержание не должно быть пустым'), Length(1, 1024, message='Длина комментария на манги ограничена 1024 символами.')])
    submit = SubmitField('Отправить')
