from marshmallow import Schema, fields, validate

class HomeFeedRequestSchema(Schema):
    filter = fields.Str(validate=validate.OneOf(["ALL", "FOLLOW", "FRIENDS"]), required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)