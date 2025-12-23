import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
from models.post.comment_model import CommentModel
from resources.posts.post_comment.post_comment.post_comment_list_response_schema import PostsCommentListResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_comment_list_request_schema import PostCommentListRequestSchema

blp = Blueprint("ProfileCommentList", __name__, description="Profile Comment List")

@blp.route("/post/comment/list")
class ProfileCommentList(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(PostCommentListRequestSchema)
    @blp.response(200, PostsCommentListResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        offset = request["offset"]
        limit = request["limit"]
        comments = CommentModel.query.order_by(CommentModel.created_date_timestamp).filter(CommentModel.post_id==post_id).offset(offset).limit(limit).all()
        comments.sort(key=self.__sortCommentsList, reverse=True)
        return self.__getPofileCommentListSuccessResponse(comments=comments)

    def __sortCommentsList(self, e):
        return e.created_date_timestamp

    def __getPofileCommentListSuccessResponse(self, comments):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostsCommentListResponseSchema()
        response.meta = meta
        response.data = comments
        return response
