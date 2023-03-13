from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))  # Real path to backend


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        'SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(BASE_DIR, 'dev.db')  # Path concatenation
    DEBUG = True  # Automatic server reloading
    SQLALCHEMY_ECHO = True  # Generated SQL commands after database comments


class ProdConfig(Config):
    pass


class TestConfig(Config):
    pass
