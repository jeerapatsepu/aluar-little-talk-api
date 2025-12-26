from marshmallow import Schema, fields, validate

from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

class PostCommentUserListRequestSchema(Schema):
    comment_id = fields.Str(required=True, validate=validate.Length(min=1))
    offset = fields.Integer(required=True)
    limit = fields.Integer(required=True)