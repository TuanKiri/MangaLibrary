import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True 
    MANGA_ADMIN = 'admin@mail.ru'

    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #     ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MANGA_MAIL_SUBJECT_PREFIX = '[MangaLibrary]'
    # MANGA_MAIL_SENDER = 'MangaLibrary Admin <mangalibrary@example.com>'

    # 50 megabytes
    MAX_CONTENT_LENGTH = 50 * 1000 * 1000

    USER_FOLLOWERS_PER_PAGE = 10
    USER_COMMENTS_PER_PAGE = 10
    USER_LIST_PER_PAGE = 10
    MANGA_LIST_PER_PAGE = 10
    MANGA_COMMENTS_PER_PAGE = 10
    NEWS_LIST_PER_PAGE = 10
    TAGS_LIST_PER_PAGE = 100
    RECAPTCHA_PUBLIC_KEY = 'public key'
    RECAPTCHA_PRIVATE_KEY = 'secret key'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload-dev/')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload-test/')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload/')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
