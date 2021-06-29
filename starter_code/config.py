import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Shosho11@localhost:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False

