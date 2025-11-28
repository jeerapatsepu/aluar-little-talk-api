# import logging
from flask import request as dd, render_template
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

blp = Blueprint("Home", __name__, description="Home")

@blp.route("/")
class Home(MethodView):
    def get(self):
        return render_template('home/index.html')
    
    def post(self, request, ard):
        email = dd.form["email"]
        password = dd["password"]
        return f"Email: {email}, Password: {password}"