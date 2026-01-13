from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.post import PostContent
from models.profile.user_profile import UserProfile
from models.profile_recommendations import ProfileRecommendation
from resources.base.profile import ProfileBase
from resources.manager.image_manager import ImageManager
from resources.search.search_recomment_user_list.search_recomment_user_list_schema import SearchRecommentUserListRequestSchema, SearchRecommentUserListResponseSchema
from schemas.reponse_schema.meta import MetaSchema
import logging

from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

blp = Blueprint("SearchRecommentUserList", __name__, description="Search Recomment User List")

@blp.route("/search/recomment/user/list")
class SearchRecommentUserList(MethodView):
    @blp.arguments(SearchRecommentUserListRequestSchema)
    @blp.response(200, SearchRecommentUserListResponseSchema)
    def post(self, request):
        profile_list = self.__get_profile_list(request=request)
        return self.__getSuccessResponseSchema(data=profile_list)

    def __get_profile_list(self, request):
        offset = request["offset"]
        limit = request["limit"]
        profile_recommendation_list = ProfileRecommendation.query.offset(offset=offset).limit(limit=limit).all()
        if len(profile_recommendation_list) > 0:
            map_profile_list = list(map(self.__map_profile_list, profile_recommendation_list))
            return map_profile_list
        else:
            profile_list = UserProfile.query.offset(offset=offset).limit(limit=limit).all()
            map_profile_list = list(map(self.__map_profile_list, profile_list))
            return map_profile_list
    
    def __map_profile_list(self, profile):
        map_profile = ProfileBase(uid=profile.uid).get_ProfileDataResponseSchema()
        return map_profile

    def __getSuccessResponseSchema(self, data: list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = SearchRecommentUserListResponseSchema()
        response.meta = meta
        response.data = data
        return response