from marshmallow import Schema, fields
from schemas.error import ErrorSchema

class MetaSchema(Schema):
    response_id = fields.Str()
    response_code = fields.Int()
    response_date = fields.Str()
    response_timestamp = fields.Str()
    error = fields.Nested(ErrorSchema(), dump_only=True)

class MetaResponseSchema(Schema):
    meta = fields.Nested(MetaSchema(), dump_only=True)