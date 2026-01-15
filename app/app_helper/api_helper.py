from flask import Flask
from flask_smorest import Api
from app.routes.auth_route.auth_create import blp as AuthCreateBlueprint
from app.routes.auth_route.auth_apple_login import blp as AuthLoginBlueprint
from app.routes.auth_route.auth_logout import blp as AuthLogoutBlueprint
from app.routes.home_route.home import blp as HomeBlueprint
from app.routes.profile_route.profile import blp as ProfileBlueprint
from app.routes.profile_route.profile_user import blp as ProfileUserBlueprint
from app.routes.profile_route.profile_posts import blp as ProfilePostsBlueprint
from app.routes.post_route.post.post_create.post_create import blp as PostCreateBlueprint
from app.routes.post_route.post.like.post_like import blp as PostLikeBlueprint
from app.routes.post_route.post.like.post_dislike import blp as PostDisLikeBlueprint
from app.routes.post_route.post.post_delete import blp as PostDeleteBlueprint
from app.routes.post_route.post.get_post.get_post import blp as GetPostBlueprint
from app.routes.post_route.post.bookmark.post_bookmark import blp as PostBookmarkBlueprint
from app.routes.post_route.post.bookmark.post_unbookmark import blp as PostUnbookmarkBlueprint
from app.routes.post_route.post.repost.post_repost import blp as PostRepostBlueprint
from app.routes.post_route.post.repost.post_unrepost import blp as PostUnrepostBlueprint
from app.routes.post_route.comment.comment_create.comment_create import blp as PostCommentCreateBlueprint
from app.routes.post_route.comment.comment_list.comment_list import blp as ProfileCommentListBlueprint
from app.routes.post_route.comment.comment_like.comment_like import blp as PostCommentLikeBlueprint
from app.routes.post_route.comment.comment_dislike.comment_dislike import blp as PostCommentDisLikeBlueprint
from app.routes.post_route.comment.comment_delete.comment_delete import blp as PostCommentDeleteBlueprint
from app.routes.post_route.post.post_like_list.post_like_list import blp as PostLikeListBlueprint
from app.routes.post_route.post.post_comment_user_list.post_comment_user_list import blp as PostCommentUserListBlueprint
from app.routes.post_route.post.post_repost_user_list.post_repost_user_list import blp as PostRepostUserListBlueprint
from app.routes.post_route.comment.comment_like_user_list.comment_like_user_list import blp as PostCommentLikeUserListBlueprint
from app.routes.profile_route.profile_follow import blp as ProfileFollowBlueprint
from app.routes.profile_route.profile_unfollow import blp as ProfileUnfollowBlueprint
from app.routes.profile_route.profile_change_photo import blp as ProfileChangePhotoBlueprint
from app.routes.profile_route.profile_edit import blp as ProfileEditBlueprint
from app.routes.delete_user_route.delete_user_term.delete_user_term import blp as DeleteUserTermBlueprint
from app.routes.delete_user_route.delete_user_request.delete_user_request import blp as DeleteUserRequestBlueprint
from app.routes.internal_route.delete_user import blp as InternalDeleteUserBlueprint
from app.routes.internal_route.profile_recommendation import blp as InternalProfileRecommendationBlueprint
from app.routes.search_route.search_user_list.search_user_list import blp as SearchUserListBlueprint
from app.routes.search_route.search_recomment_user_list.search_recomment_user_list import blp as SearchRecommentUserListBlueprint
from app.routes.search_route.search_post_list.search_post_list import blp as SearchPostListBlueprint
from app.routes.search_route.search_recomment_post_list.search_recomment_post_list import blp as SearchRecommentPostListBlueprint

class APIHelper:
    def __init__(self, app: Flask):
        self.__app = app

    def register_blueprint(self):
        api = Api(self.__app)
        api.register_blueprint(HomeBlueprint)
        api.register_blueprint(AuthCreateBlueprint)
        api.register_blueprint(AuthLoginBlueprint)
        api.register_blueprint(AuthLogoutBlueprint)
        api.register_blueprint(ProfileBlueprint)
        api.register_blueprint(ProfileUserBlueprint)
        api.register_blueprint(ProfilePostsBlueprint)
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
        api.register_blueprint(DeleteUserTermBlueprint)
        api.register_blueprint(DeleteUserRequestBlueprint)
        api.register_blueprint(InternalDeleteUserBlueprint)
        api.register_blueprint(InternalProfileRecommendationBlueprint)
        api.register_blueprint(SearchUserListBlueprint)
        api.register_blueprint(SearchRecommentUserListBlueprint)
        api.register_blueprint(SearchPostListBlueprint)
        api.register_blueprint(SearchRecommentPostListBlueprint)