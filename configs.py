import os

class Config(object):
    SECRET_KEY = 'ronaldocepeda23'

class DevelomentConfig(Config):
    DEBUG = True
    