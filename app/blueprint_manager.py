from flask_smorest import Api
from resources.auth.auth_apple_create.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_apple_login.auth_apple_login import blp as AuthLoginBlueprint
from resources.home.home import blp as HomeBlueprint
from resources.profile.profile.profile import blp as ProfileBlueprint
from resources.profile.posts.posts import blp as ProfilePostsBlueprint

def register_blueprint(app):
    api = Api(app)
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(ProfilePostsBlueprint)