# import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from datetime import datetime, timezone
from models.usli import USLI
from resources.auth.auth_create.auth_create_request_schema import AuthCreateRequestSchema, AuthLoginDataResponseSchema, AuthLoginResponseSchema
from app.shared import uid, bcrypt
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("AuthLogin", __name__, description="Auth Login")

@blp.route("/login")
class AuthLogin(MethodView):
    @blp.arguments(AuthCreateRequestSchema)
    @blp.response(200, AuthLoginResponseSchema)
    def post(self, request):
        email = request["email"]
        password = request["password"]
        usli = USLI.query.filter_by(email=email).first()
        if usli and bcrypt.check_password_hash(pw_hash=usli.password, password=password):
            return self.getAuthLoginSuccessRespone(1000, usli)
        else:
            # logging.exception("AuthLogin")
            return self.getAuthLoginFailRespone(5000)

    def getAuthLoginSuccessRespone(self, response_code, user):
        access_token = create_access_token(identity=str(user.uid), fresh=True)
        refresh_token = create_refresh_token(identity=str(user.uid))
        time = datetime.now(timezone.utc)

        data = AuthLoginDataResponseSchema()
        data.access_token = access_token
        data.refresh_token = refresh_token
        data.uid = user.uid

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = AuthLoginResponseSchema()
        response.meta = meta
        response.data = data
        return response

    def getAuthLoginFailRespone(self, response_code):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "Can not authen the user"

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = AuthLoginResponseSchema()
        response.meta = meta
        response.data = None
        return response