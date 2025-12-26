from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
import uuid
from models.post.comment_model import CommentModel
from models.post.post_repost_model import PostRepostModel
from models.user_profile import UserProfile
from resources.base.post.post_like_list.post_like_list_schema import PostLikeListRequestSchema, PostLikeListResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("PostRepostUserList", __name__, description="Post Repost User List")

@blp.route("/post/repost/user/list")
class PostRepostUserList(MethodView):
    @blp.arguments(PostLikeListRequestSchema)
    @blp.response(200, PostLikeListResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        offset = request["offset"]
        limit = request["limit"]
        repost_list = PostRepostModel.query.filter_by(post_id=post_id).order_by(PostRepostModel.created_date_timestamp).offset(offset=offset).limit(limit=limit).all()
        uid_list = list(set(list(map(self.__map_list_get_uid, repost_list))))
        profile_list = self.__getProfileList(uid_list=uid_list)
        return self.__getPostLikeListResponseSchema(profile_list=profile_list)
    
    def __map_list_get_uid(self, val):
        return val.user_uid
    
    def __getProfileList(self, uid_list: list):
        profile_list = []
        for uid in uid_list:
            profile = UserProfile.query.filter_by(uid=uid).one()
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