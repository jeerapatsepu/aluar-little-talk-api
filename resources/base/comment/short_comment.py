from flask_jwt_extended import current_user
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from models.user_profile import UserProfile
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema

class ShortComment:
    def __init__(self, comment_id: str):
        self.__comment_id = comment_id
    
    def get_comment(self):
        comment = CommentModel.query.filter_by(comment_uid=self.__comment_id).one()
        return self.__getCommentResponseSchema(comment=comment)
    
    def __getCommentResponseSchema(self, comment: CommentModel):
        owner_profile = UserProfile.query.filter_by(uid=comment.user_uid).first()
        reply_profile = UserProfile.query.filter_by(uid=comment.reply_user_uid).first()
        like_list = CommentLikeModel.query.filter_by(comment_id=comment.comment_uid).all()
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
            comment_schema.is_like = len(list(filter(lambda x: x.user_uid == current_user.uid, like_list))) > 0
        except Exception:
            comment_schema.is_owner = False
            comment_schema.is_like = False
        comment_schema.like_count = len(like_list)
        comment_schema.text = comment.text
        comment_schema.image_url = comment.image_url
        comment_schema.created_date_timestamp = comment.created_date_timestamp
        comment_schema.updated_date_timestamp = comment.updated_date_timestamp
        comment_schema.reply_list = []
        return comment_schema