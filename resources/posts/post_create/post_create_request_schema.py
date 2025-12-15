from marshmallow import Schema, ValidationError, fields, validates_schema, validate
from schemas.meta import MetaSchema

class PostCreateDataImageRequestSchema(Schema):
    index = fields.Integer(required=True)
    data = fields.Str(required=True)

class PostCreateDataRequestSchema(Schema):
    index = fields.Integer(required=True)
    text = fields.Str(required=True, validate=validate.Length(min=1))
    text_type = fields.Str(validate=validate.OneOf(["TITLE", "SUB_TITLE", "TEXT", "QUOTE"]), required=True) # TITLE, SUB_TITLE, TEXT, QUOTE
    type = fields.Str(validate=validate.OneOf(["TEXT", "IMAGE", "SECTION", "LINK"]), required=True) # TEXT, IMAGE, SECTION, LINK
    images = fields.Nested(PostCreateDataImageRequestSchema, required=True, many=True)
    # images = fields.List(fields.Str(), required=True)

class PostCreateRequestSchema(Schema):
    visibility = fields.Str(validate=validate.OneOf(["PUBLIC", "FRIENDS", "PRIVATE"]), required=True)
    data = fields.Nested(PostCreateDataRequestSchema, required=True, many=True)

class PostsCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(PostCreateRequestSchema, dump_only=True)