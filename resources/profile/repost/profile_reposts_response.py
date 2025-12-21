
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post.post_response_schema import PostResponseSchema
from marshmallow import Schema, fields

class ProfileRePostsResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(PostResponseSchema, dump_only=True, many=True)