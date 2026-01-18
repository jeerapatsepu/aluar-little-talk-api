import uuid
from datetime import datetime, timezone
from app.schemas.reponse_schema.error import ErrorSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.utils.response_code import ResponseCode


def get_meta_sucess_response():
    time = datetime.now(timezone.utc)

    meta = MetaSchema()
    meta.response_id = uuid.uuid4().hex
    meta.response_code = ResponseCode.SUCCESS.value
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = None
    return meta

def get_meta_fail_response(code: int, error_title: str, error_description: str):
    time = datetime.now(timezone.utc)

    error = ErrorSchema()
    error.title = error_title
    error.message = error_description

    meta = MetaSchema()
    meta.response_id = uuid.uuid4().hex
    meta.response_code = code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    return meta

def get_meta_fail_jsonify_response(code: int, error_title: str, error_description: str):
    time = datetime.now(timezone.utc)

    meta = MetaSchema()
    meta.response_id = uuid.uuid4().hex
    meta.response_code = code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())

    return {
        "meta": {
            "response_id": meta.response_id,
            "response_code": meta.response_code,
            "response_date": meta.response_date,
            "response_timestamp": meta.response_timestamp,
            "error": {
                "title": error_title,
                "message": error_description
            }
        }
    }