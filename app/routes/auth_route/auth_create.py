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
from app.services.auth_service import register_apple_signin

blp = Blueprint("AuthCreate", __name__, description="Auth Create")

@blp.route("/auth/apple/create")
class AuthCreate(MethodView):
    @blp.arguments(AuthAppleCreateRequestSchema)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self, request):
        return register_apple_signin(request)