from schemas.reponse_schema.meta import MetaSchema
from marshmallow import Schema, fields
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema

class PostsCommentListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(CommentResponseSchema, dump_only=True, many=True)