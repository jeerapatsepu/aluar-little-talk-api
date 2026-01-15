import os
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.extensions import db
from models.post.comment_model import CommentModel
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_like_model import PostLikeModel
from models.post.post_repost_model import PostRepostModel
from resources.base.comment.comment_delete_tool import CommentDeleteTool
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_action_request_schema import PostActionRequestSchema
from app.extensions import boto_client

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
        post = Post.query.filter_by(post_id=post_id).first()
        if post and post.owner_uid == owner_uid:
            PostContent.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            PostImageContent.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            PostLikeModel.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            PostBookmarkModel.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            PostRepostModel.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            comment_list = CommentModel.query.filter_by(post_id=post_id).all()
            for comment in comment_list:
                CommentDeleteTool(comment_id=comment.comment_uid).deleteComment()
            Post.query.filter_by(post_id=post_id, owner_uid=owner_uid).delete(synchronize_session=False)
            db.session.commit()
            try: 
                bucket = os.getenv("S3_BUCKET_NAME")
                prefix = "posts/" + post_id
                response = boto_client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix
                )
                if "Contents" in response:
                    boto_client.delete_objects(
                        Bucket=bucket,
                        Delete={
                            "Objects": [{"Key": obj["Key"]} for obj in response["Contents"]]
                        }
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