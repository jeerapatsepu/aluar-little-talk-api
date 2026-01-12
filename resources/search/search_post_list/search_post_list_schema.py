from marshmallow import Schema, fields, validate

from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

class SearchPostListRequestSchema(Schema):
    search = fields.Str(required=True, validate=validate.Length(min=1))
    offset = fields.Integer(required=True)
    limit = fields.Integer(required=True)

class SearchPostListDataSchema(Schema):
    content_id = fields.Str(dump_only=True)
    post_id = fields.Str(dump_only=True)
    type = fields.Str(dump_only=True)
    text = fields.Str(dump_only=True)
    text_type = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    owner_name = fields.Str(dump_only=True)
    owner_photo = fields.Str(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)

class SearchPostListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(SearchPostListDataSchema, only=("content_id", "post_id", "type", "text", "text_type", "owner_uid", "owner_name", "owner_photo", "created_date_timestamp"), dump_only=True, many=True)