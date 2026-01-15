from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
import uuid
from app.routes.post_route.comment.comment_delete_tool import CommentDeleteTool
from app.routes.post_route.comment.comment_like.comment_like_schema import CommentLikeResponseSchema, CommentLikeResquestSchema
from app.schemas.reponse_schema.post_action_response_schema import PostActionResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema


blp = Blueprint("PostCommentDelete", __name__, description="Post Comment Delete")

@blp.route("/post/comment/delete")
class PostCommentDelete(MethodView):
    @jwt_required()
    @blp.arguments(CommentLikeResquestSchema)
    @blp.response(200, CommentLikeResponseSchema)
    def post(self, request):
        comment_id = request["comment_id"]
        CommentDeleteTool(comment_id=comment_id).deleteComment()
        return self.__getPostsCommentDeleteResponseSchema()

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