import os
from models.post.comment_model import CommentModel
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_like_model import PostLikeModel
from models.post.post_repost_model import PostRepostModel
from resources.internal.tools.InternalDeleteCommentManager import InternalDeleteCommentManager
from app.shared import db
from app.s3 import client

class InternalDeletePostManager:
    def __init__(self, post_id: str):
        self.__post_id = post_id

    def delete_post(self, owner_uid: str):
        PostContent.query.filter_by(post_id=self.__post_id).delete()
        PostImageContent.query.filter_by(post_id=self.__post_id).delete()
        PostLikeModel.query.filter_by(post_id=self.__post_id).delete()
        PostBookmarkModel.query.filter_by(post_id=self.__post_id).delete()
        PostRepostModel.query.filter_by(post_id=self.__post_id).delete()
        comment_list = CommentModel.query.filter_by(post_id=self.__post_id).all()
        for comment in comment_list:
            InternalDeleteCommentManager(comment_id=comment.comment_uid).deleteComment(owner_uid=owner_uid)
        Post.query.filter_by(post_id=self.__post_id, owner_uid=owner_uid).delete()
        db.session.commit()
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "posts/" + self.__post_id
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

    def delete_all_posts_of_user(self, owner_uid: str):
        PostContent.query.filter_by(post_id=self.__post_id).delete()
        PostImageContent.query.filter_by(post_id=self.__post_id).delete()
        PostLikeModel.query.filter_by(post_id=self.__post_id).delete()
        PostBookmarkModel.query.filter_by(post_id=self.__post_id).delete()
        PostRepostModel.query.filter_by(post_id=self.__post_id).delete()