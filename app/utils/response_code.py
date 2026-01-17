from enum import Enum


class ResponseCode(Enum):
    SUCCESS = 1000
    GENERAL_ERROR = 5000
    TOKEN_EXPIRED = 5001
    TOKEN_INVALID = 5002
    TOKEN_REVOKED = 50003
    REFRESH_FAIL = 50004