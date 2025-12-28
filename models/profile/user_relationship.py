from app.shared import db


class UserRelationship(db.Model):
    __tablename__ = "user_relationships"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String)
    receiver_id = db.Column(db.String)
    status = db.Column(db.String) # e.g., 'FOLLOW', 'BLOCKED', 'FRIEND' is only in response
    created_date_timestamp = db.Column(db.Integer)