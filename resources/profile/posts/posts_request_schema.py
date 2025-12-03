from marshmallow import Schema, ValidationError, fields, validates_schema
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
    id = fields.Integer(dump_only=True)
    post_id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    owner_uid = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)
    visibility = fields.Str(dump_only=True) # public, private, friends
    type = fields.Str(dump_only=True) # normal, repost, shared
    original_post_id = fields.Str(dump_only=True) # for repost, shared
    like_count = fields.Integer(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    created_date_timestamp = fields.Integer(dump_only=True)
    updated_date_timestamp = fields.Integer(dump_only=True)

class ProfilePostsResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(ProfilePostsDataResponseSchema, dump_only=True, many=True)