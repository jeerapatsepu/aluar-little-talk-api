from flask_jwt_extended import current_user
from models.post.comment_like_model import CommentLikeModel
from models.post.comment_model import CommentModel
from models.user_profile import UserProfile
from schemas.reponse_schema.post.comment_response_schema import CommentReplySchema, CommentResponseSchema

class FullComment:
    def __init__(self, comment_id: str):
        self.__comment_id = comment_id
    
    def get_comment(self):
        comment = CommentModel.query.filter_by(comment_uid=self.__comment_id).one()
        return self.__getCommentResponseSchema(comment=comment)
    
    def __getCommentResponseSchema(self, comment: CommentModel):
        owner_profile = UserProfile.query.filter_by(uid=comment.user_uid).first()
        like_list = CommentLikeModel.query.filter_by(comment_id=comment.comment_uid).all()
        comment_schema = CommentResponseSchema()
        comment_schema.comment_id = comment.comment_uid
        comment_schema.parent_comment_id = comment.parent_comment_uid
        comment_schema.owner_image = owner_profile.photo
        comment_schema.owner_name = owner_profile.full_name
        comment_schema.owner_uid = owner_profile.uid
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
        self.__getReplyList(comment_schema=comment_schema)
        return comment_schema
    
    def __getReplyList(self, comment_schema: CommentResponseSchema):
        schema_list = []
        reply_list = CommentModel.query.filter_by(parent_comment_uid=self.__comment_id).order_by(CommentModel.created_date_timestamp).offset(0).limit(4).all()
        comment_schema.is_see_reply_more = len(reply_list) > 3
        if len(reply_list) > 3:
            reply_list.pop()
        for reply in reply_list:
            owner_profile = UserProfile.query.filter_by(uid=reply.user_uid).first()
            schema = CommentReplySchema()
            schema.comment_id = reply.comment_uid
            schema.parent_comment_id = reply.parent_comment_uid
            schema.owner_image = owner_profile.photo
            schema.owner_name = owner_profile.full_name
            schema.owner_uid = owner_profile.uid
            schema.post_id = reply.post_id
            try:
                schema.is_owner = current_user.uid == owner_profile.uid
            except Exception:
                schema.is_owner = False
            schema.created_date_timestamp = reply.created_date_timestamp
            schema.updated_date_timestamp = reply.updated_date_timestamp
            schema.text = reply.text
            schema.image_url = reply.image_url
            like_list = CommentLikeModel.query.filter_by(comment_id=reply.comment_uid).all()
            schema.like_count = len(like_list)
            schema.is_like = len(list(filter(lambda x: x.user_uid == current_user.uid, like_list))) > 0
            parent_comment = CommentModel.query.filter_by(comment_uid=reply.parent_comment_uid).first()
            parent_comment_profile = UserProfile.query.filter_by(uid=parent_comment.user_uid).first()
            schema.reply_image = parent_comment_profile.photo
            schema.reply_name = parent_comment_profile.full_name
            schema.reply_uid = parent_comment_profile.uid
            schema_list.append(schema)
        comment_schema.reply_list = schema_list