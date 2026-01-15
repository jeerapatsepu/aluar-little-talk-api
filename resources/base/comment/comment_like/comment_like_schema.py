from app.schemas.reponse_schema.meta import MetaSchema
from marshmallow import Schema, fields
from app.schemas.reponse_schema.comment_response_schema import CommentResponseSchema

class CommentLikeResquestSchema(Schema):
    comment_id = fields.Str(required=True)

class CommentLikeResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)