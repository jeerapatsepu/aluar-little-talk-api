import uuid
from datetime import datetime, timezone
from app.schemas.reponse_schema.meta import MetaSchema


def get_meta_sucess_response():
    time = datetime.now(timezone.utc)

    meta = MetaSchema()
    meta.response_id = uuid.uuid4().hex
    meta.response_code = 1000
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = None