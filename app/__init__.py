from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.app_jwt import handle_jwt
from app.blueprint_manager import register_blueprint
from app.app_config import config
from app.shared import db, bcrypt

def create_app(db_url=None) -> Flask:
    load_dotenv()

    app = Flask(__name__)
    config(app, db_url)
    handle_jwt(app)
    register_blueprint(app)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    return app