from datetime import datetime
from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column

from app import db
from constants import SCHEMA
from .auth import User


class URLMapper(db.Model):
    # __tablename__ = "url_mapper"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    long_url = mapped_column(String)
    url_key = mapped_column(String, index=True)
    user_id = mapped_column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
    )
    created_at = mapped_column(DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    usage_limit = mapped_column(Integer, nullable=True, default=None)
    hit_count = mapped_column(Integer, default=0)
    expiry_datetime = mapped_column(DateTime, nullable=True)
