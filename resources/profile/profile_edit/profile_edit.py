import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone
from models.profile.user_profile import UserProfile
from app.shared import db
from resources.base.profile import ProfileBase
from resources.profile.profile_edit.profile_edit_schema import ProfileEditRequestSchema, ProfileEditResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("ProfileEdit", __name__, description="Profile Edit")

@blp.route("/profile/edit")
class ProfileEdit(MethodView):
    @jwt_required()
    @blp.arguments(ProfileEditRequestSchema)
    @blp.response(200, ProfileEditResponseSchema)
    def post(self, request):
        self.__editProfile(request=request)
        return self.__getSuccessResponse(uid=current_user.uid)
    
    def __editProfile(self, request):
        name = request["name"]
        website = request["website"]
        bio = request["bio"]
        profile = UserProfile.query.filter_by(uid=current_user.uid).one()
        profile.full_name = name
        profile.link = website
        profile.caption = bio
        db.session.commit()

    def __getSuccessResponse(self, uid: str):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        data = ProfileBase(uid=uid).get_ProfileDataResponseSchema()

        response = ProfileEditResponseSchema()
        response.meta = meta
        response.data = data
        return response