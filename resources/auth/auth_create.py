import uuid
from flask import redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timezone
from app.models.usli import USLI
from app.extensions import db
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateDataResponseSchema, AuthAppleCreateResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.auth_apple_create_request_schema import AuthAppleCreateRequestSchema

blp = Blueprint("AuthCreate", __name__, description="Auth Create")

@blp.route("/auth/apple/create")
class AuthCreate(MethodView):
    @blp.arguments(AuthAppleCreateRequestSchema)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self, request):
        email = request["email"]
        full_name = request["full_name"]
        user_identifier = request["user_identifier"]
        usli = USLI.query.filter_by(email=email).first()
        if usli:
            redirect("/auth/apple/login")
        else:
            new_user = self.__createUSLI(email, full_name, user_identifier)
            return self.__getAuthCreateSuccessResponse(new_user)
        
    def __createUSLI(self, email: str, full_name: str, user_identifier: str):
        uid = uuid.uuid4().hex
        new_user = USLI(uid=uid,
                        email=email,
                        full_name=full_name,
                        user_identifier=user_identifier)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def __getAuthCreateSuccessResponse(self, new_user: USLI):
        access_token = create_access_token(identity=new_user, fresh=True)
        refresh_token = create_refresh_token(identity=new_user)
        time = datetime.now(timezone.utc)

        data = AuthAppleCreateDataResponseSchema()
        data.access_token = access_token
        data.refresh_token = refresh_token
        data.uid = new_user.uid

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