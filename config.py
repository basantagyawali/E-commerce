import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
     #mysql://username:password@server/db
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://login:pass@localhost/flask_app'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #location for photo upload 
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images')
