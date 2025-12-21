from marshmallow import Schema, fields, validate

class PostActionRequestSchema(Schema):
    post_id = fields.Str(required=True, validate=validate.Length(min=1))