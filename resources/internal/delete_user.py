import os
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone, timedelta
from models.post.post import Post
from models.profile.user_profile import UserProfile
from models.profile.user_relationship import UserRelationship
from models.user_delete_request import UserDeleteRequest
from models.usli import USLI
from resources.full_post import FullPost
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema

blp = Blueprint("InternalDeleteUser", __name__, description="Internal Delete User")

@blp.route("/internal/delete/user")
class InternalDeleteUser(MethodView):
    @blp.response(200, PostActionResponseSchema)
    def post(self):
        internal_header_key = request.headers.get("X-Internal-Auth")
        if internal_header_key == os.getenv("INTERNAL_AUTH_KEY"):
            self.__deleteUserThan15Days()
            return self.__getSuccessResponse()
        return self.__getFailResponse()
    
    def __deleteUserThan15Days(self):
        user_uid_list = UserDeleteRequest.query.filter_by(self.__isThan15Days(created_date_timestamp=credits)).all()
        for uid in user_uid_list:
            USLI.query.filter_by(uid=uid).delete()
            UserProfile.query.filter_by(uid=uid).delete()
            UserRelationship.query.filter_by(sender_id=uid).delete()
            UserRelationship.query.filter_by(receiver_id=uid).delete()
            UserDeleteRequest.query.filter_by(user_uid=uid).delete()
            post_list = Post.query.filter_by(owner_uid=uid).all()
            for post in post_list:
                FullPost(post_id=post.post_id, owner_uid=uid).delete_post()

    def __isThan15Days(self, created_date_timestamp: int) -> bool:
        ts_date = datetime.fromtimestamp(created_date_timestamp)
        return datetime.now() - ts_date > timedelta(days=15)
    
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