from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.profile_data_response_schema import ProfileDataResponseSchema
from marshmallow import Schema, fields

class ProfileResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, only=("name", "uid", "photo", "caption", "link", "relationship_status", "email", "follower_count", "following_count"), dump_only=True)