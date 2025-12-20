from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post_like_model import PostLikeModel
from resources.posts.post_schema import PostActionRequestSchema, PostActionResponseSchema
from schemas.meta import MetaSchema

blp = Blueprint("PostLike", __name__, description="Post Like")

@blp.route("/post/like")
class PostLike(MethodView):
    @jwt_required()
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = current_user.uid
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

        response = PostActionResponseSchema()
        response.meta = meta
        return response