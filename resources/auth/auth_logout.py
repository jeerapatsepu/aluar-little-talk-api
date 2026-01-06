import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from datetime import datetime, timezone
from models.token_block import TokenBlock
from app.shared import db
from schemas.reponse_schema.auth.auth_apple_create_response_schema import AuthAppleCreateResponseSchema
from schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("AuthLogout", __name__, description="Auth Logout")

@blp.route("/auth/logout")
class AuthLogout(MethodView):
    @jwt_required()
    @blp.response(200, AuthAppleCreateResponseSchema)
    def post(self, request):
        jti = get_jwt()["jti"]
        now = int(datetime.now(timezone.utc).timestamp())
        token_block = TokenBlock(jti=jti, created_date_timestamp=now)
        db.session.add(token_block)
        db.session.commit()
        return self.__getAuthLogoutSuccessResponse()

    def __getAuthLogoutSuccessResponse(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = AuthAppleCreateResponseSchema()
        response.meta = meta
        return response