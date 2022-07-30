import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from myapp import app

application_logging_level = logging.INFO

class SMTPLogging:
    def __init__(self):
    
        self.mail_subject = "Important error"
        
        self.auth = None
        if app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
            self.auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

        self.secure = None
        if app.config["MAIL_USE_TLS"]:
            self.secure = ()

    def __enter__(self):
        self.mail_handler = SMTPHandler(mailhost=(app.config["MAIL_SERVER"],app.config["MAIL_PORT"]),fromaddr="np-reply@"+app.config["MAIL_SERVER"],
        toaddrs=app.config["ADMINS"],subject=self.mail_subject,credentials=self.auth,secure=self.secure)
        
        return self.mail_handler
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.mail_handler.setLevel(logging.ERROR)


class RotatingFileLogger:
    def __init__(self):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        self.formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'
        )
        self.filename='logs/microblog.log'
        self.maxbyte = 10*1024 # 10KBytes
        self.backupcount = 10
    
    def __enter__(self):
        self.filehandler = RotatingFileHandler(filename=self.filename,maxBytes=self.maxbyte,backupCount=self.backupcount)
        return self.filehandler
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.filehandler.setFormatter(self.formatter)
        self.filehandler.setLevel(logging.INFO)


if not app.debug:
    
    if app.config["MAIL_SERVER"]:
        with SMTPLogging() as smtpLogging:
            app.logger.addHandler(smtpLogging)
       
    with RotatingFileLogger() as rotatingFileLogger:
        app.logger.addHandler(rotatingFileLogger)    
        
    app.logger.setLevel(application_logging_level)
    app.logger.info("Microblog startup")