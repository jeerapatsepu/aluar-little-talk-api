from flask_jwt_extended import current_user
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_like_model import PostLikeModel
from models.post.post_repost_model import PostRepostModel
from models.user_profile import UserProfile
from schemas.reponse_schema.post.post.post_image_data_schema import PostImageDataSchema
class FullPost:
    def __init__(self, post_id: str):
        self.__post_id = post_id
    
    def get_post(self):
        post = Post.query.filter_by(post_id=self.__post_id).one()
        owner = UserProfile.query.filter_by(uid=post.owner_uid).first()
        new_post = self.__getContentList(owner, post)
        return new_post
    
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
        post.bookmark_count = PostBookmarkModel.query.filter_by(post_id=post.post_id).count()
        post.repost_count = PostRepostModel.query.filter_by(post_id=post.post_id).count()
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