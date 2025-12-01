from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class ProfileRequestSchema(Schema):
    uid = fields.Str(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        if len(data["uid"]) <= 0:
            raise ValidationError("UID must be not empty", "uid")

class ProfileDataResponseSchema(Schema):
    name = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)
    caption = fields.Str(dump_only=True)
    link = fields.Str(dump_only=True)

class ProfileResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, dump_only=True)