from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema
from marshmallow import Schema, fields

class ProfileResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, dump_only=True)