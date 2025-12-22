from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_like_model import PostLikeModel
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_action_request_schema import PostActionRequestSchema
from app.s3 import client

blp = Blueprint("PostDelete", __name__, description="Post Delete")

@blp.route("/post/delete")
class PostDelete(MethodView):
    @jwt_required()
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, PostActionResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        self.__deletePostModel(post_id=post_id)
        return self.__getPostsLikeResponseSchema()
    
    def __deletePostModel(self, post_id: str):
        owner_uid = current_user.uid
        Post.query.filter_by(post_id=post_id, owner_uid=owner_uid).delete(synchronize_session=False)
        PostContent.query.filter_by(post_id=post_id).delete(synchronize_session=False)
        PostImageContent.query.filter_by(post_id=post_id).delete(synchronize_session=False)
        db.session.commit()
        try: 
            client.delete_directory(
                DirectoryId='posts/' + post_id
            ) 
        except Exception:
            pass

    def __getPostsLikeResponseSchema(self):
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