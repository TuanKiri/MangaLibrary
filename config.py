import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'very secret key')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES', True) 
    MANGA_ADMIN = os.environ.get('MANGA_ADMIN', 'admin@mail.ru')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.yandex.ru')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MANGA_MAIL_SUBJECT_PREFIX = os.environ.get('MANGA_MAIL_SUBJECT_PREFIX', '[MangaLibrary]')
    MANGA_MAIL_SENDER = os.environ.get('MANGA_MAIL_SENDER', 'MangaLibrary <mangalibrary@example.com>')

    # 50 megabytes
    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH', 50 * 1000 * 1000)

    USER_FOLLOWERS_PER_PAGE = os.environ.get('USER_FOLLOWERS_PER_PAGE', 10)
    USER_COMMENTS_PER_PAGE = os.environ.get('USER_COMMENTS_PER_PAGE', 10)
    USER_LIST_PER_PAGE = os.environ.get('USER_LIST_PER_PAGE', 10)
    MANGA_LIST_PER_PAGE = os.environ.get('MANGA_LIST_PER_PAGE', 10)
    MANGA_COMMENTS_PER_PAGE = os.environ.get('MANGA_COMMENTS_PER_PAGE', 10)
    NEWS_LIST_PER_PAGE = os.environ.get('NEWS_LIST_PER_PAGE', 10)
    TAGS_LIST_PER_PAGE = os.environ.get('TAGS_LIST_PER_PAGE', 100)

    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest@rabbitmq//')
    CELERY_BACKEND_URL = os.environ.get('CELERY_BACKEND_URL', 'db+sqlite:///' + os.path.join(basedir, 'task.sqlite'))
    CELERY_ROUTES = os.environ.get('CELERY_ROUTES', {'task.email.*': {'queue': 'email'}})

    SERVER_NAME = os.environ.get('SERVER_NAME', '127.0.0.1:5000')

    UPLOADS_AUTOSERVE = os.environ.get('UPLOADS_AUTOSERVE', True)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG', True)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or \
        os.path.join(basedir, 'upload-dev/')


class TestingConfig(Config):
    TESTING = os.environ.get('TESTING', True)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite://'
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload-test/')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or \
        os.path.join(basedir, 'upload/')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
