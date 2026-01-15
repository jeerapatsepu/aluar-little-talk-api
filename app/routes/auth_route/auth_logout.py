import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from datetime import datetime, timezone
from app.models.token_block import TokenBlock
from app.extensions import db
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.services.auth_service import logout

blp = Blueprint("AuthLogout", __name__, description="Auth Logout")

@blp.route("/auth/logout")
class AuthLogout(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self):
        return logout()