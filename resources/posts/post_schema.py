from marshmallow import Schema, fields, validate
from schemas.meta import MetaSchema

class PostActionRequestSchema(Schema):
    post_id = fields.Str(required=True, validate=validate.Length(min=1))

class PostActionResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)