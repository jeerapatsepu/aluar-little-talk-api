from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post_bookmark_model import PostBookmarkModel
from resources.posts.post_bookmark.post_bookmark_schema import PostBookmarkRequestSchema, PostBookmarkResponseSchema
from resources.posts.post_like.post_like_request_schema import PostLikeRequestSchema, PostLikeResponseSchema
from schemas.meta import MetaSchema

blp = Blueprint("PostUnbookmark", __name__, description="Post Unbookmark")

@blp.route("/post/unbookmark")
class PostUnbookmark(MethodView):
    @jwt_required()
    @blp.arguments(PostBookmarkRequestSchema)
    @blp.response(200, PostBookmarkResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = get_jwt_identity()
        like = PostBookmarkModel.query.filter_by(post_id=post_id, user_uid=owner_uid).first()
        if like:
            db.session.delete(like)
            db.session.commit()
        return self.getPostsUnbookmarkResponseSchema()

    def getPostsUnbookmarkResponseSchema(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostBookmarkResponseSchema()
        response.meta = meta
        return response