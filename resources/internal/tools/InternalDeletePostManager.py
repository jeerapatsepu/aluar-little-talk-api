import os
from app.models.comment_model import CommentModel
from app.models.post import Post, PostContent, PostImageContent
from app.models.post_bookmark_model import PostBookmarkModel
from app.models.post_like_model import PostLikeModel
from app.models.post_repost_model import PostRepostModel
from resources.internal.tools.InternalDeleteCommentManager import InternalDeleteCommentManager
from app.extensions import db
from app.extensions import boto_client

class InternalDeletePostManager:
    def __init__(self, post_id: str):
        self.__post_id = post_id

    def delete_post(self, owner_uid: str):
        PostContent.query.filter_by(post_id=self.__post_id).delete(synchronize_session=False)
        PostImageContent.query.filter_by(post_id=self.__post_id).delete(synchronize_session=False)
        PostLikeModel.query.filter_by(post_id=self.__post_id).delete(synchronize_session=False)
        PostBookmarkModel.query.filter_by(post_id=self.__post_id).delete(synchronize_session=False)
        PostRepostModel.query.filter_by(post_id=self.__post_id).delete(synchronize_session=False)
        comment_list = CommentModel.query.filter_by(post_id=self.__post_id).all()
        for comment in comment_list:
            InternalDeleteCommentManager(comment_id=comment.comment_uid).deleteComment(owner_uid=owner_uid)
        Post.query.filter_by(post_id=self.__post_id, owner_uid=owner_uid).delete(synchronize_session=False)
        db.session.commit()
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "posts/" + self.__post_id
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