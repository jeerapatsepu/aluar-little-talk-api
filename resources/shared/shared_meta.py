from datetime import datetime, timezone
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.error import ErrorSchema
from app.extensions import uid

def get_meta_response(response_code: int, error: ErrorSchema = None) -> MetaSchema:
    time = datetime.now(timezone.utc)
    meta = MetaSchema()
    meta.response_id = uid.hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    return meta