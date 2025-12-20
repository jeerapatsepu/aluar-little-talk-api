from flask_smorest import Api
from resources.auth.auth_apple_create.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_apple_login.auth_apple_login import blp as AuthLoginBlueprint
from resources.home.home import blp as HomeBlueprint
from resources.profile.profile.profile import blp as ProfileBlueprint
from resources.profile.posts.profile_posts.posts import blp as ProfilePostsBlueprint
from resources.search.new_user_list import blp as NewUserListBlueprint
from resources.posts.post_create.post_create import blp as PostCreateBlueprint
from resources.posts.like.post_like import blp as PostLikeBlueprint
from resources.posts.like.post_dislike import blp as PostDisLikeBlueprint
from resources.posts.get_post.get_post import blp as GetPostBlueprint
from resources.posts.bookmark.post_bookmark import blp as PostBookmarkBlueprint
from resources.posts.bookmark.post_unbookmark import blp as PostUnbookmarkBlueprint

def register_blueprint(app):
    api = Api(app)
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(ProfilePostsBlueprint)
    api.register_blueprint(NewUserListBlueprint)
    api.register_blueprint(PostCreateBlueprint)
    api.register_blueprint(PostLikeBlueprint)
    api.register_blueprint(PostDisLikeBlueprint)
    api.register_blueprint(GetPostBlueprint)
    api.register_blueprint(PostBookmarkBlueprint)
    api.register_blueprint(PostUnbookmarkBlueprint)