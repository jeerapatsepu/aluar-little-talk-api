from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from app.routes.post_route.comment.comment_reply_list.comment_reply_list_schema import CommentReplyListResponseSchema, CommentReplyListResquestSchema
from app.services.post_comment_service import get_reply_list

blp = Blueprint("PostCommentReplyList", __name__, description="Post Comment Reply List")

@blp.route("/post/comment/reply/list")
class PostCommentReplyList(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(CommentReplyListResquestSchema)
    @blp.response(200, CommentReplyListResponseSchema)
    def post(self, request):
        return get_reply_list(request)