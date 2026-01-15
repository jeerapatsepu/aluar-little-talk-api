from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.models.token_block import TokenBlock
from app.models.usli import USLI

class JWTHelper:
    def __init__(self, app: Flask):
        self.__app = app

    def register_callback(self):
        jwt = JWTManager(self.__app)
        self.__register_callback_user_identity_loader(jwt)
        self.__register_callback_user_lookup_loader(jwt)
        self.__register_callback_needs_fresh_token_loader(jwt)
        self.__register_callback_token_in_blocklist_loader(jwt)
        self.__register_callback_revoked_token_loader(jwt)
        self.__register_callback_additional_claims_loader(jwt)
        self.__register_callback_expired_token_loader(jwt)
        self.__register_callback_invalid_token_loader(jwt)
        self.__register_callback_unauthorized_loader(jwt)

    def __register_callback_user_identity_loader(self, jwt: JWTManager):
        @jwt.user_identity_loader
        def user_identity_lookup(user):
            return user.uid
    
    def __register_callback_user_lookup_loader(self, jwt: JWTManager):
        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            return USLI.query.filter_by(uid=identity).one_or_none()
    
    def __register_callback_needs_fresh_token_loader(self, jwt: JWTManager):
        @jwt.needs_fresh_token_loader
        def token_not_fresh_callback(jwt_header, jwt_payload):
            return (
                jsonify(
                    {
                        "description": "The token is not fresh.",
                        "error": "fresh_token_required",
                    }
                    ),
                    401,
                )
    
    def __register_callback_token_in_blocklist_loader(self, jwt: JWTManager):
        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
            jti = jwt_payload["jti"]
            token = TokenBlock.query.filter_by(jti=jti).scalar()
            return token is not None
    
    def __register_callback_revoked_token_loader(self, jwt: JWTManager):
        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):
            return (
                jsonify(
                    {"description": "The token has been revoked.", "error": "token_revoked"}
                ),
                401,
            )
    
    def __register_callback_additional_claims_loader(self, jwt: JWTManager):
        @jwt.additional_claims_loader
        def add_claims_to_jwt(identity):
            # if identity == 1:
            #     return {"is_admin": True}
            return {"is_admin": False}
    
    def __register_callback_expired_token_loader(self, jwt: JWTManager):
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return (
                jsonify({"message": "The token has expired.", "error": "token_expired"}),
                401,
            )
        
    def __register_callback_invalid_token_loader(self, jwt: JWTManager):
        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            return (
                jsonify(
                    {"message": "Signature verification failed.", "error": "invalid_token"}
                ),
                401,
            )
    
    def __register_callback_unauthorized_loader(self, jwt: JWTManager):
        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return (
                jsonify(
                    {
                        "description": "Request does not contain an access token.",
                        "error": "authorization_required",
                    }
                ),
                401,
            )