from marshmallow import Schema, fields, validate

from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.profile_data_response_schema import ProfileDataResponseSchema

class SearchUserListRequestSchema(Schema):
    search = fields.Str(required=True, validate=validate.Length(min=1))
    offset = fields.Integer(required=True)
    limit = fields.Integer(required=True)

class SearchUserListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(ProfileDataResponseSchema, only=("name", "uid", "photo", "caption", "link", "email"), dump_only=True, many=True)