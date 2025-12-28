import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
from models.post.comment_model import CommentModel
from models.profile.user_profile import UserProfile
from resources.base.comment.comment_list.comment_list_response_schema import PostsCommentListResponseSchema
from resources.full_comment import FullComment
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema
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
        comments = CommentModel.query.order_by(CommentModel.created_date_timestamp).filter(CommentModel.post_id==post_id, CommentModel.parent_comment_uid=="").offset(offset).limit(limit).all()
        comments = self.__getCommentResponseSchema(comments=comments)
        return self.__getPofileCommentListSuccessResponse(comments=comments)

    def __getCommentResponseSchema(self, comments: list):
        comment_schema_list = []
        for comment in comments:
            comment_schema = FullComment(comment_id=comment.comment_uid).get_comment()
            comment_schema_list.append(comment_schema)
        return comment_schema_list

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
