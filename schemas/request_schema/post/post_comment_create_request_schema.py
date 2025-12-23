from marshmallow import Schema, fields, validate
from schemas.reponse_schema.post.post.post_response_schema import PostDataSchema

class PostCommentCreateRequestSchema(Schema):
    text = fields.Str(required=True)
    image = fields.Str(required=True)
    parent_comment_uid = fields.Str(required=True)
    reply_user_uid = fields.Str(required=True)
    post_id = fields.Str(required=True)
    user_uid = fields.Str(required=True)