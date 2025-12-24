import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
from models.post.post import Post
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_repost_model import PostRepostModel
from resources.base.post.short_post import ShortPost
from resources.profile.post.profile_posts_response import ProfilePostsResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post.post_data_schema import PostDataSchema
from schemas.request_schema.profile.profile_posts_request_schema import ProfilePostsRequestSchema

blp = Blueprint("ProfilePosts", __name__, description="Profile Posts")

@blp.route("/profile/posts")
class ProfilePosts(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]
        filter = request["filter"]
        posts = []
        match filter:
            case "ALL":
                posts = Post.query.order_by(Post.created_date_timestamp).filter(Post.owner_uid==uid, Post.visibility=="PUBLIC").offset(offset).limit(limit).all()
                posts.sort(key=self.__sortPostsList, reverse=True)
                posts = self.__getShortPost(posts=posts)
            case "REPOSTS":
                reposts = PostRepostModel.query.filter_by(user_uid=uid).order_by(PostRepostModel.created_date_timestamp).offset(offset).limit(limit).all()
                reposts.sort(key=self.__sortPostsList, reverse=True)
                posts = self.__getShortPost(posts=reposts)
            case "BOOKMARKS":
                bookmarks = PostBookmarkModel.query.filter_by(user_uid=uid).order_by(PostBookmarkModel.created_date_timestamp).offset(offset).limit(limit).all()
                bookmarks.sort(key=self.__sortPostsList, reverse=True)
                posts = self.__getShortPost(posts=bookmarks)
            case "PRIVATE":
                posts = Post.query.order_by(Post.created_date_timestamp).filter(Post.owner_uid==uid, Post.visibility=="PRIVATE").offset(offset).limit(limit).all()
                posts.sort(key=self.__sortPostsList, reverse=True)
                posts = self.__getPrivateShortPost(posts=posts)
            case _:
                posts = Post.query.order_by(Post.created_date_timestamp).filter(Post.owner_uid==uid, Post.visibility=="PUBLIC").offset(offset).limit(limit).all()
                posts.sort(key=self.__sortPostsList, reverse=True)
                posts = self.__getShortPost(posts=posts)
        return self.__getPofilePostsSuccessResponse(posts)

    def __getShortPost(self, posts: list):
        short_post_list = []
        for post in posts:
            short_post = ShortPost(post_id=post.post_id).get_post()
            if short_post.visibility != "PRIVATE":
                short_post_list.append(short_post)
        return short_post_list
    
    def __getPrivateShortPost(self, posts: list):
        short_post_list = []
        for post in posts:
            short_post = ShortPost(post_id=post.post_id).get_post()
            short_post_list.append(short_post)
        return short_post_list

    def __sortPostsList(self, e):
        return e.created_date_timestamp

    def __getPofilePostsSuccessResponse(self, posts):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfilePostsResponseSchema()
        response.meta = meta
        response.data = posts
        return response
