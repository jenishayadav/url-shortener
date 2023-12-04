import os

from app import app
from controllers import *
from models import *

if __name__ == "__main__":
    environment = os.environ.get("FLASK_ENV", "development")
    app.run(debug=environment == "development", host="0.0.0.0", port=5000)
