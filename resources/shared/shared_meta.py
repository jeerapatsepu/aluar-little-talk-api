from datetime import datetime, timezone
from schemas.meta import MetaSchema
from schemas.error import ErrorSchema
from app.shared import uid

def get_meta_response(response_code: int, error: ErrorSchema = None) -> MetaSchema:
    time = datetime.now(timezone.utc)
    meta = MetaSchema()
    meta.response_id = uid.hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    return meta