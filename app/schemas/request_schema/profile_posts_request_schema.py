from marshmallow import Schema, fields, validate

class ProfilePostsRequestSchema(Schema):
    uid = fields.Str(required=True, validate=validate.Length(min=1))
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    filter = fields.Str(validate=validate.OneOf(["ALL", "REPOSTS", "BOOKMARKS", "PRIVATE"]), required=False)