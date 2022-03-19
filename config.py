import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    WTF_CSRF_ENABLED = False
    JSON_ADD_STATUS = False
    STATIC_FOLDER = '/app/static'
    SQLALCHEMY_MIGRATE_REPO = "db"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gtrrrrrrrrrrrrhoniwhgt3yot587tw6y740333fr3o46ytf98h75yh'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False