
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from ..models import User, Role
from .. import users_upload


class EditProfileForm(FlaskForm):
    avatar = FileField('', validators=[FileAllowed(users_upload, message='Только изображения')])
    background = FileField('', validators=[FileAllowed(users_upload, message='Только изображения')])
    location = StringField('Место проживания: ', validators=[Length(0, 64)])
    name = StringField('Имя', validators=[Length(0, 64)])
    site = StringField('Сайт: ', validators=[Length(0, 64)])
    about_me = TextAreaField('О себе: ')
    submit = SubmitField('Изменить')

class EditProfileAdminForm(FlaskForm):
    avatar = FileField('', validators=[FileAllowed(users_upload, message='Только изображения')])
    background = FileField('', validators=[FileAllowed(users_upload, message='Только изображения')])
    email = StringField('Почта', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Никнейм', validators=[
        DataRequired(), Length(1, 64)], id='tags-tokenfield')
    confirmed = BooleanField('Подтвержден')
    role = SelectField('Роль', coerce=int)
    location = StringField('Место проживания: ', validators=[Length(0, 64)])
    name = StringField('Имя', validators=[Length(0, 64)])
    site = StringField('Сайт: ', validators=[Length(0, 64)])
    about_me = TextAreaField('О себе: ')
    submit = SubmitField('Изменить')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Почта уже занята.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Имя пользователя уже занято.')