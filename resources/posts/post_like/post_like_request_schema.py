from marshmallow import Schema, ValidationError, fields, validates_schema, validate
from schemas.meta import MetaSchema

class PostLikeRequestSchema(Schema):
    post_id = fields.Str(required=True)

class PostLikeResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)