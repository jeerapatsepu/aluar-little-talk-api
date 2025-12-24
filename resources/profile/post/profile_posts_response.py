
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post.post_response_schema import PostResponseSchema
from marshmallow import Schema, fields

class ProfilePostsResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(PostResponseSchema, dump_only=True, many=True)