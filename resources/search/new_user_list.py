import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
from models.profile.user_profile import UserProfile
from resources.search.new_user_list_request_schema import NewUserListRequestSchema, NewUserListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("NewUserList", __name__, description="New User List")

@blp.route("/search/new_user_list")
class NewUserList(MethodView):
    @blp.arguments(NewUserListRequestSchema)
    @blp.response(200, NewUserListResponseSchema)
    def post(self, request):
        offset = request["offset"]
        limit = request["limit"]
        new_profiles: list = []
        profiles = UserProfile.query.offset(offset).limit(limit).all()
        print(profiles.count)
        for item in profiles:
            dt = datetime.fromtimestamp(item.created_date_timestamp).strftime("%d")
            now = datetime.now().strftime("%d")
            if now == dt:
                new_profiles.append(item)
        return self.getPofilePostsSuccessResponse(new_profiles)

    def getPofilePostsSuccessResponse(self, profiles):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = NewUserListResponseSchema()
        response.meta = meta
        response.data = profiles
        return response