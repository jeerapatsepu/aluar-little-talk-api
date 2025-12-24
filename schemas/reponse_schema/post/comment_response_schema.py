from marshmallow import Schema, fields, validate

from schemas.reponse_schema.post.post.post_data_schema import PostDataSchema

class CommentReplySchema(Schema):
    comment_id = fields.Str(dump_only=True)
    parent_comment_id = fields.Str(dump_only=True)
    owner_image = fields.Str(dump_only=True)
    owner_name = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    post_id = fields.Str(dump_only=True)
    is_owner = fields.Boolean(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)
    updated_date_timestamp = fields.Integer(dump_only=True)
    text = fields.Str(dump_only=True)
    image_url = fields.Str(dump_only=True)
    
class CommentResponseSchema(Schema):
    comment_id = fields.Str(dump_only=True)
    parent_comment_id = fields.Str(dump_only=True)
    owner_image = fields.Str(dump_only=True)
    owner_name = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    post_id = fields.Str(dump_only=True)
    is_owner = fields.Boolean(dump_only=True)
    text = fields.Str(dump_only=True)
    image_url = fields.Str(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)
    updated_date_timestamp = fields.Integer(dump_only=True)
    reply_list = fields.Nested(CommentReplySchema,
                                only=("comment_id", "parent_comment_id", "owner_image", "owner_name", "owner_uid", "post_id", "is_owner", "created_date_timestamp", "updated_date_timestamp", "text", "image_url"),
                                dump_only=True, many=True)
    is_see_reply_more = fields.Boolean(dump_only=True)
    is_like = fields.Boolean(dump_only=True)
    like_count = fields.Integer(dump_only=True)
