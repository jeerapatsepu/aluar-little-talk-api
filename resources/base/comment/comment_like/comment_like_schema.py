from schemas.reponse_schema.meta import MetaSchema
from marshmallow import Schema, fields, validate
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema

class CommentLikeResquestSchema(Schema):
    comment_id = fields.Str(required=True)

class CommentLikeResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)