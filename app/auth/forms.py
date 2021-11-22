from app import db
from app.models import User
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(message='Поле пустое!'), Length(1, 64), Email(message='Неверный формат почты')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Поле пустое!'), Length(1, 32)])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(message='Поле пустое!'), Length(1, 64), Email(message='Неверный формат почты')])
    username = StringField('Никнейм', validators=[
        DataRequired(), Length(1, 64)])

    password = PasswordField('Пароль',
                             validators=[DataRequired(message='Поле пустое!'), EqualTo('password2', message='Пароли не совпадают'),
                                         Length(1, 32)])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired(message='Поле пустое!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Почта уже используется')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Никнейм занят')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать.')])
    password2 = PasswordField('Повторить пароль',
                              validators=[DataRequired()])
    submit = SubmitField('Обновить пароль')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Отправить письмо')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), EqualTo('password2', message='PПароли должны совпадать')])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired()])
    submit = SubmitField('Установить пароль')


class ChangeEmailForm(FlaskForm):
    email = StringField('Новая почта', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Почта уже занята.')