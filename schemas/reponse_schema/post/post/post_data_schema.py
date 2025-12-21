
from marshmallow import Schema, fields, validate
from schemas.reponse_schema.post.post.post_image_data_schema import PostImageDataSchema

class PostDataSchema(Schema):
    index = fields.Integer(required=True)
    text = fields.Str(required=True)
    text_type = fields.Str(validate=validate.OneOf(["TITLE", "SUB_TITLE", "TEXT", "QUOTE", ""]), required=True) # TITLE, SUB_TITLE, TEXT, QUOTE
    type = fields.Str(validate=validate.OneOf(["TEXT", "IMAGE", "SECTION", "LINK"]), required=True) # TEXT, IMAGE, SECTION, LINK
    images = fields.Nested(PostImageDataSchema, required=True, many=True)
    # images = fields.List(fields.Str(), required=True)