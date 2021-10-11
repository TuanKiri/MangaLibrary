from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed


class NewsForm(FlaskForm):
    title = StringField('Название',
                        validators=[DataRequired(message="Поле пусто!"), Length(1, 128, message='От 1 до 128 символов длиной')])
    news = TextAreaField('Новость',
                        validators=[DataRequired(message='Содержание не должно быть пустым'), Length(1, 1024, message='Длина новости ограничена 1024 символами.')])
    image = MultipleFileField('', id="formFileMultiple", validators=[FileAllowed('avatars', message='Только изображения')])
    submit = SubmitField('Опубликовать')

class SearchForm(FlaskForm):
    search = StringField('Поиск:', validators=[Length(0, 64)])
    submit = SubmitField('Искать')


