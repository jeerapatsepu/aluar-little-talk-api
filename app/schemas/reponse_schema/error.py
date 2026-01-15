from marshmallow import Schema, fields

class ErrorSchema(Schema):
    title = fields.Str(required=True)
    message = fields.Str(required=True)