from marshmallow import Schema, fields

class PostCommentCreateRequestSchema(Schema):
    text = fields.Str(required=True)
    image = fields.Str(required=True)
    parent_comment_uid = fields.Str(required=True)
    post_id = fields.Str(required=True)
    user_uid = fields.Str(required=True)
    reply_uid = fields.Str(required=True)