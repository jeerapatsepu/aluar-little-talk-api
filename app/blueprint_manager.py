from flask_smorest import Api
from resources.auth.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_apple_login import blp as AuthLoginBlueprint
from resources.home.home import blp as HomeBlueprint
from resources.profile.profile.profile import blp as ProfileBlueprint
from resources.profile.profile_user.profile_user import blp as ProfileUserBlueprint
from resources.profile.post.profile_posts import blp as ProfilePostsBlueprint
from resources.search.new_user_list import blp as NewUserListBlueprint
from resources.base.post.post_create.post_create import blp as PostCreateBlueprint
from resources.base.post.like.post_like import blp as PostLikeBlueprint
from resources.base.post.like.post_dislike import blp as PostDisLikeBlueprint
from resources.base.post.post_delete import blp as PostDeleteBlueprint
from resources.base.post.get_post.get_post import blp as GetPostBlueprint
from resources.base.post.bookmark.post_bookmark import blp as PostBookmarkBlueprint
from resources.base.post.bookmark.post_unbookmark import blp as PostUnbookmarkBlueprint
from resources.base.post.repost.post_repost import blp as PostRepostBlueprint
from resources.base.post.repost.post_unrepost import blp as PostUnrepostBlueprint
from resources.base.comment.comment_create.comment_create import blp as PostCommentCreateBlueprint
from resources.base.comment.comment_list.comment_list import blp as ProfileCommentListBlueprint
from resources.base.comment.comment_like.comment_like import blp as PostCommentLikeBlueprint
from resources.base.comment.comment_dislike.comment_dislike import blp as PostCommentDisLikeBlueprint
from resources.base.comment.comment_delete.comment_delete import blp as PostCommentDeleteBlueprint
from resources.base.post.post_like_list.post_like_list import blp as PostLikeListBlueprint
from resources.base.post.post_comment_user_list.post_comment_user_list import blp as PostCommentUserListBlueprint
from resources.base.post.post_repost_user_list.post_repost_user_list import blp as PostRepostUserListBlueprint
from resources.base.comment.comment_like_user_list.comment_like_user_list import blp as PostCommentLikeUserListBlueprint
from resources.profile.profile_follow.profile_follow import blp as ProfileFollowBlueprint
from resources.profile.profile_unfollow.profile_unfollow import blp as ProfileUnfollowBlueprint
from resources.profile.profile_change_photo.profile_change_photo import blp as ProfileChangePhotoBlueprint
from resources.profile.profile_edit.profile_edit import blp as ProfileEditBlueprint

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
    api.register_blueprint(PostDeleteBlueprint)
    api.register_blueprint(PostCommentCreateBlueprint)
    api.register_blueprint(ProfileCommentListBlueprint)
    api.register_blueprint(PostCommentLikeBlueprint)
    api.register_blueprint(PostCommentDisLikeBlueprint)
    api.register_blueprint(PostCommentDeleteBlueprint)
    api.register_blueprint(PostLikeListBlueprint)
    api.register_blueprint(PostCommentUserListBlueprint)
    api.register_blueprint(PostRepostUserListBlueprint)
    api.register_blueprint(PostCommentLikeUserListBlueprint)
    api.register_blueprint(ProfileFollowBlueprint)
    api.register_blueprint(ProfileUnfollowBlueprint)
    api.register_blueprint(ProfileChangePhotoBlueprint)
    api.register_blueprint(ProfileEditBlueprint)