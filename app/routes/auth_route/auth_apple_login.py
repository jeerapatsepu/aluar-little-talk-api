# import logging
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timezone
from app.models.user_delete_request import UserDeleteRequest
from app.models.usli import USLI
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateDataResponseSchema, AuthAppleCreateResponseSchema
from app.schemas.reponse_schema.error import ErrorSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.auth_apple_login_request_schema import AuthAppleLoginRequestSchema
from app.extensions import db

blp = Blueprint("AuthLogin", __name__, description="Auth Login")

@blp.route("/auth/apple/login")
class AuthLogin(MethodView):
    @blp.arguments(AuthAppleLoginRequestSchema)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self, request):
        user_identifier = request["user_identifier"]
        usli = USLI.query.filter_by(user_identifier=user_identifier).first()
        if usli:
            user_delete = UserDeleteRequest.query.filter_by(user_uid=usli.uid).first()
            if user_delete:
                db.session.delete(user_delete)
                db.session.commit()
            return self.__getAuthLoginSuccessRespone(usli)
        else:
            # logging.exception("AuthLogin")
            return self.__getAuthLoginFailRespone(5000)

    def __getAuthLoginSuccessRespone(self, usli: USLI):
        access_token = create_access_token(identity=usli, fresh=True)
        refresh_token = create_refresh_token(identity=usli)
        time = datetime.now(timezone.utc)

        data = AuthAppleCreateDataResponseSchema()
        data.access_token = access_token
        data.refresh_token = refresh_token
        data.uid = usli.uid

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = AuthAppleCreateResponseSchema()
        response.meta = meta
        response.data = data
        return response

    def __getAuthLoginFailRespone(self, response_code):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "Can not authen the user"

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = AuthAppleCreateResponseSchema()
        response.meta = meta
        response.data = None
        return response