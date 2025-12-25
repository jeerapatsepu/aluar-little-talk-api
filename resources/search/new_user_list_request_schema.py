from marshmallow import Schema, fields
from schemas.reponse_schema.meta import MetaSchema

class NewUserListRequestSchema(Schema):
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)

class NewUserListDataResponseSchema(Schema):
    full_name = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)

class NewUserListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(NewUserListDataResponseSchema, only=("full_name", "uid", "photo"), dump_only=True, many=True)