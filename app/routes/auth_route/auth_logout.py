from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateResponseSchema
from app.services.auth_service import logout

blp = Blueprint("AuthLogout", __name__, description="Auth Logout")

@blp.route("/auth/logout")
class AuthLogout(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self):
        return logout()