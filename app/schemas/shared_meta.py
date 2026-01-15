from datetime import datetime, timezone
import uuid
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.reponse_schema.error import ErrorSchema

def get_meta_response(response_code: int, error: ErrorSchema = None) -> MetaSchema:
    time = datetime.now(timezone.utc)
    meta = MetaSchema()
    meta.response_id = uuid.uuid4().hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    return meta