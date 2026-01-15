from marshmallow import Schema, fields, validate

class PostCommentListRequestSchema(Schema):
    post_id = fields.Str(required=True, validate=validate.Length(min=1))
    limit = fields.Int(required=True)
    offset = fields.Int(required=True)