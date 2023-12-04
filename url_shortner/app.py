import logging
from datetime import datetime
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import Config

app = Flask(__name__)


class RequestLoggerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with app.request_context(environ):
            ip_address = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.logger.info(
                f"IP: {ip_address}, User Agent: {user_agent}, Time: {timestamp}"
            )

        return self.app(environ, start_response)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.wsgi_app = RequestLoggerMiddleware(app.wsgi_app)

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)


from models import *

with app.app_context():
    db.create_all()
