from functools import cache
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import Length, DataRequired, Regexp
from flask_wtf.file import FileField, FileAllowed, file_required
from .. import manga_upload
from ..models import Manga
from wtforms import ValidationError


class AddMangaForm(FlaskForm):
    image = FileField('', validators=[FileAllowed(manga_upload, message='Только изображения')])
    title = StringField('Название',
                        validators=[DataRequired(message="Поле пусто!"), Length(1, 128, message='От 1 до 128 символов длиной')])
    author = StringField('Автор', validators=[Length(0, 64, message='От 0 до 64 символов длиной')])
    tags = StringField('Теги')
    catalog = TextAreaField('Описание')
    submit = SubmitField()

    def validate_title(self, field):
        if Manga.query.filter_by(title=field.data).first():
            raise ValidationError('Манга существует.')


class EditMangaForm(AddMangaForm):
    def __init__(self, manga, *args, **kwargs):
        super(EditMangaForm, self).__init__(*args, **kwargs)
        self.manga = manga

    def validate_title(self, field):
        if field.data != self.manga.title and \
                Manga.query.filter_by(title=field.data).first():
            raise ValidationError('Манга существует.')


class EditChapterForm(FlaskForm):
    volume = StringField('Том', validators=[Length(1, 32, message='От 1 до 32 символов длиной'), 
                                            Regexp('^[0-9]*$', 0, 'Только цифры!')])
    chapter = StringField('Глава', validators=[Length(1, 32, message='От 1 до 32 символов длиной'),
                                                Regexp('^[0-9]*$', 0, 'Только цифры!')])
    title = StringField('Название',
                        validators=[Length(0, 128, message='До 128 символов длиной')])
    image = MultipleFileField('', id="formFileMultiple", validators=[file_required(message='Изображения не загружены!'), 
                                                                    FileAllowed(manga_upload, message='Только изображения!')])
    submit = SubmitField('Добавить')

class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField('Искать')


