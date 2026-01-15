import os
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from app.extensions import boto_client
from app.extensions import db

class InternalDeleteCommentManager:
    def deleteAllCommentOfPost(self, post_id: str):
        self.__deleteCommentModel(post_id=post_id)

    def __deleteCommentModel(self, post_id: str):
        comment_list = CommentModel.query.filter_by(post_id=post_id).all()
        CommentModel.query.filter_by(post_id=post_id).delete(synchronize_session=False)
        db.session.commit()
        for comment in comment_list:
            CommentLikeModel.query.filter_by(post_id=post_id).delete(synchronize_session=False)
            db.session.commit()
            self.__deleteCommentImage(comment_id=comment.comment_uid)

    def __deleteCommentImage(self, comment_id: str):
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "comments/" + comment_id
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