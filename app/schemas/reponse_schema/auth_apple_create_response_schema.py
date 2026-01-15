from marshmallow import Schema, validate, fields
from app.schemas.reponse_schema.meta import MetaSchema

class AuthAppleCreateDataResponseSchema(Schema):
    access_token = fields.Str(dump_only=True, validate=validate.Length(min=1))
    refresh_token = fields.Str(dump_only=True, validate=validate.Length(min=1))
    uid = fields.Str(dump_only=True, validate=validate.Length(min=1))

class AuthAppleCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(AuthAppleCreateDataResponseSchema, only=("access_token", "refresh_token", "uid"), dump_only=True)