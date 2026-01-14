import os
from datetime import timedelta

def config(app, db_url):
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_VERSION"] = "v1"
    app.config["API_TITLE"] = "Log API"
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_timeout": 5
    }
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['headers']