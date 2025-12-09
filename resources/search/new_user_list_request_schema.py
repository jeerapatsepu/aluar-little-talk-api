from marshmallow import Schema, fields, validates_schema
from schemas.meta import MetaSchema

class NewUserListRequestSchema(Schema):
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)

class NewUserListDataResponseSchema(Schema):
    full_name = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)

class NewUserListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(NewUserListDataResponseSchema, dump_only=True, many=True)