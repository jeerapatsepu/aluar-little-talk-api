import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
from models.post.post import Post
from resources.base.short_post import ShortPost
from resources.profile.post.profile_posts_response import ProfilePostsResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.meta import MetaSchema
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
        posts = Post.query.filter_by(owner_uid=uid).offset(offset).limit(limit).all()
        posts.sort(key=self.__sortPostsList, reverse=True)
        new_posts = self.__getShortPost(posts=posts)
        return self.__getPofilePostsSuccessResponse(new_posts)

    def __getShortPost(self, posts: list):
        short_post_list = []
        for post in posts:
            short_post = ShortPost(post_id=post.post_id)
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
