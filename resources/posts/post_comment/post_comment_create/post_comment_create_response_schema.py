from schemas.reponse_schema.meta import MetaSchema
from marshmallow import Schema, fields
from schemas.reponse_schema.post.comment_response_schema import CommentResponseSchema

class PostsCommentCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(CommentResponseSchema, dump_only=True)