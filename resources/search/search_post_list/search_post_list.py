from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.post import PostContent
from models.profile.user_profile import UserProfile
from resources.search.search_post_list.search_post_list_schema import SearchPostListDataSchema, SearchPostListRequestSchema, SearchPostListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("SearchPostList", __name__, description="Search Post List")

@blp.route("/search/post/list")
class SearchPostList(MethodView):
    @blp.arguments(SearchPostListRequestSchema)
    @blp.response(200, SearchPostListResponseSchema)
    def post(self, request):
        content_list = self.__get_content_list(request=request)
        return self.__get_success_esponse_schema(content_list=content_list)

    def __get_content_list(self, request):
        search = request["search"]
        offset = request["offset"]
        limit = request["limit"]
        content_list = PostContent.query.order_by(PostContent.owner_uid).filter(PostContent.text.contains(search)).offset(offset=offset).limit(limit=limit).all()
        content_data_list = list(map(self.__map_content_list, content_list))
        return content_data_list
    
    def __map_content_list(self, content: SearchPostListDataSchema):
        profile = UserProfile.query.filter(UserProfile.uid == content.owner_uid).first()
        if profile:
            content.owner_name = profile.full_name
            content.owner_photo = profile.photo
        return content
    
    def __get_success_esponse_schema(self, content_list: list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = SearchPostListResponseSchema()
        response.meta = meta
        response.data = content_list
        return response