from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class AuthAppleCreateRequestSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.Str(required=True)
    user_identifier = fields.Str(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        if len(data["password"]) < 8:
            raise ValidationError("Password must be more than 8 characters", "password")

class AuthLoginDataResponseSchema(Schema):
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)

class AuthLoginResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(AuthLoginDataResponseSchema, dump_only=True)