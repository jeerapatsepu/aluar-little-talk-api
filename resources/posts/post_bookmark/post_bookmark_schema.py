from marshmallow import Schema, fields
from schemas.meta import MetaSchema

class PostBookmarkRequestSchema(Schema):
    post_id = fields.Str(required=True)

class PostBookmarkResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)