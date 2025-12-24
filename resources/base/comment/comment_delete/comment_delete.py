from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from resources.base.comment.comment_like.comment_like_schema import CommentLikeResponseSchema, CommentLikeResquestSchema
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostCommentDelete", __name__, description="Post Comment Delete")

@blp.route("/post/comment/delete")
class PostCommentDelete(MethodView):
    @jwt_required()
    @blp.arguments(CommentLikeResquestSchema)
    @blp.response(200, CommentLikeResponseSchema)
    def post(self, request):
        comment_id = request["comment_id"]
        self.__deleteCommentModel(comment_id=comment_id)
        return self.__getPostsCommentDeleteResponseSchema()

    def __deleteCommentModel(self, comment_id: str):
        owner_uid = current_user.uid
        CommentModel.query.filter_by(comment_uid=comment_id, user_uid=owner_uid).delete(synchronize_session=False)
        CommentLikeModel.query.filter_by(comment_id=comment_id).delete(synchronize_session=False)
        self.__deleteReply(comment_id=comment_id)
        db.session.commit()

    def __deleteReply(self, comment_id: str):
        reply_list = CommentModel.query.filter_by(parent_comment_uid=comment_id).all()
        for reply in reply_list:
            CommentLikeModel.query.filter_by(comment_id=reply.comment_uid).delete(synchronize_session=False)
        CommentModel.query.filter_by(parent_comment_uid=comment_id).delete(synchronize_session=False)

    def __getPostsCommentDeleteResponseSchema(self):
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