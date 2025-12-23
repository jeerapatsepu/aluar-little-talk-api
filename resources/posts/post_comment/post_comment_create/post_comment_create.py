from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post.comment_model import CommentModel
from models.user_profile import UserProfile
from resources.posts.post_comment.post_comment_create.post_comment_create_response_schema import PostsCommentCreateResponseSchema
from resources.posts.post_create.post_create_response_schema import PostsCreateResponseSchema
from schemas.reponse_schema.error import ErrorSchema
from schemas.reponse_schema.meta import MetaSchema
from app.s3 import client
import base64
import os
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema
from schemas.request_schema.post.post_comment_create_request_schema import PostCommentCreateRequestSchema

blp = Blueprint("PostCommentCreate", __name__, description="Post Comment Create")

@blp.route("/post/comment/create")
class PostCommentCreate(MethodView):
    @jwt_required()
    @blp.arguments(PostCommentCreateRequestSchema)
    @blp.response(200, PostsCommentCreateResponseSchema)
    def post(self, request):
        self.__createPostComment(request=request)

    def __createPostComment(self, request):
        text = request["text"]
        image = request["image"]
        comment_type = request["comment_type"]
        parent_comment_uid = request["parent_comment_uid"]
        post_id = request["post_id"]
        reply_user_uid = request["reply_user_uid"]
        comment_uid = uuid.uuid4().hex
        owner_uid = current_user.uid
        try:
            image_path = 'comments/' + comment_uid + '.jpg'
            client.put_object(Body=base64.b64decode(image),
                              Bucket=os.getenv("S3_BUCKET_NAME"),
                              Key=image_path,
                              ACL='public-read',
                              ContentType='image/jpeg')
            image_url=os.getenv('LITTLE_TALK_S3_ENDPOINT') + '/' + image_path
            comment = CommentModel(comment_type=comment_type,
                                   comment_uid=comment_uid,
                                   text=text,
                                   image_url=image_url,
                                   parent_comment_uid=parent_comment_uid,
                                   reply_user_uid=reply_user_uid,
                                   post_id=post_id,
                                   user_uid=owner_uid,
                                   created_date_timestamp = int(datetime.now(timezone.utc).timestamp()),
                                   updated_date_timestamp = int(datetime.now(timezone.utc).timestamp()))
            db.session.add(comment)
            db.session.commit()
            self.__getPostsCommentCreateSuccessResponseSchema(comment=comment)
        except Exception:
            self.__getPostsCommentCreateFailResponseSchema()

    def __getPostsCommentCreateSuccessResponseSchema(self, comment: CommentModel):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        owner_profile = UserProfile.query.filter_by(uid=comment.user_uid).first()
        reply_profile = UserProfile.query.filter_by(uid=comment.reply_user_uid).first()
        data = CommentResponseSchema()
        data.comment_id = comment.comment_uid
        data.comment_type = comment.comment_type
        data.parent_comment_id = comment.parent_comment_uid
        data.owner_image = owner_profile.photo
        data.owner_name = owner_profile.full_name
        data.owner_uid = owner_profile.uid
        data.reply_user_uid = reply_profile.uid
        data.reply_user_name = reply_profile.full_name
        data.post_id = comment.post_id
        data.is_owner = comment.user_uid == current_user.uid
        data.created_date_timestamp = comment.created_date_timestamp
        data.updated_date_timestamp = comment.updated_date_timestamp

        response = PostsCommentCreateResponseSchema()
        response.meta = meta
        response.data = data
        return response
    
    def __getPostsCommentCreateFailResponseSchema(self):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "Can not create comment"

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 5000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = PostsCommentCreateResponseSchema()
        response.meta = meta
        response.data = None
        return response