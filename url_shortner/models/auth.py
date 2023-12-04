from app import db

from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column


class User(db.Model):
    # __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    email = mapped_column(String, unique=True)
    password = mapped_column(String)
    created_at = mapped_column(DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
