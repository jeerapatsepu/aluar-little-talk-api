from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_create_request_schema import PostCreateRequestSchema
from marshmallow import Schema, fields

class PostsCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(PostCreateRequestSchema, dump_only=True)