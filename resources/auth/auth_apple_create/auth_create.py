from flask import redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from datetime import datetime, timezone
from models import USLI
from resources.auth.auth_apple_create.auth_apple_create_request_schema import AuthAppleCreateRequestSchema, AuthLoginDataResponseSchema, AuthLoginResponseSchema
from app.shared import db, uid
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema
from app.shared import bcrypt

blp = Blueprint("AuthCreate", __name__, description="Auth Create")

@blp.route("/auth/apple/create")
class AuthCreate(MethodView):
    @blp.arguments(AuthAppleCreateRequestSchema)
    @blp.response(200, AuthLoginResponseSchema)
    def post(self, request):
        email = request["email"]
        full_name = request["full_name"]
        user_identifier = request["user_identifier"]

        usli = USLI.query.filter_by(email=email).first()
        if usli:
            redirect("/auth/apple/login")
        else:
            id = uid.hex
            new_user = USLI(uid=id,
                            email=email,
                            full_name=full_name,
                            user_identifier=user_identifier)
            db.session.add(new_user)
            db.session.commit()
            return self.getAuthCreateSuccessResponse(1000, id)

    def getAuthCreateSuccessResponse(self, response_code, id):
        access_token = create_access_token(identity=str(id), fresh=True)
        refresh_token = create_refresh_token(identity=str(id))
        time = datetime.now(timezone.utc)

        data = AuthLoginDataResponseSchema()
        data.access_token = access_token
        data.refresh_token = refresh_token
        data.uid = id

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

    def getAuthCreateFailResponse(self, response_code):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "No user"

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