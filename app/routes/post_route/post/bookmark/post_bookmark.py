from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from app.models.post_bookmark_model import PostBookmarkModel
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.post_action_response_schema import PostActionResponseSchema
from app.schemas.request_schema.post_action_request_schema import PostActionRequestSchema

blp = Blueprint("PostBookmark", __name__, description="Post Bookmark")

@blp.route("/post/bookmark")
class PostBookmark(MethodView):
    @jwt_required()
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = current_user.uid
        bookmark = PostBookmarkModel.query.filter_by(post_id=post_id, user_uid=owner_uid).first()
        if not bookmark:
            self.__createPostBookmarkModel(post_id, owner_uid)
        return self.__getPostsBookmarkResponseSchema()

    def __createPostBookmarkModel(self, post_id: str, owner_uid: str):
        post_bookmark = PostBookmarkModel(post_id=post_id,
                                      user_uid=owner_uid,
                                      created_date_timestamp=int(datetime.now(timezone.utc).timestamp()),
                                      updated_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(post_bookmark)
        db.session.commit()

    def __getPostsBookmarkResponseSchema(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostActionResponseSchema()
        response.meta = meta
        return response