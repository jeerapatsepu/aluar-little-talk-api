from flask import redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required
)
from datetime import datetime, timezone
from models import USLI
from app.shared import db, uid
from models.user_profile import UserProfile
from resources.profile.profile.profile_request_schema import ProfileDataResponseSchema, ProfileRequestSchema, ProfileResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema
from app.shared import bcrypt

blp = Blueprint("Profile", __name__, description="Profile")

@blp.route("/profile")
class Profile(MethodView):
    @jwt_required()
    @blp.arguments(ProfileRequestSchema)
    @blp.response(200, ProfileResponseSchema)
    def post(self, request):
        uid = request["uid"]

        usli = USLI.query.filter_by(uid=uid).first()
        if usli:
            profile = UserProfile.query.filter_by(uid=uid).first()
            if profile:
                return self.getAuthCreateSuccessResponse(profile)
            else:
                return self.createProfile(usli)
        else:
            return self.getAuthCreateFailResponse(5000)

    def createProfile(self, usli: USLI):
        profile = UserProfile(uid=usli.uid,
                          email=usli.email,
                          full_name=usli.full_name,
                          photo="",
                          caption="",
                          link="",
                          created_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(profile)
        db.session.commit()
        return self.getAuthCreateSuccessResponse(profile)

    def getAuthCreateSuccessResponse(self, profile: UserProfile):
        time = datetime.now(timezone.utc)

        data = ProfileDataResponseSchema()
        data.name = profile.full_name
        data.email = profile.email
        data.uid = profile.uid
        data.photo = profile.photo
        data.caption = profile.caption
        data.link = profile.link

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

    def getAuthCreateFailResponse(self, response_code):
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