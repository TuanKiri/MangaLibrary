from app import celery
from .email import send_email
from .models import User

@celery.task(bind=True, name='task.email.confirm', ignore_result=True, max_retries=3)
def send_confirmation_token(self, user_id, **kwargs):
    user = User.query.get(user_id)
    if user:
        token = user.generate_confirmation_token()
        try:
            send_email(user.email, 'Подтверждение аккаунта',
                        'email/confirm', user=user, token=token)
        except Exception as exc:
             raise self.retry(exc=exc, countdown= 2 * 60)

@celery.task(bind=True, name='task.email.change_email', ignore_result=True, max_retries=3)
def send_change_email(self, user_id, new_email, **kwargs):
    user = User.query.get(user_id)
    if user:
        token = user.generate_email_change_token(new_email)
        try:
            send_email(new_email, 'Подтверждение почты',
                        'email/change_email', user=user, token=token)
        except Exception as exc:
             raise self.retry(exc=exc, countdown= 2 * 60)

@celery.task(bind=True, name='task.email.password_reset', ignore_result=True, max_retries=3)
def send_password_reset(self, user_id, **kwargs):
    user = User.query.get(user_id)
    if user:
        token = user.generate_reset_token()
        try:
            send_email(user.email, 'Сброс пароля',
                        'email/reset_password', user=user, token=token)
        except Exception as exc:
             raise self.retry(exc=exc, countdown= 2 * 60)