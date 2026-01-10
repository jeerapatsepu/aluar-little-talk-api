from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.post import PostContent
from models.profile.user_profile import UserProfile
from resources.base.profile import ProfileBase
from resources.manager.image_manager import ImageManager
from resources.search.search_recomment_user_list.search_recomment_user_list_schema import SearchRecommentUserListRequestSchema, SearchRecommentUserListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("SearchRecommentUserList", __name__, description="Search Recomment User List")

@blp.route("/search/recomment/user/list")
class SearchRecommentUserList(MethodView):
    @blp.arguments(SearchRecommentUserListRequestSchema)
    @blp.response(200, SearchRecommentUserListResponseSchema)
    def post(self, request):
        offset = request["offset"]
        limit = request["limit"]
        profile_list = UserProfile.query.offset(offset=offset).limit(limit=limit).all()
        profile_list = self.__filterProfileList(profile_list=profile_list)
        return self.__getSuccessResponseSchema(profile_list=profile_list)

    def __filterProfileList(self, profile_list: list):
        filtered_list = []
        for profile in profile_list:
            profile_schema = ProfileBase(uid=profile.uid).get_ProfileDataResponseSchema()
            if len(profile_schema.photo) > 0:
                verify_photo = ImageManager(profile_schema.photo).verify_profile_photo()
                content_list = PostContent.query.filter_by(owner_uid=profile_schema.uid).all()
                verify_content = len(list(filter(lambda x: len(x.text) >= 255, content_list))) > 5
                not_relationship = profile_schema.relationship_status != "FOLLOW" and profile_schema.relationship_status != "FRIEND"
                print(verify_photo, verify_content, not_relationship)
                if verify_photo and verify_content and not_relationship:
                    filtered_list.append(profile)
        if len(filtered_list) > 0:
            return filtered_list
        else:
            return self.__filterProfileListRemoveFollowed(profile_list=profile_list)
    
    def __filterProfileListRemoveFollowed(self, profile_list: list):
        filtered_list = profile_list
        for profile in profile_list:
            if profile.relationship_status == "FOLLOW" or profile.relationship_status == "FRIEND":
                filtered_list.remove(profile)
        return filtered_list

    def __getSuccessResponseSchema(self, profile_list: list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        data = []
        for profile in profile_list:
            profile_data = {
                "uid": profile.uid,
                "email": profile.email,
                "name": profile.full_name,
                "photo": profile.photo,
                "caption": profile.caption,
                "link": profile.link
            }
            data.append(profile_data)

        response = SearchRecommentUserListResponseSchema()
        response.meta = meta
        response.data = data
        return response