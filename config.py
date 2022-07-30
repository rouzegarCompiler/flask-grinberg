import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # FLASK
    FLASK_APP = os.environ.get("FLASK_APP") or "microblog.py"

    FLASK_ENV = os.environ.get("FLASK_ENV") or "development"

    FLASK_DEBUG = int(os.environ.get("FLASK_DEBUG")) or 1

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # FLASK_SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")) or False

    SQLALCHEMY_ECHO = bool(os.environ.get("SQLALCHEMY_ECHO")) or False