from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from app.models.comment_model import CommentModel
from app.models.user_profile import UserProfile
from resources.base.comment.comment_create.comment_create_response_schema import CommentCreateResponseSchema
from resources.full_comment import FullComment
from app.schemas.reponse_schema.meta import MetaSchema
from app.extensions import boto_client
import base64
import os
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.post_comment_create_request_schema import PostCommentCreateRequestSchema

blp = Blueprint("PostCommentCreate", __name__, description="Post Comment Create")

@blp.route("/post/comment/create")
class PostCommentCreate(MethodView):
    @jwt_required()
    @blp.arguments(PostCommentCreateRequestSchema)
    @blp.response(200, CommentCreateResponseSchema)
    def post(self, request):
        return self.__createPostComment(request=request)

    def __createPostComment(self, request):
        text = request["text"]
        image = request["image"]
        parent_comment_uid = request["parent_comment_uid"]
        post_id = request["post_id"]
        reply_uid = request["reply_uid"]
        comment_id = uuid.uuid4().hex
        owner_uid = current_user.uid
        image_url = self.__uploadCommentImage(comment_id=comment_id, image=image)
        comment = CommentModel(comment_uid=comment_id,
                                text=text,
                                image_url=image_url,
                                parent_comment_uid=parent_comment_uid,
                                post_id=post_id,
                                user_uid=owner_uid,
                                reply_uid=reply_uid,
                                created_date_timestamp = int(datetime.now(timezone.utc).timestamp()),
                                updated_date_timestamp = int(datetime.now(timezone.utc).timestamp()))
        db.session.add(comment)
        db.session.commit()
        return self.__getPostsCommentCreateSuccessResponseSchema(comment=comment, reply_uid=reply_uid)

    def __uploadCommentImage(self, comment_id: str, image: str):
        try:
            if len(image) > 0:
                image_path = 'comments/' + comment_id + '.jpg'
                boto_client.put_object(Body=base64.b64decode(image),
                                Bucket=os.getenv("S3_BUCKET_NAME"),
                                Key=image_path,
                                ACL='public-read',
                                ContentType='image/jpeg')
                return os.getenv('LITTLE_TALK_S3_ENDPOINT') + '/' + image_path
            else:
                return ""
        except Exception:
            return ""
    
    def __getPostsCommentCreateSuccessResponseSchema(self, comment: CommentModel, reply_uid: str):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        comment_schema = FullComment(comment_id=comment.comment_uid).get_comment()
        if reply_uid:
            reply_profile = UserProfile.query.filter_by(uid=reply_uid).one()
            comment_schema.reply_uid = reply_profile.uid
            comment_schema.reply_name = reply_profile.full_name
            comment_schema.reply_image = reply_profile.photo

        response = CommentCreateResponseSchema()
        response.meta = meta
        response.data = comment_schema
        return response