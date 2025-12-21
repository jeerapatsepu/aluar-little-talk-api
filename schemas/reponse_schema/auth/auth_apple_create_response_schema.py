from marshmallow import Schema, validate, fields
from schemas.reponse_schema.meta import MetaSchema

class AuthAppleCreateDataResponseSchema(Schema):
    access_token = fields.Str(dump_only=True, validate=validate.Length(min=1))
    refresh_token = fields.Str(dump_only=True, validate=validate.Length(min=1))
    uid = fields.Str(dump_only=True, validate=validate.Length(min=1))

class AuthAppleCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(AuthAppleCreateDataResponseSchema, dump_only=True)