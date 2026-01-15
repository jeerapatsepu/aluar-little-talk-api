from flask import Flask
from flask_migrate import Migrate
from app.app_helper.api_helper import APIHelper
from app.app_helper.app_helper import AppHelper
from app.app_helper.jwt_helper import JWTHelper
from app.extensions import db, bcrypt

def create_app() -> Flask:
    app = Flask(__name__)
    AppHelper(app).config()
    JWTHelper(app).register_callback()
    APIHelper(app).register_blueprint()

    db.init_app(app)
    with app.app_context():
        db.create_all()

    bcrypt.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    return app