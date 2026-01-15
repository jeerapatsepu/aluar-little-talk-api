from marshmallow import Schema, validate, fields

class ProfileRequestSchema(Schema):
    uid = fields.Str(required=True, validate=validate.Length(min=1))