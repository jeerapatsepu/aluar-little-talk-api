from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.profile.user_profile import UserProfile
from resources.search.search_user_list.search_user_list_schema import SearchUserListRequestSchema, SearchUserListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostRepostUserList", __name__, description="Post Repost User List")

@blp.route("/search/user/list")
class PostRepostUserList(MethodView):
    @blp.arguments(SearchUserListRequestSchema)
    @blp.response(200, SearchUserListResponseSchema)
    def post(self, request):
        search = request["search"]
        offset = request["offset"]
        limit = request["limit"]
        profile_list = UserProfile.query.filter_by(full_name=search).order_by(UserProfile.full_name).offset(offset=offset).limit(limit=limit).all()
        return self.__getSuccessResponseSchema(profile_list=profile_list)

    def __getSuccessResponseSchema(self, profile_list: list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = SearchUserListResponseSchema()
        response.meta = meta
        response.data = profile_list
        return response