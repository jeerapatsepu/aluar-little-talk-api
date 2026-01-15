from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas.reponse_schema.auth_apple_create_response_schema import AuthAppleCreateResponseSchema
from app.schemas.request_schema.auth_apple_login_request_schema import AuthAppleLoginRequestSchema
from app.services.auth_service import login_apple_signin

blp = Blueprint("AuthLogin", __name__, description="Auth Login")

@blp.route("/auth/apple/login")
class AuthLogin(MethodView):
    @blp.arguments(AuthAppleLoginRequestSchema)
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self, request):
        user_identifier = request["user_identifier"]
        return login_apple_signin(user_identifier)