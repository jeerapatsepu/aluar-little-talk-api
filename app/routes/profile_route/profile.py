import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone
from app.models.usli import USLI
from app.extensions import db
from app.models.user_profile import UserProfile
from app.utils.profile import ProfileBase
from app.schemas.reponse_schema.profile_response_schema import ProfileResponseSchema
from app.schemas.reponse_schema.error import ErrorSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.profile_request_schema import ProfileRequestSchema

blp = Blueprint("Profile", __name__, description="Profile")

@blp.route("/profile")
class Profile(MethodView):
    @jwt_required()
    @blp.arguments(ProfileRequestSchema)
    @blp.response(200, ProfileResponseSchema)
    def post(self, request):
        uid = request["uid"]
        usli = db.session.query(USLI).filter(USLI.uid==uid).first()
        if usli and current_user.uid == uid:
            profile = db.session.query(UserProfile).filter(UserProfile.uid==uid).first()
            if profile:
                return self.__getProfileSuccessResponse(profile)
            else:
                return self.__createProfile(usli)
        else:
            return self.__getProfileFailResponse(5000)

    def __createProfile(self, usli: USLI):
        profile = UserProfile(uid=usli.uid,
                          email=usli.email,
                          full_name=usli.full_name,
                          photo="",
                          caption="",
                          link="",
                          created_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(profile)
        db.session.commit()
        return self.__getProfileSuccessResponse(profile)

    def __getProfileSuccessResponse(self, profile: UserProfile):
        time = datetime.now(timezone.utc)

        data = ProfileBase(uid=profile.uid).get_ProfileDataResponseSchema()

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
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
        meta.response_id = uuid.uuid4().hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = ProfileResponseSchema()
        response.meta = meta
        response.data = None
        return response