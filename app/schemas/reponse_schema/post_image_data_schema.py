from marshmallow import Schema, fields

class PostImageDataSchema(Schema):
    index = fields.Integer(required=True)
    data = fields.Str(required=True)