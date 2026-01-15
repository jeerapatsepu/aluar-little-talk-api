from marshmallow import Schema, fields

from app.schemas.reponse_schema.meta import MetaSchema

class DeleteUserTermDataSchema(Schema):
    title = fields.Str()
    description = fields.Str()

class DeleteUserTermResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, only=("response_id", "response_code", "response_date", "response_timestamp", "error"), dump_only=True)
    data = fields.Nested(DeleteUserTermDataSchema, only=("title", "description"), dump_only=True, many=False)