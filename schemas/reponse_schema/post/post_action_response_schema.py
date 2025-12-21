from marshmallow import Schema, fields
from schemas.reponse_schema.meta import MetaSchema

class PostActionResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)