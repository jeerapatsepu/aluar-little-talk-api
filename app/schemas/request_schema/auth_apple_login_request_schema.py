from marshmallow import Schema, fields, validate

class AuthAppleLoginRequestSchema(Schema):
    user_identifier = fields.Str(required=True, validate=validate.Length(min=1))