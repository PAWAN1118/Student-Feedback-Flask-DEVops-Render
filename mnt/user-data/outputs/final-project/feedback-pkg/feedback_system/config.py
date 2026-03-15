import os


class Config:
    SECRET_KEY  = os.environ.get('SECRET_KEY',  'dev-secret-change-in-production')
    DB_PATH     = os.environ.get('DB_PATH',     os.path.join(os.getcwd(), 'feedback.db'))
    PER_PAGE    = int(os.environ.get('PER_PAGE', 6))
    HOST        = os.environ.get('HOST',        '0.0.0.0')
    PORT        = int(os.environ.get('PORT',    5000))
    DEBUG       = os.environ.get('DEBUG',       'false').lower() == 'true'
    APP_NAME    = os.environ.get('APP_NAME',    'Student Feedback System')
    APP_TAGLINE = os.environ.get('APP_TAGLINE', 'Academic Excellence Portal')


class DevelopmentConfig(Config):
    DEBUG   = True
    DB_PATH = os.path.join(os.getcwd(), 'feedback_dev.db')


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DB_PATH = ':memory:'


config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     Config,
}
