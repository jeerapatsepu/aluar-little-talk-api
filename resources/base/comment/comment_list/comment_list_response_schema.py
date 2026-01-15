from app.schemas.reponse_schema.meta import MetaSchema
from marshmallow import Schema, fields
from app.schemas.reponse_schema.comment_response_schema import CommentResponseSchema

class PostsCommentListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(CommentResponseSchema, only=("comment_id", "parent_comment_id", "owner_image", "owner_name", "owner_uid", "post_id", "is_owner", "text", "image_url", "created_date_timestamp", "updated_date_timestamp", "reply_list", "is_see_reply_more", "is_like", "like_count"), dump_only=True, many=True)