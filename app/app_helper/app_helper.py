from datetime import timedelta
import os
from flask import Flask


class AppHelper:
    def __init__(self, app: Flask):
        self.__app = app

    def config(self, db_url=None):
        self.__app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
        self.__app.config["PROPAGATE_EXCEPTIONS"] = True
        self.__app.config["API_VERSION"] = "1.0.0"
        self.__app.config["API_TITLE"] = "Little Talk API"
        self.__app.config["OPENAPI_VERSION"] = "3.0.3"

        self.__app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 280,
            "pool_timeout": 5
        }
        self.__app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
        self.__app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.__app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        self.__app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=15)
        self.__app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        self.__app.config['JWT_TOKEN_LOCATION'] = ['headers']