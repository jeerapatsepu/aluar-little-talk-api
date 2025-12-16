from marshmallow import Schema, ValidationError, fields, validates_schema
from resources.posts.post_create.post_create_request_schema import PostCreateDataRequestSchema
from schemas.meta import MetaSchema

class ProfilePostsRequestSchema(Schema):
    uid = fields.Str(required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        if len(data["uid"]) <= 0:
            raise ValidationError("UID must be not empty", "uid")

class ProfilePostsDataResponseSchema(Schema):
    post_id = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    owner_image = fields.Str(dump_only=True)
    owner_name = fields.Str(dump_only=True)
    visibility = fields.Str(dump_only=True) # PUBLIC, PRIVATE, FRIENDS
    type = fields.Str(dump_only=True) # POST, REPOST, SHARED
    original_post_id = fields.Str(dump_only=True) # for repost, shared
    like_count = fields.Integer(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)
    updated_date_timestamp = fields.Integer(dump_only=True)
    contents = fields.Nested(PostCreateDataRequestSchema, dump_only=True, many=True)
    is_see_more = fields.Boolean(dump_only=True)

class ProfilePostsResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(ProfilePostsDataResponseSchema, dump_only=True, many=True)