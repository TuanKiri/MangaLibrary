from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField, FileAllowed
from .. import manga_upload
from ..models import Manga
from wtforms import ValidationError

class EditMangaForm(FlaskForm):
    image = FileField('', validators=[FileAllowed(manga_upload, message='Только изображения')])
    title = StringField('Название',
                        validators=[DataRequired(message="Поле пусто!"), Length(1, 128, message='От 1 до 128 символов длиной')])
    author = StringField('Автор', validators=[Length(0, 64, message='От 0 до 64 символов длиной')])
    tags = StringField('Теги')
    catalog = TextAreaField('Описание')
    submit = SubmitField()

    def validate_username(self, field):
        if Manga.query.filter_by(title=field.data).first():
            raise ValidationError('Манга существует.')

class EditChapterForm(FlaskForm):
    volume = StringField('Том', validators=[Length(1, 32, message='От 1 до 32 символов длиной')])
    chapter = StringField('Глава', validators=[Length(1, 32, message='От 1 до 32 символов длиной')])
    title = StringField('Название',
                        validators=[Length(0, 128, message='До 128 символов длиной')])
    image = MultipleFileField('', id="formFileMultiple", validators=[FileAllowed(manga_upload, message='Только изображения')])
    submit = SubmitField('Добавить')

class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField('Искать')


