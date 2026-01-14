from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.post import Post, PostContent
from models.profile.user_profile import UserProfile
from models.profile_recommendations import ProfileRecommendation
from resources.base.profile import ProfileBase
from resources.manager.image_manager import ImageManager
from resources.search.search_recomment_post_list.search_recomment_post_list_schema import SearchRecommentPostListRequestSchema, SearchRecommentPostListResponseSchema
from resources.short_post import ShortPost
from schemas.reponse_schema.meta import MetaSchema
import logging
from app.shared import bigqueryClient

from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

blp = Blueprint("SearchRecommentUserList", __name__, description="Search Recomment User List")

@blp.route("/search/recomment/post/list")
class SearchRecommentUserList(MethodView):
    @blp.arguments(SearchRecommentPostListRequestSchema)
    @blp.response(200, SearchRecommentPostListResponseSchema)
    def post(self, request):
        # profile_list = self.__get_post_list(request=request)
        query = """
        SELECT
        param.value.string_value AS post_id,
        COUNT(*) AS view_count
        FROM `project_id.analytics_xxxx.events_*`,
        UNNEST(event_params) AS param
        WHERE event_name = 'SEE_POST_DETAIL'
        AND param.key = 'post_id'
        GROUP BY post_id
        ORDER BY view_count DESC
        """

        df = bigqueryClient.query(query).to_dataframe()
        objects = df.to_dict("records")
        return self.__getSuccessResponseSchema(data=[])

    def __get_post_list(self, request):
        offset = request["offset"]
        limit = request["limit"]
        like_list = Post.query.filter().offset(offset=offset).limit(limit=limit).all()
        pass
    
    def __map_recommendation_list(self, post):
        map_post = ShortPost(post_id=post.post_id)
        return map_post

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

        response = SearchRecommentPostListResponseSchema()
        response.meta = meta
        response.data = data
        return response