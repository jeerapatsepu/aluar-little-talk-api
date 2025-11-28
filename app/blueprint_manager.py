from flask_smorest import Api
from resources.auth.auth_create.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_login import blp as AuthLoginBlueprint
from resources.home.home import blp as HomeBlueprint

def register_blueprint(app):
    api = Api(app)
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)