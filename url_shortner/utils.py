import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import request, jsonify
from models.auth import User
import jwt

from constants import *
from app import app


def standard_400_return(err):
    return jsonify(
        {
            STATUS_KEY: STATUS_FAILURE_VALUE,
            STATUS_MESSAGE_KEY: str(err),
            STATUS_CODE: 400,
        }
    )


def standard_500_return(err):
    return jsonify(
        {
            STATUS_KEY: STATUS_FAILURE_VALUE,
            STATUS_MESSAGE_KEY: str(err),
            STATUS_CODE: 500,
        }
    )


def standard_200_data_return(data, message=None):
    return jsonify(
        {
            STATUS_KEY: STATUS_SUCCESS_VALUE,
            DATA_KEY: data,
            **({MESSAGE_KEY: message} if message else {}),
            STATUS_CODE: 200,
        }
    )


def standard_200_message_return(message):
    return jsonify(
        {
            STATUS_KEY: STATUS_SUCCESS_VALUE,
            MESSAGE_KEY: message,
            STATUS_CODE: 200,
        }
    )


def standard_404_return(err):
    return jsonify(
        {
            STATUS_KEY: STATUS_FAILURE_VALUE,
            STATUS_MESSAGE_KEY: str(err),
            STATUS_CODE: 404,
        }
    )


def db_session():
    try:
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        session = sessionmaker(engine)()
        return session
    except Exception as e:
        raise ("Could not generate db session")


def token_required(flask_fn):
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print("token", token)
        else:
            return (
                standard_400_return("Header 'Authorization' is missing !!"),
                400,
            )
        if not token:
            return standard_400_return("Token is missing !!"), 401

        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.filter_by(id=data["public_id"]).first()
        except Exception as err:
            # TODO: Add logger
            print(err.__class__, str(err))
            return standard_400_return("Token is invalid !!"), 401
        return flask_fn(current_user, *args, **kwargs)

    # REF: https://stackoverflow.com/a/42254713
    wrapper.__name__ = flask_fn.__name__
    return wrapper


def generate_random_string(length=8):
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
