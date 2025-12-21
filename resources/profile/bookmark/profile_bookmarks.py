import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
from models.post.post_bookmark_model import PostBookmarkModel
from resources.base.short_post import ShortPost
from resources.profile.bookmark.profile_bookmarks_response import ProfileBookmarksResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.profile.profile_posts_request_schema import ProfilePostsRequestSchema

blp = Blueprint("ProfileBookmarks", __name__, description="Profile Bookmarks")

@blp.route("/profile/bookmarks")
class ProfileBookmarks(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfileBookmarksResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]
        bookmarks = PostBookmarkModel.query.filter_by(user_uid=uid).order_by(PostBookmarkModel.created_date_timestamp).offset(offset).limit(limit).all()
        bookmarks.sort(key=self.__sortRePostsList, reverse=True)
        new_posts = self.__getShortPost(bookmarks=bookmarks)
        return self.__getPofilePostsSuccessResponse(new_posts)

    def __getShortPost(self, bookmarks: list):
        short_post_list = []
        for repost in bookmarks:
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

        response = ProfileBookmarksResponseSchema()
        response.meta = meta
        response.data = posts
        return response
