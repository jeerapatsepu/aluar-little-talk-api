from marshmallow import Schema, fields

from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.post_response_schema import PostResponseSchema

class SearchRecommentPostListRequestSchema(Schema):
    offset = fields.Integer(required=True)
    limit = fields.Integer(required=True)

class SearchRecommentPostListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(PostResponseSchema, only=("post_id", "owner_image", "owner_name", "owner_uid", "visibility", "type", "original_post_id", "created_date_timestamp", "updated_date_timestamp", "is_owner", "is_like", "like_count", "is_bookmark", "is_repost", "repost_count", "comment_count", "contents", "is_see_more"), dump_only=True, many=True)