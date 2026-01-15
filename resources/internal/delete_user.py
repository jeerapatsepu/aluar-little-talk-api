import os
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone, timedelta
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_like_model import PostLikeModel
from models.post.post_repost_model import PostRepostModel
from models.profile.user_profile import UserProfile
from models.profile.user_relationship import UserRelationship
from models.user_delete_request import UserDeleteRequest
from models.usli import USLI
from resources.internal.tools.InternalDeleteCommentManager import InternalDeleteCommentManager
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from app.extensions import db
from app.extensions import boto_client

blp = Blueprint("InternalDeleteUser", __name__, description="Internal Delete User")

@blp.route("/internal/delete/user")
class InternalDeleteUser(MethodView):
    @blp.response(200, PostActionResponseSchema)
    def post(self):
        internal_header_key = request.headers.get("X-Internal-Auth")
        if internal_header_key == os.getenv("INTERNAL_AUTH_KEY"):
            self.__deleteUserThan15Days()
            return self.__getSuccessResponse()
        else:
            return self.__getFailResponse()
    
    def __deleteUserThan15Days(self):
        user_uid_list = UserDeleteRequest.query.all()
        user_uid_list = self.__filterThan15Days(request_list=user_uid_list)
        for user_request in user_uid_list:
            USLI.query.filter_by(uid=user_request.user_uid).delete()
            UserProfile.query.filter_by(uid=user_request.user_uid).delete()
            UserRelationship.query.filter_by(sender_id=user_request.user_uid).delete()
            UserRelationship.query.filter_by(receiver_id=user_request.user_uid).delete()
            UserDeleteRequest.query.filter_by(user_uid=user_request.user_uid).delete()
            post_list = Post.query.filter_by(owner_uid=user_request.user_uid).all()
            Post.query.filter_by(owner_uid=user_request.user_uid).delete(synchronize_session=False)
            for post in post_list:
                self.__delete_post_contents(post_id=post.post_id)
            CommentLikeModel.query.filter_by(user_uid=user_request.user_uid).delete(synchronize_session=False)
            CommentModel.query.filter_by(user_uid=user_request.user_uid).delete(synchronize_session=False)
            PostContent.query.filter_by(owner_uid=user_request.user_uid).delete(synchronize_session=False)
            PostImageContent.query.filter_by(owner_uid=user_request.user_uid).delete(synchronize_session=False)
            PostLikeModel.query.filter_by(user_uid=user_request.user_uid).delete(synchronize_session=False)
            PostBookmarkModel.query.filter_by(user_uid=user_request.user_uid).delete(synchronize_session=False)
            PostRepostModel.query.filter_by(user_uid=user_request.user_uid).delete(synchronize_session=False)
            db.session.commit()

    def __filterThan15Days(self, request_list: list):
        list = []
        for item in request_list:
            ts_date = datetime.fromtimestamp(item.created_date_timestamp)
            if datetime.now() - ts_date > timedelta(days=15):
                list.append(item)
        return list
    
    def __delete_post_contents(self, post_id: str):
        InternalDeleteCommentManager().deleteAllCommentOfPost(post_id=post_id)
        db.session.commit()
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "posts/" + post_id
            response = boto_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )
            if "Contents" in response:
                boto_client.delete_objects(
                    Bucket=bucket,
                    Delete={
                        "Objects": [{"Key": obj["Key"]} for obj in response["Contents"]]
                    }
                )
        except Exception:
            pass
        
    def __getSuccessResponse(self):
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
    
    def __getFailResponse(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 5000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostActionResponseSchema()
        response.meta = meta
        return response