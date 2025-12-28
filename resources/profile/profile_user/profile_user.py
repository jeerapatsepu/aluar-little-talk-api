from marshmallow import Schema, fields
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone
from models.profile.user_relationship import UserRelationship
from models.usli import USLI
from app.shared import db, uid
from models.profile.user_profile import UserProfile
from resources.profile.profile.profile_response_schema import ProfileResponseSchema
from schemas.reponse_schema.error import ErrorSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.profile.profile_request_schema import ProfileRequestSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

blp = Blueprint("ProfileUser", __name__, description="Profile User")

@blp.route("/profile/user")
class ProfileUser(MethodView):
    @blp.arguments(ProfileRequestSchema)
    @blp.response(200, ProfileResponseSchema)
    def post(self, request):
        uid = request["uid"]
        usli = db.session.query(USLI).filter(USLI.uid==uid).first()
        if usli:
            profile = db.session.query(UserProfile).filter(UserProfile.uid==uid).first()
            if profile:
                return self.__getProfileSuccessResponse(profile)
            else:
                return self.__getProfileFailResponse(5000)
        else:
            return self.__getProfileFailResponse(5000)

    def __getProfileSuccessResponse(self, profile: UserProfile):
        time = datetime.now(timezone.utc)

        data = ProfileDataResponseSchema()
        data.name = profile.full_name
        data.uid = profile.uid
        data.photo = profile.photo
        data.caption = profile.caption
        data.link = profile.link
        relationship_status_of_current_user = UserRelationship.query.filter_by(receiver_id=current_user.uid, sender_id=data.uid).first()
        relationship_status_of_user = UserRelationship.query.filter_by(receiver_id=data.uid, sender_id=current_user.uid).first()
        relationship_status = ""
        if relationship_status_of_current_user:
            relationship_status = relationship_status_of_current_user.status
        if relationship_status_of_user:
            relationship_status = "FRIEND"
        data.relationship_status = relationship_status

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfileResponseSchema()
        response.meta = meta
        response.data = data
        return response

    def __getProfileFailResponse(self, response_code):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "Email is not unique"

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = ProfileResponseSchema()
        response.meta = meta
        response.data = None
        return response