from marshmallow import Schema, fields, validate

class AuthAppleCreateRequestSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    user_identifier = fields.Str(required=True, validate=validate.Length(min=1))