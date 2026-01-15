from marshmallow import Schema, fields
from app.schemas.reponse_schema.meta import MetaSchema

class PostActionResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)