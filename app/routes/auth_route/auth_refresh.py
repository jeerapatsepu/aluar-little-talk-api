from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateResponseSchema
from app.services.auth_service import refresh

blp = Blueprint("AuthRefresh", __name__, description="Auth Refresh")

@blp.route("/auth/refresh")
class AuthRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self):
        return refresh()