from app.shared import db

class UserDeleteRequest(db.Model):
    __tablename__ = "user_delete_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)