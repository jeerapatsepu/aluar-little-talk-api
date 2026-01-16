        
from flask_jwt_extended import current_user
from sqlalchemy import and_, desc
from app.models.comment_like_model import CommentLikeModel
from app.models.comment_model import CommentModel
from app.models.user_profile import UserProfile
from app.routes.post_route.comment.comment_reply_list.comment_reply_list_schema import CommentReplyListResponseSchema
from app.schemas.reponse_schema.comment_response_schema import CommentResponseSchema
from app.utils.resposne_helper import get_meta_sucess_response


def get_reply_list(request):
    comment_id = request["comment_id"]
    offset = request["offset"]
    limit = request["limit"]
    reply_list = CommentModel.query.order_by(desc(CommentModel.created_date_timestamp)).filter(CommentModel.parent_comment_uid == comment_id).offset(offset).limit(limit).all()
    return __get_reply_list_response(list(map(__map_reply_list, reply_list)))

def __map_reply_list(reply: CommentModel):
    reply_schema = CommentResponseSchema()
    profile = UserProfile.query.filter(UserProfile.uid == reply.user_uid).first()
    reply_to_profile = UserProfile.query.filter(UserProfile.uid == reply.reply_uid).first()
    reply_schema.comment_id = reply.comment_uid
    reply_schema.parent_comment_id = reply.parent_comment_uid
    reply_schema.owner_image = profile.photo
    reply_schema.owner_name = profile.full_name
    reply_schema.owner_uid = reply.user_uid
    reply_schema.reply_image = reply_to_profile.photo
    reply_schema.reply_name = reply_to_profile.full_name
    reply_schema.reply_uid = reply.reply_uid
    reply_schema.post_id = reply.post_id
    reply_schema.text = reply.text
    reply_schema.image_url = reply.image_url
    reply_schema.created_date_timestamp = reply.created_date_timestamp
    reply_schema.updated_date_timestamp = reply.updated_date_timestamp
    reply_schema.reply_list = []
    reply_schema.is_see_reply_more = False
    reply_schema.like_count = CommentLikeModel.query.filter(CommentLikeModel.comment_id == reply.comment_uid).count()
    try:
        reply_schema.is_owner = current_user.uid == reply.user_uid
        reply_schema.is_like = CommentLikeModel.query.filter(and_(CommentLikeModel.user_uid == current_user.uid, CommentLikeModel.comment_id == reply.comment_uid)).first() is not None
    except Exception:
        reply_schema.is_owner = False
        reply_schema.is_like = False
    return reply_schema

def __get_reply_list_response(data: list):
    response = CommentReplyListResponseSchema()
    response.meta = get_meta_sucess_response()
    response.data = data
    return response