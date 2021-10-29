from .. import db, limiter
from . import auth
from ..models import User, Ban
from ..email import send_email
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from .forms import LoginForm, RegistrationForm, ChangeEmailForm, \
                    ChangePasswordForm, PasswordResetRequestForm, \
                    PasswordResetForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit('6/hour', methods=['POST'],
               error_message="Вы пытаетесь войти в систему слишком много раз, повторите попытку через час.")
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data.lower()).first()
        if user is not None and user.verify_password(login_form.password.data):
            if user.banned:
                reason = Ban.query.filter_by(user_id=user.id).first().reason
                flash(f'Ошибка входа! Вы заблокированы по причине: "{reason}". '
                        'Если вы считаете, что это ошибка, свяжитесь с администратором.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, login_form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Неверный логин или пароль!', 'danger')
    return render_template('login.html', login_form=login_form, title="Вход")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(email=registration_form.email.data.lower(),
                password=registration_form.password.data,
                username=registration_form.username.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        # send_email(user.email, 'Подтверждение аккаунта',
        #             'email/confirm', user=user, token=token)
        flash('Письмо с подтверждением было отправлено вам по электронной почте.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register.html', registration_form=registration_form, title="Регистрация")


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Подтверждение аккаунта',
               'email/confirm', user=current_user, token=token)
    flash('Вам было отправлено новое письмо с подтверждением по электронной почте.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Вы подтвердили аккаунт. Благодарим!', 'info')
    else:
        flash('Ссылка для подтверждения недействительна или срок ее действия истек.', 'warning')
    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    change_email_form = ChangeEmailForm()
    if change_email_form.validate_on_submit():
        if current_user.verify_password(change_email_form.password.data):
            new_email = change_email_form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Подтверждение почты',
                        'email/change_email',
                        user=current_user, token=token)
            flash('Вам было отправлено письмо с инструкциями для подтверждению вашего нового адреса электронной почты.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль.', 'danger')
    return render_template('change_email.html', change_email_form=change_email_form, title="Смена почты")


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Ваша почта была обновлена.', 'info')
    else:
        flash('Неверный запрос.', 'danger')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        if current_user.verify_password(change_password_form.old_password.data):
            current_user.password = change_password_form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Ваш пароль обновлен.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный запрос.', 'danger')
    return render_template('change_password.html', change_password_form=change_password_form, title="Смена пароля")
    

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    password_reset_request_form = PasswordResetRequestForm()
    if password_reset_request_form.validate_on_submit():
        user = User.query.filter_by(email=password_reset_request_form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Сброс пароля',
                        'email/reset_password',
                        user=user, token=token)
        flash('Письмо с инструкциями по сбросу пароля было отправлено вам на почту.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('password_reset_request.html', password_reset_request_form=password_reset_request_form, title="Обновление пароля")


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    password_reset_form = PasswordResetForm()
    if password_reset_form.validate_on_submit():
        if User.reset_password(token, password_reset_form.password.data):
            db.session.commit()
            flash('Ваш пароль был обновлен.', 'info')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('password_reset.html', password_reset_form=password_reset_form, title="Обновление пароля")