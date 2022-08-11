from flask import Flask
import logging
from logging.handlers import SMTPHandler
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap5
from flask_moment import Moment


app = Flask(__name__)
app.app_context
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
mail = Mail(app)
bootstrap = Bootstrap5(app)
moment = Moment(app)

from myapp import routes, models, errors , logger
