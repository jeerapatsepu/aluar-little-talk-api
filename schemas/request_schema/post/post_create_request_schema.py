from marshmallow import Schema, fields, validate
from schemas.reponse_schema.post.post.post_response_schema import PostDataSchema

class PostCreateRequestSchema(Schema):
    visibility = fields.Str(validate=validate.OneOf(["PUBLIC", "FRIENDS", "PRIVATE"]), required=True)
    data = fields.Nested(PostDataSchema,
                         only=("index", "text", "text_type", "type", "images"),
                         required=True,
                         many=True,
                         validate=validate.Length(min=1))