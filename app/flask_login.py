from flask_login import login_manager
from models.usli import USLI

@login_manager.user_loader
def load_user(user_id):
    return USLI.query.filter_by(uid=user_id).one_or_none()