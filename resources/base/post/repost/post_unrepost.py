from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from models.post.post_repost_model import PostRepostModel
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_action_request_schema import PostActionRequestSchema

blp = Blueprint("PostUnrepost", __name__, description="Post Unrepost")

@blp.route("/post/unrepost")
class PostUnrepost(MethodView):
    @jwt_required()
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = current_user.uid
        repost = PostRepostModel.query.filter_by(post_id=post_id, user_uid=owner_uid).first()
        if repost:
            self.__deletePostRepostModel(repost=repost)
        return self.__getPostsUnrepostResponseSchema()

    def __deletePostRepostModel(self, repost: PostRepostModel):
        db.session.delete(repost)
        db.session.commit()

    def __getPostsUnrepostResponseSchema(self):
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