import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint
from datetime import datetime, timezone
from models.user_delete_request import UserDeleteRequest
from resources.delete_user.delete_user_term.delete_user_term_schema import DeleteUserTermDataSchema, DeleteUserTermResponseSchema
from resources.profile.profile_change_photo.profile_change_photo_schema import ProfileChangePhotoResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from app.shared import db

blp = Blueprint("DeleteUserRequest", __name__, description="Delete User Request")

@blp.route("/delete/user/request")
class DeleteUserRequest(MethodView):
    @jwt_required()
    @blp.response(200, PostActionResponseSchema)
    def post(self):
        delete_request = UserDeleteRequest(user_uid=current_user.uid,
                        created_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(delete_request)
        db.session.commit()
        return self.__getSuccessResponse()
    
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