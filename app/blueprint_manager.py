from flask_smorest import Api
from resources.auth.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_apple_login import blp as AuthLoginBlueprint
from resources.home.home import blp as HomeBlueprint
from resources.profile.profile.profile import blp as ProfileBlueprint
from resources.profile.profile_user.profile_user import blp as ProfileUserBlueprint
from resources.profile.post.profile_posts import blp as ProfilePostsBlueprint
from resources.profile.repost.profile_reposts import blp as ProfileRePostsBlueprint
from resources.profile.bookmark.profile_bookmarks import blp as ProfileBookmarksBlueprint
from resources.search.new_user_list import blp as NewUserListBlueprint
from resources.posts.post_create.post_create import blp as PostCreateBlueprint
from resources.posts.like.post_like import blp as PostLikeBlueprint
from resources.posts.like.post_dislike import blp as PostDisLikeBlueprint
from resources.posts.get_post import blp as GetPostBlueprint
from resources.posts.bookmark.post_bookmark import blp as PostBookmarkBlueprint
from resources.posts.bookmark.post_unbookmark import blp as PostUnbookmarkBlueprint
from resources.posts.repost.post_repost import blp as PostRepostBlueprint
from resources.posts.repost.post_unrepost import blp as PostUnrepostBlueprint

def register_blueprint(app):
    api = Api(app)
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(ProfileUserBlueprint)
    api.register_blueprint(ProfilePostsBlueprint)
    api.register_blueprint(NewUserListBlueprint)
    api.register_blueprint(PostCreateBlueprint)
    api.register_blueprint(PostLikeBlueprint)
    api.register_blueprint(PostDisLikeBlueprint)
    api.register_blueprint(GetPostBlueprint)
    api.register_blueprint(PostBookmarkBlueprint)
    api.register_blueprint(PostUnbookmarkBlueprint)
    api.register_blueprint(PostRepostBlueprint)
    api.register_blueprint(PostUnrepostBlueprint)
    api.register_blueprint(ProfileRePostsBlueprint)
    api.register_blueprint(ProfileBookmarksBlueprint)