import os
from datetime import timedelta

def config(app, db_url):
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_VERSION"] = "v1"
    app.config["API_TITLE"] = "Log API"
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_timeout": 5
    }
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    app.config['OAUTH2_PROVIDERS'] = {
        # Google OAuth 2.0 documentation:
        # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
        # 'google': {
        #     'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        #     'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        #     'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        #     'token_url': 'https://accounts.google.com/o/oauth2/token',
        #     'userinfo': {
        #         'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
        #         'email': lambda json: json['email'],
        #     },
        #     'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
        # },

        # GitHub OAuth 2.0 documentation:
        # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
        'github': {
            'client_id': os.environ.get('GITHUB_CLIENT_ID'),
            'client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'token_url': 'https://github.com/login/oauth/access_token',
            'userinfo': {
                'url': 'https://api.github.com/user/emails',
                'email': lambda json: json[0]['email'],
            },
            'scopes': ['user:email'],
        },
    }