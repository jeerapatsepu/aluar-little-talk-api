from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.post_like_model import PostLikeModel
from models.profile.user_profile import UserProfile
from resources.base.post.post_like_list.post_like_list_schema import PostLikeListRequestSchema, PostLikeListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostLikeList", __name__, description="Post Like List")

@blp.route("/post/like/list")
class PostLikeList(MethodView):
    @blp.arguments(PostLikeListRequestSchema)
    @blp.response(200, PostLikeListResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        offset = request["offset"]
        limit = request["limit"]
        like_list = PostLikeModel.query.filter_by(post_id=post_id).order_by(PostLikeModel.created_date_timestamp).offset(offset=offset).limit(limit=limit).all()
        profile_list = self.__getProfileList(like_list=like_list)
        return self.__getPostLikeListResponseSchema(profile_list=profile_list)

    def __getProfileList(self, like_list: list):
        profile_list = []
        for like in like_list:
            profile = UserProfile.query.filter_by(uid=like.user_uid).one()
            profile.name = profile.full_name
            profile_list.append(profile)
        return profile_list

    def __getPostLikeListResponseSchema(self, profile_list: list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostLikeListResponseSchema()
        response.meta = meta
        response.data = profile_list
        return response