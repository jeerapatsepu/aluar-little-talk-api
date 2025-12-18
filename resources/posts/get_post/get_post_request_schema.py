from marshmallow import Schema, fields

from resources.profile.posts.profile_posts.posts_request_schema import ProfilePostsDataResponseSchema
from schemas.meta import MetaSchema

class GetPostRequestSchema(Schema):
    post_id = fields.Str(required=True)

class GetPostResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(ProfilePostsDataResponseSchema, dump_only=True)