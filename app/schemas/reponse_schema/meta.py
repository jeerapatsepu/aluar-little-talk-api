from marshmallow import Schema, fields
from app.schemas.reponse_schema.error import ErrorSchema

class MetaSchema(Schema):
    response_id = fields.Str()
    response_code = fields.Int()
    response_date = fields.Str()
    response_timestamp = fields.Str()
    error = fields.Nested(ErrorSchema, only=("title", "message"), dump_only=True)

class MetaResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)