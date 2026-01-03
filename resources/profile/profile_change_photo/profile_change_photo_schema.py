from marshmallow import Schema, fields, validate

from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

class ProfileChangePhotoRequestSchema(Schema):
    image = fields.Str(required=True)

class ProfileChangePhotoResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, only=("name", "uid", "photo", "caption", "link", "email"), dump_only=True, many=True)