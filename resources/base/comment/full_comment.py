from flask_jwt_extended import current_user
from models.post.comment_model import CommentModel
from models.post.post import Post, PostContent, PostImageContent
from models.post.post_bookmark_model import PostBookmarkModel
from models.post.post_like_model import PostLikeModel
from models.post.post_repost_model import PostRepostModel
from models.user_profile import UserProfile
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema
from schemas.reponse_schema.post.post.post_image_data_schema import PostImageDataSchema

class FullComment:
    def __init__(self, comment_id: str):
        self.__comment_id = comment_id
    
    def get_comment(self):
        comment = CommentModel.query.filter_by(comment_uid=self.__comment_id).one()
        return self.__getCommentResponseSchema(comment=comment)
    
    def __getCommentResponseSchema(self, comment: CommentModel):
        owner_profile = UserProfile.query.filter_by(uid=comment.user_uid).first()
        reply_profile = UserProfile.query.filter_by(uid=comment.reply_user_uid).first()
        comment_schema = CommentResponseSchema()
        comment_schema.comment_id = comment.comment_uid
        comment_schema.parent_comment_id = comment.parent_comment_uid
        comment_schema.owner_image = owner_profile.photo
        comment_schema.owner_name = owner_profile.full_name
        comment_schema.owner_uid = owner_profile.uid
        if reply_profile:
            comment_schema.reply_user_uid = reply_profile.uid
            comment_schema.reply_user_name = reply_profile.full_name
        comment_schema.post_id = comment.post_id
        try:
            comment_schema.is_owner = current_user.uid == owner_profile.uid
        except Exception:
            comment_schema.is_owner = False
        comment_schema.text = comment.text
        comment_schema.image_url = comment.image_url
        comment_schema.created_date_timestamp = comment.created_date_timestamp
        comment_schema.updated_date_timestamp = comment.updated_date_timestamp
        comment_schema.reply_list = []
        return comment_schema

    def __sortReplyList(self, e):
        return e.index