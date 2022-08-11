import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # FLASK
    FLASK_APP = os.environ.get("FLASK_APP") or "microblog.py"

    FLASK_ENV = os.environ.get("FLASK_ENV") or "development"

    FLASK_DEBUG = 0

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # FLASK_SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False

    SQLALCHEMY_ECHO = True

    # Email
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25) 
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
    # Admin
    ADMINS = ["mohammad.rouzegar78@gmail.com"]

    # Page Number
    POSTS_PER_PAGE = 10
