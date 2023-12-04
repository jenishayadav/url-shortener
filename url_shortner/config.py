import os

for k, v in os.environ.items():
    if k.lower().startswith("postgres"):
        print("[DEBUG] ENV", k, v)


class Config:
    """Configuration class for application settings."""

    _db_host = os.environ.get("POSTGRES_HOST", "localhost")
    _db_port = os.environ.get("POSTGRES_PORT", "5432")
    _db_name = os.environ.get("POSTGRES_DB", "postgres")
    _db_user = os.environ.get("POSTGRES_USER", "postgres")
    _db_password = os.environ.get("POSTGRES_PASSWORD", "password")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "3d6f45a5fc12445dbac2f59c3b6c7cb1"
    )
