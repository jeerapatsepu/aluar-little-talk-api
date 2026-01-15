import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone
from app.models.user_relationship import UserRelationship
from app.extensions import db
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.post_action_response_schema import PostActionResponseSchema
from app.schemas.request_schema.profile_request_schema import ProfileRequestSchema

blp = Blueprint("ProfileUnfollow", __name__, description="Profile Unfollow")

@blp.route("/profile/unfollow")
class ProfileUnfollow(MethodView):
    @jwt_required()
    @blp.arguments(ProfileRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        uid = request["uid"]
        relationship = UserRelationship.query.filter_by(sender_id=current_user.uid, receiver_id=uid).first()
        if relationship:
            db.session.delete(relationship)
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