from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post_like_model import PostLikeModel
from resources.posts.post_like.post_like_request_schema import PostLikeRequestSchema, PostLikeResponseSchema
from schemas.meta import MetaSchema

blp = Blueprint("PostLike", __name__, description="Post Like")

@blp.route("/post/like")
class PostLike(MethodView):
    @jwt_required()
    @blp.arguments(PostLikeRequestSchema)
    @blp.response(200, PostLikeResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = get_jwt_identity()
        like = PostLikeModel.query.filter_by(post_id=post_id, user_uid=owner_uid).first()
        if not like:
            post_like = PostLikeModel(post_id=post_id,
                                      user_uid=owner_uid,
                                      created_date_timestamp=int(datetime.now(timezone.utc).timestamp()),
                                      updated_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
            db.session.add(post_like)
            db.session.commit()
        return self.getPostsLikeResponseSchema()

    def getPostsLikeResponseSchema(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostLikeResponseSchema()
        response.meta = meta
        return response