from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from app.models.comment_like_model import CommentLikeModel
from app.models.comment_model import CommentModel
from resources.base.comment.comment_like.comment_like_schema import CommentLikeResponseSchema, CommentLikeResquestSchema
from app.schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostCommentLike", __name__, description="Post Comment Like")

@blp.route("/post/comment/like")
class PostCommentLike(MethodView):
    @jwt_required()
    @blp.arguments(CommentLikeResquestSchema)
    @blp.response(200, CommentLikeResponseSchema)
    def post(self, request):
        comment_id = request["comment_id"]
        comment_like = CommentLikeModel.query.filter_by(comment_id=comment_id, user_uid=current_user.uid).first()
        if not comment_like:
            self.__createCommentLikeModel(comment_id=comment_id)
        return self.__getCommentLikeResponseSchema()

    def __createCommentLikeModel(self, comment_id: str):
        owner_uid = current_user.uid
        now = int(datetime.now(timezone.utc).timestamp())
        comment = CommentModel.query.filter_by(comment_uid=comment_id).first()
        comment_like = CommentLikeModel(post_id=comment.post_id,
                                        comment_id=comment_id,
                                        user_uid=owner_uid,
                                        comment_type="COMMENT",
                                        created_date_timestamp=now,
                                        updated_date_timestamp=now)
        db.session.add(comment_like)
        db.session.commit()

    def __getCommentLikeResponseSchema(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = CommentLikeResponseSchema()
        response.meta = meta
        return response