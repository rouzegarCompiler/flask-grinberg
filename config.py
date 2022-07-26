import os

class Config(object):
    FLASK_APP = os.environ.get("FLASK_APP") or "microblog.py"

    FLASK_ENV = os.environ.get("FLASK_ENV") or "development"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
