from marshmallow import Schema, fields

class AuthAppleLoginRequestSchema(Schema):
    user_identifier = fields.Str(required=True)