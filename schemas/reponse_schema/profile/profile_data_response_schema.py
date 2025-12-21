from marshmallow import Schema, fields

class ProfileDataResponseSchema(Schema):
    name = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)
    caption = fields.Str(dump_only=True)
    link = fields.Str(dump_only=True)