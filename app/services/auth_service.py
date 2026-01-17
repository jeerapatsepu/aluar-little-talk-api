from datetime import datetime, timezone
import logging
import uuid
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity
from app.models.token_block import TokenBlock
from app.models.user_delete_request import UserDeleteRequest
from app.models.usli import USLI
from app.extensions import db
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateDataResponseSchema, AuthAppleCreateResponseSchema
from app.utils.response_code import ResponseCode
from app.utils.resposne_helper import get_meta_fail_response, get_meta_sucess_response

def login_apple_signin(user_identifier: str):
    usli = USLI.query.filter_by(user_identifier=user_identifier).first()
    if usli:
        __delete_user_request_deactivate(usli.uid)
        return __get_login_apple_signin_success(usli)
    else:
        return __get_login_apple_signin_fail()
    
def register_apple_signin(request):
    email = request["email"]
    full_name = request["full_name"]
    user_identifier = request["user_identifier"]
    usli = USLI.query.filter_by(email=email).first()
    if usli:
        return login_apple_signin(user_identifier)
    else:
        new_user = __create_usli_model(email, full_name, user_identifier)
        return __get_register_apple_signin_success(new_user)

def logout():
    current_user = get_jwt_identity()
    if current_user:
        jti = get_jwt()["jti"]
        now = int(datetime.now(timezone.utc).timestamp())
        token_block = TokenBlock(jti=jti, created_date_timestamp=now)
        db.session.add(token_block)
        db.session.commit()
        return __get_logout_success_response()
    else:
        return __get_logout_fail_response()

def refresh():
    indentity = get_jwt_identity()
    usli = USLI.query.filter(USLI.uid==indentity.uid).first()
    if usli:
        return __get_register_apple_signin_success(usli)
    else:
        return __get_refresh_fail_response()

def __delete_user_request_deactivate(uid: str):
    user_delete = UserDeleteRequest.query.filter_by(user_uid=uid).first()
    if user_delete:
        db.session.delete(user_delete)
        db.session.commit()

def __create_usli_model(email: str, full_name: str, user_identifier: str):
        uid = uuid.uuid4().hex
        new_user = USLI(uid=uid,
                        email=email,
                        full_name=full_name,
                        user_identifier=user_identifier)
        db.session.add(new_user)
        db.session.commit()
        return new_user

def __get_register_apple_signin_success(new_user: USLI):
    access_token = create_access_token(identity=new_user)
    refresh_token = create_refresh_token(identity=new_user)

    data = AuthAppleCreateDataResponseSchema()
    data.access_token = access_token
    data.refresh_token = refresh_token
    data.uid = new_user.uid

    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_sucess_response()
    response.data = data
    return response

def __get_login_apple_signin_success(usli: USLI):
    access_token = create_access_token(identity=usli)
    refresh_token = create_refresh_token(identity=usli)

    data = AuthAppleCreateDataResponseSchema()
    data.access_token = access_token
    data.refresh_token = refresh_token
    data.uid = usli.uid

    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_sucess_response()
    response.data = data
    return response

def __get_login_apple_signin_fail():
    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_fail_response(5000, "Service can not answer", "Can not authen the user")
    response.data = None
    return response

def __get_logout_success_response():
    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_sucess_response()
    return response

def __get_logout_fail_response():
    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_fail_response(ResponseCode.GENERAL_ERROR.value, "Service can not answer", "Can not authen the user")
    return response

def __get_refresh_fail_response():
    response = AuthAppleCreateResponseSchema()
    response.meta = get_meta_fail_response(ResponseCode.REFRESH_FAIL.value, "Service can not answer", "Can not authen the user")
    return response