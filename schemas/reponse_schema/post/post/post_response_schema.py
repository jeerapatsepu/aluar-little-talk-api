from marshmallow import Schema, fields, validate

from schemas.reponse_schema.post.post.post_data_schema import PostDataSchema

class PostResponseSchema(Schema):
    post_id = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    owner_image = fields.Str(dump_only=True)
    owner_name = fields.Str(dump_only=True)
    visibility = fields.Str(dump_only=True) # PUBLIC, PRIVATE, FRIENDS
    type = fields.Str(dump_only=True) # POST, REPOST, SHARED
    original_post_id = fields.Str(dump_only=True) # for repost, shared
    like_count = fields.Integer(dump_only=True)
    is_like = fields.Boolean(dump_only=True)
    is_bookmark = fields.Boolean(dump_only=True)
    bookmark_count = fields.Integer(dump_only=True)
    is_repost = fields.Boolean(dump_only=True)
    repost_count = fields.Integer(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)
    updated_date_timestamp = fields.Integer(dump_only=True)
    contents = fields.Nested(PostDataSchema, dump_only=True, many=True)
    is_see_more = fields.Boolean(dump_only=True)
    is_owner = fields.Boolean(dump_only=True)