import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://setty_owner:2VRYFE5SBkzT@ep-gentle-bird-a2b33gnf.eu-central-1.aws.neon.tech/setty?sslmode=require'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://setty_owner:2VRYFE5SBkzT@ep-gentle-bird-a2b33gnf.eu-central-1.aws.neon.tech/setty?sslmode=require'
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE') or 'redis://'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}