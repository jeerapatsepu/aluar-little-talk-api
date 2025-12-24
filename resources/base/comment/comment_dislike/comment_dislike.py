from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post.comment_like_model import CommentLikeModel
from resources.base.comment.comment_like.comment_like_schema import CommentLikeResponseSchema, CommentLikeResquestSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostCommentDislike", __name__, description="Post Comment Dislike")

@blp.route("/post/comment/dislike")
class PostCommentDisLike(MethodView):
    @jwt_required()
    @blp.arguments(CommentLikeResquestSchema)
    @blp.response(200, CommentLikeResponseSchema)
    def post(self, request):
        comment_id = request["comment_id"]
        owner_uid = current_user.uid
        like = CommentLikeModel.query.filter_by(comment_id=comment_id, user_uid=owner_uid).first()
        if like:
            self.__deleteCommentLikeModel(like=like)
        return self.__getCommentLikeResponseSchema()
    
    def __deleteCommentLikeModel(self, like: CommentLikeModel):
        db.session.delete(like)
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