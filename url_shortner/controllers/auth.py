from app import app
from flask import jsonify

from models.auth import User
from utils import (
    db_session,
    standard_200_message_return,
    standard_200_data_return,
    standard_400_return,
    standard_404_return,
    # standard_500_return,
)
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from flask import Blueprint, request


# auth_bp = Blueprint('auth', __name__)


@app.route("/sign-in/", methods=["POST"])
def login_user():
    session = db_session()
    try:
        data = request.get_json()
        password = data["password"]
        email = data["email"]
        if not password:
            raise ValueError("Password is required")
        if not email:
            raise ValueError("Email is required")
        user = session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode(
                    {"public_id": user.id, "email": user.email},
                    app.config["SECRET_KEY"],
                )
                response = standard_200_data_return(
                    {"token": token, "status": 200}
                )
            else:
                response = (
                    standard_400_return("Password is wrong. Please try again!"),
                    400,
                )

        else:
            response = (
                standard_404_return(
                    "User not found with this email and password. "
                ),
                404,
            )
    except ValueError as err:
        response = standard_400_return(err), 400
    finally:
        if session:
            session.close()
    return response


@app.route("/sign-up/", methods=["POST"])
def signup_user():
    session = db_session()
    try:
        print(request.get_json())
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        if not name:
            raise ValueError("Name is required to signup")
        if not password:
            raise ValueError("Password is required to signup")
        if not email:
            raise ValueError("Email is required to signup")
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                name=name,
                password=generate_password_hash(password),
                email=email,
            )
            session.add(user)
            session.commit()
            response = (
                standard_200_message_return(
                    "User created successfully. Please login!"
                ),
                200,
            )
        else:
            response = (
                standard_400_return(
                    "User already exists. Please try signing in!"
                ),
                400,
            )
    except ValueError as err:
        response = standard_400_return(err), 400
    # except Exception as err:
    #     response = standard_500_return(err), 500
    finally:
        if session:
            session.close()
    return response
