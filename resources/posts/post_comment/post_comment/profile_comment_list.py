import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
from models.post.comment_model import CommentModel
from models.user_profile import UserProfile
from resources.posts.post_comment.post_comment.post_comment_list_response_schema import PostsCommentListResponseSchema
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
        comments = CommentModel.query.order_by(CommentModel.created_date_timestamp).filter(CommentModel.post_id==post_id).offset(offset).limit(limit).all()
        comments.sort(key=self.__sortCommentsList, reverse=False)
        comments = self.__getCommentResponseSchema(comments=comments)
        return self.__getPofileCommentListSuccessResponse(comments=comments)

    def __sortCommentsList(self, e):
        return e.created_date_timestamp

    def __getCommentResponseSchema(self, comments: list):
        comment_response_list = []
        for comment in comments:
            owner_profile = UserProfile.query.filter_by(uid=comment.user_uid).first()
            comment_response = CommentResponseSchema()
            comment_response.comment_id = comment.comment_uid
            comment_response.parent_comment_id = comment.parent_comment_uid
            if owner_profile:
                comment_response.owner_image = owner_profile.photo
                comment_response.owner_name = owner_profile.full_name
                comment_response.owner_uid = owner_profile.uid
            comment_response.post_id = comment.post_id
            comment_response.text = comment.text
            comment_response.image_url = comment.image_url
            comment_response.created_date_timestamp = comment.created_date_timestamp
            comment_response.updated_date_timestamp = comment.updated_date_timestamp
            try:
                comment_response.is_owner = comment.comment_uid == current_user.uid
            except Exception:
                comment_response.is_owner = False

            comment_response_list.append(comment_response)
        return comment_response_list

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
