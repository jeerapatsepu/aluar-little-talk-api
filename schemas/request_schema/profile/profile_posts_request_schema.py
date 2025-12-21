from marshmallow import Schema, fields, validate

class ProfilePostsRequestSchema(Schema):
    uid = fields.Str(required=True, validate=validate.Length(min=1))
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)