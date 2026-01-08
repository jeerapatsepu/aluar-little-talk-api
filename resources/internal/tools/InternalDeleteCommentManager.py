import os
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from app.s3 import client
from app.shared import db

class InternalDeleteCommentManager:
    def __init__(self, comment_id: str):
        self.__comment_id = comment_id
    
    def deleteComment(self, owner_uid: str):
        self.__deleteCommentModel(comment_id=self.__comment_id, owner_uid=owner_uid)

    def __deleteCommentModel(self, comment_id: str, owner_uid: str):
        comment = CommentModel.query.filter_by(comment_uid=comment_id).first()
        if comment and comment.user_uid == owner_uid:
            self.__deleteComment(comment_id=comment_id, owner_uid=owner_uid)
            self.__deleteReply(comment_id=comment_id)
            db.session.commit()

    def __deleteComment(self, comment_id: str, owner_uid: str):
        CommentLikeModel.query.filter_by(comment_id=comment_id).delete(synchronize_session=False)
        comment_list = CommentModel.query.filter_by(comment_uid=comment_id).all()
        for comment in comment_list:
            self.__deleteCommentImage(comment_id=comment.comment_uid)
        CommentModel.query.filter_by(comment_uid=comment_id, user_uid=owner_uid).delete(synchronize_session=False)

    def __deleteReply(self, comment_id: str):
        reply_list = CommentModel.query.filter_by(parent_comment_uid=comment_id).all()
        for reply in reply_list:
            self.__deleteCommentImage(comment_id=reply.comment_uid)
            CommentLikeModel.query.filter_by(comment_id=reply.comment_uid).delete(synchronize_session=False)
        CommentModel.query.filter_by(parent_comment_uid=comment_id).delete(synchronize_session=False)

    def __deleteCommentImage(self, comment_id: str):
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "comments/" + comment_id
            response = client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )
            if "Contents" in response:
                client.delete_objects(
                    Bucket=bucket,
                    Delete={
                        "Objects": [{"Key": obj["Key"]} for obj in response["Contents"]]
                    }
                )
        except Exception:
            pass