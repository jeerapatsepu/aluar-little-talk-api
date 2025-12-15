from flask import redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from models import USLI
from app.shared import db, uid
from models.post import Post
from models.user_profile import UserProfile
from resources.profile.posts.profile_posts.posts_request_schema import ProfilePostsDataResponseSchema, ProfilePostsRequestSchema, ProfilePostsResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema
from app.shared import bcrypt

blp = Blueprint("ProfilePosts", __name__, description="Profile Posts")

@blp.route("/profile/posts")
class ProfilePosts(MethodView):
    @jwt_required()
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]

        posts = Post.query.filter_by(owner_uid=uid).offset(offset).limit(limit).all()
        return self.getPofilePostsSuccessResponse(posts)

    def getPofilePostsSuccessResponse(self, posts):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfilePostsResponseSchema()
        response.meta = meta
        response.data = posts
        return response