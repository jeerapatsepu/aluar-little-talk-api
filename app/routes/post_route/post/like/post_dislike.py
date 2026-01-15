from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from app.models.post_like_model import PostLikeModel
from app.schemas.reponse_schema.post_action_response_schema import PostActionResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.post_action_request_schema import PostActionRequestSchema

blp = Blueprint("PostDislike", __name__, description="Post Dislike")

@blp.route("/post/dislike")
class PostDisLike(MethodView):
    @jwt_required()
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = current_user.uid
        like = PostLikeModel.query.filter_by(post_id=post_id, user_uid=owner_uid).first()
        if like:
            self.__deletePostLikeModel(like=like)
        return self.__getPostsLikeResponseSchema()
    
    def __deletePostLikeModel(self, like: PostLikeModel):
        db.session.delete(like)
        db.session.commit()

    def __getPostsLikeResponseSchema(self):
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