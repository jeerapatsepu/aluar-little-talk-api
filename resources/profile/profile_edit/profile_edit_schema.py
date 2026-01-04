from marshmallow import Schema, fields, validate

from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

class ProfileEditRequestSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    website = fields.Str(required=True, validate=validate.Length(min=1))
    bio = fields.Str(required=True, validate=validate.Length(min=1))

class ProfileEditResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, only=("name", "uid", "photo", "caption", "link", "email"), dump_only=True, many=False)