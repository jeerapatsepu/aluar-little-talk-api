import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
from models.post.post import Post
from models.post.post_repost_model import PostRepostModel
from resources.base.short_post import ShortPost
from resources.profile.repost.profile_reposts_response import ProfileRePostsResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.profile.profile_posts_request_schema import ProfilePostsRequestSchema

blp = Blueprint("ProfileRePosts", __name__, description="Profile RePosts")

@blp.route("/profile/reposts")
class ProfileRePosts(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfileRePostsResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]
        reposts = PostRepostModel.query.filter_by(user_uid=uid).order_by(PostRepostModel.created_date_timestamp).offset(offset).limit(limit).all()
        reposts.sort(key=self.__sortRePostsList, reverse=True)
        new_posts = self.__getShortPost(posts=reposts)
        return self.__getPofilePostsSuccessResponse(new_posts)

    def __getShortPost(self, reposts: list):
        short_post_list = []
        for repost in reposts:
            short_post = ShortPost(post_id=repost.post_id).get_post()
            short_post_list.append(short_post)
        return short_post_list

    def __sortRePostsList(self, e):
        return e.created_date_timestamp

    def __getPofilePostsSuccessResponse(self, posts):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfileRePostsResponseSchema()
        response.meta = meta
        response.data = posts
        return response
