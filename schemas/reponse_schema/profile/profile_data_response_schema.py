from marshmallow import Schema, fields

class ProfileDataResponseSchema(Schema):
    name = fields.Str(dump_only=True)
    relationship_status = fields.Str(dump_only=True) # e.g., 'FOLLOW', 'BLOCKED', 'FRIEND'
    uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)
    caption = fields.Str(dump_only=True)
    link = fields.Str(dump_only=True)