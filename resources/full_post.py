import os
from flask_jwt_extended import current_user
from app.models.comment_model import CommentModel
from app.models.post import Post, PostContent, PostImageContent
from app.models.post_bookmark_model import PostBookmarkModel
from app.models.post_like_model import PostLikeModel
from app.models.post_repost_model import PostRepostModel
from app.models.user_profile import UserProfile
from resources.base.comment.comment_delete_tool import CommentDeleteTool
from app.schemas.reponse_schema.post_image_data_schema import PostImageDataSchema
from app.extensions import db, boto_client

class FullPost:
    def __init__(self, post_id: str):
        self.__post_id = post_id
    
    def get_post(self):
        post = Post.query.filter_by(post_id=self.__post_id).one()
        owner = UserProfile.query.filter_by(uid=post.owner_uid).first()
        new_post = self.__getContentList(owner, post)
        return new_post
    
    def delete_post(self, owner_uid: str):
        PostContent.query.filter_by(post_id=self.__post_id).delete()
        PostImageContent.query.filter_by(post_id=self.__post_id).delete()
        PostLikeModel.query.filter_by(post_id=self.__post_id).delete()
        PostBookmarkModel.query.filter_by(post_id=self.__post_id).delete()
        PostRepostModel.query.filter_by(post_id=self.__post_id).delete()
        comment_list = CommentModel.query.filter_by(post_id=self.__post_id).all()
        for comment in comment_list:
            CommentDeleteTool(comment_id=comment.comment_uid).deleteComment()
        Post.query.filter_by(post_id=self.__post_id, owner_uid=owner_uid).delete()
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
    
    def __getContentList(self, owner: UserProfile, post: Post):
        contents = PostContent.query.filter_by(post_id=post.post_id).all()
        contents.sort(key=self.__sortContentList)
        post.contents = self.__getImageContentList(contents)
        if owner:
            post.owner_name = owner.full_name
            post.owner_image = owner.photo
        like_list = PostLikeModel.query.filter_by(post_id=post.post_id).all()
        try:
            post.is_like = len(list(filter(lambda x: x.user_uid == current_user.uid, like_list))) > 0
            bookmark = PostBookmarkModel.query.filter_by(post_id=post.post_id, user_uid=current_user.uid).first()
            if bookmark:
                post.is_bookmark = True
            repost = PostRepostModel.query.filter_by(post_id=post.post_id, user_uid=current_user.uid).first()
            if repost:
                post.is_repost = True
            post.is_owner = current_user.uid == owner.uid
        except Exception:
            post.is_like = None
            post.is_bookmark = None
            post.is_repost = None
            post.is_owner = False
        post.like_count = len(like_list)
        post.repost_count = PostRepostModel.query.filter_by(post_id=post.post_id).count()
        post.comment_count = CommentModel.query.filter_by(post_id=post.post_id).count()
        return post
    
    def __getImageContentList(self, contentList: list):
        for content in contentList:
            if content.type == "IMAGE":
                image_list = PostImageContent.query.filter_by(content_id=content.content_id).all()
                image_list.sort(key=self.__sortContentList)
                image_respone_list = []
                for image in image_list:
                    image_response = PostImageDataSchema()
                    image_response.index = image.index
                    image_response.data = image.link
                    image_respone_list.append(image_response)
                content.images = image_respone_list
        return contentList
    
    def __sortContentList(self, e):
        return e.index