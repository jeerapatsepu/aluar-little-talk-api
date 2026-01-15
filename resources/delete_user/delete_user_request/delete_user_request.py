import uuid
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint
from datetime import datetime, timezone
from app.models.user_delete_request import UserDeleteRequest
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.post_action_response_schema import PostActionResponseSchema
from app.extensions import db

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